"""The context budget of a local model, measured and not guessed (spec M4 open item 9a).

Run from the repository root, for example:

    py tools/context_budget.py C:\\models\\Some-Model-27B-Q4_K_M.gguf --vram 24 --headroom 1.5

It reads the GGUF file's header with the `gguf` package (llama.cpp's own reader, in the
`agents` extra, which `dev` brings): the architecture, the layer count, the key-value
head count (one for all layers, or one a layer), the head width, the sliding window if
the model has one, the context it was trained to, and the file's size on disk (the
weights). It prints the KV cache's bytes per token at f16 and at q8_0, and the largest
`--ctx-size` that fits the card's memory after the weights and a headroom the owner
sets. `docs/agents/Harness.md` has the table the owner fills from it, one row for each
model with a consent record; the owner's observed range for the two 26B and 27B models
on a 4090 (80k to 110k tokens, 2026-09-28) is what the figures are checked against.

**The formula.** llama.cpp's KV cache keeps two tensors a layer, K and V, each of the
layer's key-value heads times the head width, for every token of the context, in the
cache's type (`--cache-type-k`, `--cache-type-v`; f16 unless told otherwise; the cache
in llama.cpp's `src/llama-kv-cache.cpp`, the widths `n_embd_k_gqa` and `n_embd_v_gqa` of
`src/llama-hparams.h`: KV heads x head width). So, a token:

    bytes = sum over layers of KV heads x (key width + value width) x bytes an element
          = 2 tensors x layers x KV heads x head width x 2 bytes, at f16 with equal widths

An element is 2 bytes at f16 and 34/32 bytes at q8_0 (ggml's `block_q8_0`, in
`ggml/src/ggml-common.h`: a half-precision scale and 32 one-byte values, 34 bytes for 32
elements; about half of f16). The key and value widths are the header's `key_length` and
`value_length`, or the embedding length over the head count where it gives none.

**The sliding window.** A model whose header gives a sliding window has layers that
attend only to the last so many tokens, and llama.cpp keeps those layers' cache at about
the window's size unless it is started with `--swa-full`. Which layers slide is in the
header's `sliding_window_pattern` where the converter wrote it (one flag a layer, or a
period n: every n-th layer attends to the whole context); where it did not, the owner
gives the period with `--swa-every N` from the model's card or llama.cpp's source. The
script prints the full-context figure (every layer at the whole context, the formula
above, an upper bound on the cache) and, where the pattern is known, the figure with the
sliding layers at their window, which is the one to set `--ctx-size` by.

**What fits.** The card's memory, less the weights (the file's size: all layers on the
card, `--n-gpu-layers 99`), less the headroom (the CUDA context, llama.cpp's compute
buffers, which grow with the batch size, and the desktop's share of the card; a
judgement the owner makes, 1.5 GiB by default), is what the cache may take; the largest
context is that over the bytes a token, rounded down to a multiple of 1,024. Memory is
in GiB (2^30 bytes), as a card's memory is counted (a 4090's 24 GiB). A model whose
weights and headroom alone do not fit is said so, with the numbers, and the script
exits 1.

It is a tool, not a test of the game: nothing here touches a World. The test writes a
synthetic header (`tests/test_context_budget.py`); no GGUF is in the repository.
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# A card's memory and the headroom, in GiB (the defaults: the owner's card, a 4090, and
# a judgement for the CUDA context, the compute buffers and the desktop).
GIB = 2**30
DEFAULT_VRAM_GIB = 24.0
DEFAULT_HEADROOM_GIB = 1.5

# Bytes an element of the cache (ggml: f16 two bytes; block_q8_0 34 bytes for 32).
CACHE_TYPES: dict[str, float] = {"f16": 2.0, "q8_0": 34 / 32}

# `--ctx-size` is rounded down to a multiple of this (a tidy figure; llama-server takes
# any).
CTX_STEP = 1024


@dataclass(frozen=True)
class Header:
    """What the budget needs from a GGUF header."""

    architecture: str
    layers: int
    kv_heads: tuple[int, ...]  # one a layer
    key_width: int
    value_width: int
    context_length: int | None
    sliding_window: int | None
    swa_layers: tuple[bool, ...] | None  # one a layer, where the pattern is known
    key_width_swa: int | None = None
    value_width_swa: int | None = None
    size_bytes: int = 0

    def elements_a_token(self) -> tuple[int, int]:
        """The cache's elements a token: (the layers at the whole context, the sliding
        layers), where the pattern is known; else every layer is at the whole context."""
        full = swa = 0
        for il in range(self.layers):
            kv = self.kv_heads[il]
            sliding = bool(self.swa_layers and self.sliding_window and self.swa_layers[il])
            if sliding:
                k = self.key_width_swa or self.key_width
                v = self.value_width_swa or self.value_width
                swa += kv * (k + v)
            else:
                full += kv * (self.key_width + self.value_width)
        return full, swa

    def upper_bound_elements(self) -> int:
        """Every layer at the whole context: the formula as the spec states it."""
        return sum(kv * (self.key_width + self.value_width) for kv in self.kv_heads)


def _value(fields: dict[str, Any], key: str) -> Any:
    f = fields.get(key)
    return None if f is None else f.contents()


def _per_layer(value: Any, layers: int, what: str) -> tuple[int, ...]:
    if isinstance(value, list):
        if len(value) != layers:
            raise ValueError(f"the header gives {len(value)} {what} for {layers} layers")
        return tuple(int(x) for x in value)
    return (int(value),) * layers


def swa_pattern(value: Any, layers: int) -> tuple[bool, ...] | None:
    """The sliding layers from a header's `sliding_window_pattern` or `--swa-every`: a
    list of flags (true: the layer slides) as it stands, or a period n (every n-th layer,
    the n-th, 2n-th and so on, attends to the whole context; llama.cpp's
    `set_swa_pattern`)."""
    if value is None:
        return None
    if isinstance(value, list):
        if len(value) != layers:
            return None
        return tuple(bool(x) for x in value)
    n = int(value)
    if n <= 1:
        return (False,) * layers
    return tuple(il % n != n - 1 for il in range(layers))


def read_header(path: str | os.PathLike[str], swa_every: int | None = None) -> Header:
    """The header of a GGUF file, through the `gguf` package's reader."""
    try:
        from gguf import GGUFReader
    except ImportError:
        raise SystemExit(
            "The gguf package is needed to read the file's header: py -m pip install -e "
            '".[agents]" (or pip install gguf).'
        ) from None
    reader = GGUFReader(path)
    fields = reader.fields
    arch = _value(fields, "general.architecture")
    if not arch:
        raise ValueError("the header gives no general.architecture")
    arch = str(arch)

    def key(name: str) -> Any:
        return _value(fields, f"{arch}.{name}")

    layers = key("block_count")
    if layers is None:
        raise ValueError(f"the header gives no {arch}.block_count")
    layers = int(layers)
    heads = key("attention.head_count")
    kv = key("attention.head_count_kv")
    if kv is None:
        kv = heads  # no grouping: as many key-value heads as heads
    if kv is None:
        raise ValueError(f"the header gives no {arch}.attention.head_count_kv or head_count")
    kv_heads = _per_layer(kv, layers, "key-value head counts")
    k = key("attention.key_length")
    v = key("attention.value_length")
    if k is None or v is None:
        emb = key("embedding_length")
        h = heads[0] if isinstance(heads, list) else heads
        if emb is None or not h:
            raise ValueError(f"the header gives no {arch}.attention.key_length")
        width = int(emb) // int(h)
        k = width if k is None else k
        v = width if v is None else v
    window = key("attention.sliding_window")
    pattern = swa_pattern(
        swa_every if swa_every else key("attention.sliding_window_pattern"), layers
    )
    ctx = key("context_length")
    return Header(
        architecture=arch,
        layers=layers,
        kv_heads=kv_heads,
        key_width=int(k),
        value_width=int(v),
        context_length=int(ctx) if ctx is not None else None,
        sliding_window=int(window) if window else None,
        swa_layers=pattern if window else None,
        key_width_swa=_int_or_none(key("attention.key_length_swa")),
        value_width_swa=_int_or_none(key("attention.value_length_swa")),
        size_bytes=Path(path).stat().st_size,
    )


def _int_or_none(value: Any) -> int | None:
    return None if value is None else int(value)


def cache_bytes(elements: tuple[int, int], window: int | None, ctx: int, per: float) -> float:
    """The cache's bytes at a context of `ctx` tokens: the whole-context layers for every
    token, the sliding layers for at most the window."""
    full, swa = elements
    held = min(ctx, window) if window else ctx
    return (full * ctx + swa * held) * per


def largest_context(
    elements: tuple[int, int], window: int | None, room_bytes: float, per: float
) -> int | None:
    """The largest context whose cache fits `room_bytes`, or None when every layer slides
    (the cache is bounded by the window, not the context)."""
    full, swa = elements
    if room_bytes <= 0:
        return 0
    if full == 0:
        return None
    if window and swa:
        at_window = (full + swa) * window * per
        if room_bytes >= at_window:
            return int((room_bytes - swa * window * per) // (full * per))
        return int(room_bytes // ((full + swa) * per))
    return int(room_bytes // (full * per))


def _gib(n: float) -> str:
    return f"{n / GIB:,.2f} GiB"


def report(h: Header, name: str, vram_gib: float, headroom_gib: float) -> tuple[list[str], int]:
    """The lines the script prints, and its exit code."""
    widths = (
        f"head width {h.key_width}"
        if h.key_width == h.value_width
        else f"key width {h.key_width}, value width {h.value_width}"
    )
    kv = (
        f"{h.kv_heads[0]} key-value heads"
        if len(set(h.kv_heads)) == 1
        else f"key-value heads by layer from {min(h.kv_heads)} to {max(h.kv_heads)}"
    )
    trained = f"{h.context_length:,} tokens" if h.context_length else "not given"
    out = [
        f"{name}: {h.architecture}, {h.layers} layers, {kv}, {widths}; trained context {trained}.",
        f"Weights (the file on disk): {_gib(h.size_bytes)} ({h.size_bytes:,} bytes).",
    ]
    upper = h.upper_bound_elements()
    elements = h.elements_a_token()
    sliding = h.sliding_window is not None and h.swa_layers is not None and elements[1] > 0
    for cache, per in CACHE_TYPES.items():
        out.append(
            f"KV cache a token at {cache}, every layer at the whole context: "
            f"{upper * per:,.0f} bytes ({upper * per / 1024:,.1f} KiB)."
        )
    if h.sliding_window and not sliding:
        out.append(
            f"The model has a sliding window of {h.sliding_window:,} tokens, but the header "
            "does not say which layers slide: the figures count every layer at the whole "
            "context, an upper bound. Give the period with --swa-every N (from the model's "
            "card) for the figure llama.cpp will use without --swa-full."
        )
    if sliding:
        n_swa = sum(1 for x in h.swa_layers or () if x)
        out.append(
            f"Sliding window: {h.sliding_window:,} tokens on {n_swa} of {h.layers} layers, "
            "whose cache llama.cpp holds at about the window unless started with --swa-full."
        )
    room = vram_gib * GIB - h.size_bytes - headroom_gib * GIB
    out.append(
        f"On a card of {vram_gib:g} GiB with {headroom_gib:g} GiB of headroom, the cache may "
        f"take {_gib(max(room, 0))}."
    )
    if room <= 0:
        out.append(
            f"The weights ({_gib(h.size_bytes)}) and the headroom ({headroom_gib:g} GiB) alone "
            f"do not fit a card of {vram_gib:g} GiB: use a smaller quantisation, or keep some "
            "layers off the card (--n-gpu-layers), which slows every reply."
        )
        return out, 1
    rows = [("every layer at the whole context", (upper, 0), None)]
    if sliding:
        rows.append(("the sliding layers at their window", elements, h.sliding_window))
    for words, els, window in rows:
        for cache, per in CACHE_TYPES.items():
            n = largest_context(els, window, room, per)
            if n is None:
                out.append(
                    f"  {cache}, {words}: every layer slides; the context is not bounded "
                    "by the cache."
                )
                continue
            step = (n // CTX_STEP) * CTX_STEP
            over = (
                f" (more than the {h.context_length:,} it was trained to)"
                if h.context_length and step > h.context_length
                else ""
            )
            out.append(f"  {cache}, {words}: at most {n:,} tokens; --ctx-size {step}{over}.")
    out.append(
        "A q8_0 cache is --cache-type-k q8_0 --cache-type-v q8_0, which llama.cpp gives the "
        "V cache only with flash attention (-fa)."
    )
    return out, 0


def main(argv: list[str] | None = None, out: Any = None) -> int:
    out = out or sys.stdout
    ap = argparse.ArgumentParser(
        description="FreeSail: the KV cache a token of a GGUF model, and the largest "
        "--ctx-size that fits a card"
    )
    ap.add_argument("gguf", help="the model's .gguf file")
    ap.add_argument(
        "--vram",
        type=float,
        default=DEFAULT_VRAM_GIB,
        help=f"the card's memory in GiB (default {DEFAULT_VRAM_GIB:g}, a 4090)",
    )
    ap.add_argument(
        "--headroom",
        type=float,
        default=DEFAULT_HEADROOM_GIB,
        help=f"GiB kept free for everything but the weights and the cache (default "
        f"{DEFAULT_HEADROOM_GIB:g})",
    )
    ap.add_argument(
        "--swa-every",
        type=int,
        help="for a sliding-window model whose header does not say: every N-th layer "
        "attends to the whole context (from the model's card)",
    )
    args = ap.parse_args(argv)
    try:
        h = read_header(args.gguf, args.swa_every)
    except (OSError, ValueError) as e:
        print(f"Could not read the header of {args.gguf}: {e}", file=out)
        return 2
    lines, code = report(h, Path(args.gguf).name, args.vram, args.headroom)
    for line in lines:
        print(line, file=out)
    return code


if __name__ == "__main__":
    sys.exit(main())
