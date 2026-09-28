"""`tools/context_budget.py` (spec M4 open item 9a) on a synthetic GGUF header the test
writes byte by byte (GGUF version 3: the magic, the version, the tensor and key-value
counts, then the key-value pairs; no tensors), padded to a size that stands for the
weights. No GGUF is in the repository and no model is read; the made-up architecture's
numbers are chosen so the formula can be checked by hand.
"""

from __future__ import annotations

import io
import struct
import sys
from pathlib import Path

import pytest

pytest.importorskip("gguf")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import context_budget as CB  # noqa: E402

GIB = 2**30

# GGUF value types (llama.cpp's gguf.h: GGUF_TYPE_UINT32 4, BOOL 7, STRING 8, ARRAY 9).
UINT32, BOOL, STRING, ARRAY = 4, 7, 8, 9


def _string(s: str) -> bytes:
    b = s.encode("utf-8")
    return struct.pack("<Q", len(b)) + b


def _value(v) -> tuple[int, bytes]:
    if isinstance(v, bool):
        return BOOL, struct.pack("<?", v)
    if isinstance(v, int):
        return UINT32, struct.pack("<I", v)
    if isinstance(v, str):
        return STRING, _string(v)
    kinds = {_value(x)[0] for x in v}
    (kind,) = kinds
    body = b"".join(_value(x)[1] for x in v)
    return ARRAY, struct.pack("<IQ", kind, len(v)) + body


def write_gguf(path: Path, kv: dict, size: int) -> Path:
    """A GGUF v3 file with these key-value pairs and no tensors, padded to `size` bytes."""
    out = b"GGUF" + struct.pack("<IQQ", 3, 0, len(kv))
    for key, value in kv.items():
        kind, body = _value(value)
        out += _string(key) + struct.pack("<I", kind) + body
    out += b"\0" * (-len(out) % 32)  # the data section's alignment (general.alignment, 32)
    assert len(out) <= size
    path.write_bytes(out + b"\0" * (size - len(out)))
    return path


def made_up(tmp_path: Path, size: int = 64 * 2**20, **extra) -> Path:
    kv = {
        "general.architecture": "madeup",
        "madeup.block_count": 8,
        "madeup.context_length": 32768,
        "madeup.embedding_length": 1024,
        "madeup.attention.head_count": 16,
        "madeup.attention.head_count_kv": 4,
        "madeup.attention.key_length": 64,
        "madeup.attention.value_length": 64,
    }
    kv.update(extra)
    return write_gguf(tmp_path / "Made-Up-Model-1B-Q4_K_M.gguf", kv, size)


def test_the_header_is_read_and_the_formula_holds(tmp_path):
    h = CB.read_header(made_up(tmp_path))
    assert (h.architecture, h.layers, h.kv_heads, h.key_width, h.value_width) == (
        "madeup",
        8,
        (4,) * 8,
        64,
        64,
    )
    assert h.context_length == 32768 and h.size_bytes == 64 * 2**20
    # two tensors a layer x layers x KV heads x head width x two bytes at f16
    assert h.upper_bound_elements() * 2 == 2 * 8 * 4 * 64 * 2 == 8192
    assert CB.CACHE_TYPES["q8_0"] == 34 / 32


def test_the_script_prints_the_bytes_a_token_and_the_largest_context(tmp_path):
    path = made_up(tmp_path)
    out = io.StringIO()
    # 1 GiB card, 64 MiB of weights, 0.5 GiB headroom: 448 MiB for the cache
    code = CB.main([str(path), "--vram", "1", "--headroom", "0.5"], out=out)
    text = out.getvalue()
    assert code == 0
    assert "madeup, 8 layers, 4 key-value heads, head width 64" in text
    assert "KV cache a token at f16, every layer at the whole context: 8,192 bytes" in text
    assert "at q8_0, every layer at the whole context: 4,352 bytes" in text
    room = 1 * GIB - 64 * 2**20 - GIB // 2
    f16 = room // 8192
    assert f"f16, every layer at the whole context: at most {f16:,} tokens" in text
    assert f"--ctx-size {(f16 // 1024) * 1024} (more than the 32,768 it was trained to)" in text
    q8 = int(room // (8 * 4 * 128 * 34 / 32))
    assert f"q8_0, every layer at the whole context: at most {q8:,} tokens" in text


def test_weights_that_do_not_fit_are_said_so_with_the_numbers(tmp_path):
    path = made_up(tmp_path)
    out = io.StringIO()
    code = CB.main([str(path), "--vram", "0.5", "--headroom", "0.5"], out=out)
    assert code == 1
    assert "do not fit a card of 0.5 GiB" in out.getvalue()


def test_a_sliding_window_is_counted_at_its_window_where_the_pattern_is_known(tmp_path):
    """Every fourth layer at the whole context, the rest at a window of 1,024 tokens:
    two full layers and six sliding ones."""
    path = made_up(
        tmp_path,
        **{"madeup.attention.sliding_window": 1024, "madeup.attention.sliding_window_pattern": 4},
    )
    h = CB.read_header(path)
    assert h.swa_layers == (True, True, True, False) * 2
    full, swa = h.elements_a_token()
    assert (full, swa) == (2 * 4 * 128, 6 * 4 * 128)
    room = 1 * GIB - 64 * 2**20 - GIB // 2
    n = CB.largest_context((full, swa), 1024, room, 2.0)
    assert n == int((room - swa * 1024 * 2) // (full * 2))
    assert CB.cache_bytes((full, swa), 1024, n, 2.0) <= room
    out = io.StringIO()
    CB.main([str(path), "--vram", "1", "--headroom", "0.5"], out=out)
    text = out.getvalue()
    assert "Sliding window: 1,024 tokens on 6 of 8 layers" in text
    assert f"f16, the sliding layers at their window: at most {n:,} tokens" in text
    # a flag a layer, as some converters write it, and the owner's --swa-every where the
    # header gives the window alone
    flags = [True, False] * 4
    assert CB.swa_pattern(flags, 8) == tuple(flags)
    bare = made_up(tmp_path, **{"madeup.attention.sliding_window": 1024})
    assert CB.read_header(bare).swa_layers is None
    out = io.StringIO()
    CB.main([str(bare), "--vram", "1", "--headroom", "0.5"], out=out)
    assert "does not say which layers slide" in out.getvalue()
    assert CB.read_header(bare, swa_every=4).swa_layers == (True, True, True, False) * 2


def test_per_layer_key_value_heads_are_summed(tmp_path):
    path = made_up(tmp_path, **{"madeup.attention.head_count_kv": [4, 4, 2, 2, 0, 0, 8, 8]})
    h = CB.read_header(path)
    assert h.upper_bound_elements() == (4 + 4 + 2 + 2 + 0 + 0 + 8 + 8) * 128


def test_harness_md_has_the_command_the_table_and_the_owners_range():
    text = (ROOT / "docs/agents/Harness.md").read_text(encoding="utf-8")
    assert "py tools/context_budget.py" in text
    assert "80k to 110k" in text and "2026-09-28" in text
    assert "| Model (the consent record's name) |" in text
