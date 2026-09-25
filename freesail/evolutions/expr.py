"""A tiny, safe expression language for evolution files.

Evolution files (``data/evolutions/*.yaml``) need to ask small questions about
the ship ("is this sail furled?", "is anything in its spar chain wrecked?")
and to describe small changes ("set the sail's state to loosed", "brace the
yard to 30 degrees on the starboard tack"). Those questions and changes are
written as short expressions in the file. This module reads them without
ever calling Python's ``eval``: it breaks the text into tokens, builds a
little tree, and walks the tree with a fixed table of allowed names and
functions. Nothing in an expression can reach anything outside that table.

What an expression may contain
------------------------------

Values
    Numbers (``2``, ``0.8``, ``-30``), quoted strings (``'starboard'``), the
    words ``true``, ``false`` and ``none``, and lists (``[furled, loosed]``).
    A bare word that is not a known name is taken as a string, so
    ``sail.state == furled`` compares against the text ``"furled"``.

Names
    ``sail``, ``yard``, ``spar``, ``line``: the subject of the evolution,
    bound as its kind allows (a yard is both ``spar`` and ``yard``).
    ``subject``: the subject whatever its kind. ``ship``: the ship.
    ``params``: the parameters the order supplied, merged over the file's
    defaults. ``dyn`` is a short name for ``ship.dyn``.

Dotted attributes
    ``sail.state``, ``yard.brace_limit``, ``ship.dyn.speed``,
    ``params.target_deg``. Reading only; names beginning with an underscore
    are refused. On a dictionary (``params``) the dot looks up a key and
    gives ``none`` when the key is absent.

Graph questions (the ship's own role queries)
    ``yard_of(sail)``, ``sail_of(yard)``, ``halyard_of(part)``,
    ``spar_chain(part)``, ``spar_of_role(sail, boom)``, ``mast_of(part)``,
    ``parent_of(spar)``, ``sails_on(spar)``, ``braces_of(yard)``,
    ``sheets_of(sail)``, ``lines_of(part)``, ``line_of(part, cls)``.
    ``wrecked(x)`` is true when ``x`` (a spar, a sail, or a list of spars,
    such as ``spar_chain(sail)``) has any spar wrecked or sent down.

Helpers
    ``deg(30)`` turns degrees into radians (all angles inside the engine are
    radians); ``knots(2)`` turns knots into metres per second; ``abs``,
    ``min``, ``max``, ``clamp(x, lo, hi)``; ``tack_sign(side)`` is +1 for
    starboard, -1 for larboard, and the ship's current tack when ``side``
    is ``none``; ``close_hauled()`` is true when the apparent wind is within
    ten degrees of the ship's close-hauled angle; ``any_set(sails)`` is true
    when any sail in a list is set and drawing.

Operators
    Comparisons ``==  !=  <  <=  >  >=``, membership ``x in [a, b]`` and
    ``x not in [a, b]``, the logic words ``and``, ``or``, ``not``, the
    arithmetic ``+ - * /`` and a leading minus, and parentheses.

What it may not contain
    Assignment, function definitions, indexing, method calls, attribute
    writes, or any name not listed above. Setting a value is done by the
    runner, which takes the *target* of a ``sets:`` or ``ramp:`` entry
    (``sail.state``, ``yard.brace_angle``, ``halyard_of(sail).hauled``) as
    an expression for the object plus one attribute name, and assigns to
    that attribute itself.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class ExpressionError(ValueError):
    """An expression that cannot be read or evaluated. The message is a sentence."""


# ---------------------------------------------------------------------------
# Tokens
# ---------------------------------------------------------------------------

_TOKEN = re.compile(
    r"""
    (?P<ws>\s+)
  | (?P<num>\d+\.\d*|\.\d+|\d+)
  | (?P<str>'[^']*'|"[^"]*")
  | (?P<name>[A-Za-z_][A-Za-z0-9_]*)
  | (?P<op>==|!=|<=|>=|[<>()\[\],.+\-*/])
    """,
    re.VERBOSE,
)

Token = tuple[str, str]  # (kind, text); kinds: num, str, name, op, end

_KEYWORDS = {"and", "or", "not", "in"}


def tokenize(text: str) -> list[Token]:
    out: list[Token] = []
    pos = 0
    while pos < len(text):
        m = _TOKEN.match(text, pos)
        if m is None:
            raise ExpressionError(f"Cannot read '{text}': unexpected character {text[pos]!r}.")
        pos = m.end()
        kind = m.lastgroup
        if kind == "ws":
            continue
        value = m.group(kind)
        if kind == "name" and value in _KEYWORDS:
            kind = "op"
        out.append((kind, value))
    out.append(("end", ""))
    return out


# ---------------------------------------------------------------------------
# Parser: text -> tree. A tree node is a tuple whose first item is its kind.
# ---------------------------------------------------------------------------

Node = tuple


class _Parser:
    def __init__(self, text: str):
        self.text = text
        self.tokens = tokenize(text)
        self.i = 0

    # helpers
    def peek(self) -> Token:
        return self.tokens[self.i]

    def take(self) -> Token:
        tok = self.tokens[self.i]
        self.i += 1
        return tok

    def accept(self, op: str) -> bool:
        kind, value = self.peek()
        if kind == "op" and value == op:
            self.i += 1
            return True
        return False

    def expect(self, op: str) -> None:
        if not self.accept(op):
            kind, value = self.peek()
            found = "the end" if kind == "end" else repr(value)
            raise ExpressionError(f"Cannot read '{self.text}': expected '{op}' but found {found}.")

    # grammar, lowest precedence first
    def parse(self) -> Node:
        node = self.parse_or()
        if self.peek()[0] != "end":
            raise ExpressionError(
                f"Cannot read '{self.text}': unexpected {self.peek()[1]!r} after the expression."
            )
        return node

    def parse_or(self) -> Node:
        node = self.parse_and()
        while self.accept("or"):
            node = ("or", node, self.parse_and())
        return node

    def parse_and(self) -> Node:
        node = self.parse_not()
        while self.accept("and"):
            node = ("and", node, self.parse_not())
        return node

    def parse_not(self) -> Node:
        if self.accept("not"):
            return ("not", self.parse_not())
        return self.parse_comparison()

    def parse_comparison(self) -> Node:
        node = self.parse_additive()
        while True:
            kind, value = self.peek()
            if kind == "op" and value in ("==", "!=", "<", "<=", ">", ">="):
                self.take()
                node = ("cmp", value, node, self.parse_additive())
            elif kind == "op" and value == "in":
                self.take()
                node = ("in", node, self.parse_additive(), False)
            elif kind == "op" and value == "not":
                self.take()
                self.expect("in")
                node = ("in", node, self.parse_additive(), True)
            else:
                return node

    def parse_additive(self) -> Node:
        node = self.parse_multiplicative()
        while True:
            kind, value = self.peek()
            if kind == "op" and value in ("+", "-"):
                self.take()
                node = ("binop", value, node, self.parse_multiplicative())
            else:
                return node

    def parse_multiplicative(self) -> Node:
        node = self.parse_unary()
        while True:
            kind, value = self.peek()
            if kind == "op" and value in ("*", "/"):
                self.take()
                node = ("binop", value, node, self.parse_unary())
            else:
                return node

    def parse_unary(self) -> Node:
        if self.accept("-"):
            return ("neg", self.parse_unary())
        return self.parse_postfix()

    def parse_postfix(self) -> Node:
        node = self.parse_primary()
        while True:
            if self.accept("."):
                kind, value = self.take()
                if kind != "name":
                    raise ExpressionError(f"Cannot read '{self.text}': a name must follow '.'.")
                node = ("attr", node, value)
            elif self.accept("("):
                args: list[Node] = []
                if not self.accept(")"):
                    args.append(self.parse_or())
                    while self.accept(","):
                        args.append(self.parse_or())
                    self.expect(")")
                node = ("call", node, tuple(args))
            else:
                return node

    def parse_primary(self) -> Node:
        kind, value = self.take()
        if kind == "num":
            return ("num", float(value) if "." in value else int(value))
        if kind == "str":
            return ("str", value[1:-1])
        if kind == "name":
            return ("name", value)
        if kind == "op" and value == "(":
            node = self.parse_or()
            self.expect(")")
            return node
        if kind == "op" and value == "[":
            items: list[Node] = []
            if not self.accept("]"):
                items.append(self.parse_or())
                while self.accept(","):
                    items.append(self.parse_or())
                self.expect("]")
            return ("list", tuple(items))
        found = "the end" if kind == "end" else repr(value)
        raise ExpressionError(f"Cannot read '{self.text}': unexpected {found}.")


def parse(text: str) -> Node:
    """Read an expression into a tree. Raises ExpressionError if it cannot be read."""
    if not isinstance(text, str) or not text.strip():
        raise ExpressionError("An expression must be a non-empty piece of text.")
    return _Parser(text).parse()


def split_target(text: str) -> tuple[Node, str]:
    """Split a ``sets:``/``ramp:`` target such as ``yard.brace_angle`` into
    (expression for the object, attribute name)."""
    tree = parse(text)
    if tree[0] != "attr":
        raise ExpressionError(
            f"'{text}' cannot be set: a target must end in a dotted attribute "
            "such as sail.state or yard.brace_angle."
        )
    return tree[1], tree[2]


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

_CONSTANTS: dict[str, Any] = {"true": True, "false": False, "none": None}


class Env:
    """The names and functions an expression may use."""

    def __init__(self, names: dict[str, Any], functions: dict[str, Callable[..., Any]]):
        self.names = names
        self.functions = functions

    def lookup(self, name: str) -> Any:
        if name in self.names:
            return self.names[name]
        if name in _CONSTANTS:
            return _CONSTANTS[name]
        if name in self.functions:
            return _Function(name, self.functions[name])
        return name  # a bare word stands for itself, e.g. `furled`


class _Function:
    def __init__(self, name: str, fn: Callable[..., Any]):
        self.name = name
        self.fn = fn


def evaluate(tree: Node, env: Env) -> Any:
    """Walk a parsed tree and return its value."""
    kind = tree[0]
    if kind == "num" or kind == "str":
        return tree[1]
    if kind == "name":
        return env.lookup(tree[1])
    if kind == "list":
        return [evaluate(item, env) for item in tree[1]]
    if kind == "attr":
        obj = evaluate(tree[1], env)
        name = tree[2]
        if name.startswith("_"):
            raise ExpressionError(f"'{name}' is not a readable attribute.")
        if isinstance(obj, dict):
            return obj.get(name)
        if obj is None:
            return None
        if isinstance(obj, str):
            raise ExpressionError(
                f"'{obj}' is a word, not a part; it has no attribute '{name}'. "
                "Is the name spelt as the file binds it (sail, yard, spar, line)?"
            )
        try:
            value = getattr(obj, name)
        except AttributeError:
            raise ExpressionError(f"{type(obj).__name__} has no attribute '{name}'.") from None
        if callable(value):
            raise ExpressionError(f"'{name}' is a method; expressions may not call methods.")
        return value
    if kind == "call":
        fn = evaluate(tree[1], env)
        if not isinstance(fn, _Function):
            raise ExpressionError(f"'{fn}' is not a function an expression may call.")
        args = [evaluate(a, env) for a in tree[2]]
        try:
            return fn.fn(*args)
        except (TypeError, KeyError, AttributeError) as e:
            raise ExpressionError(f"{fn.name}(...) could not be evaluated: {e}") from None
    if kind == "not":
        return not evaluate(tree[1], env)
    if kind == "and":
        return evaluate(tree[1], env) and evaluate(tree[2], env)
    if kind == "or":
        return evaluate(tree[1], env) or evaluate(tree[2], env)
    if kind == "neg":
        return -evaluate(tree[1], env)
    if kind == "cmp":
        op, left, right = tree[1], evaluate(tree[2], env), evaluate(tree[3], env)
        return _compare(op, left, right)
    if kind == "in":
        left, right, negate = evaluate(tree[1], env), evaluate(tree[2], env), tree[3]
        if not isinstance(right, list | tuple | set):
            raise ExpressionError("The right side of 'in' must be a list such as [furled, set].")
        found = any(_equal(left, item) for item in right)
        return not found if negate else found
    if kind == "binop":
        op, left, right = tree[1], evaluate(tree[2], env), evaluate(tree[3], env)
        try:
            if op == "+":
                return left + right
            if op == "-":
                return left - right
            if op == "*":
                return left * right
            if right == 0:
                raise ExpressionError("Division by zero.")
            return left / right
        except TypeError:
            raise ExpressionError(f"Cannot apply '{op}' to {left!r} and {right!r}.") from None
    raise ExpressionError(f"Unknown expression node {kind!r}.")


def _equal(a: Any, b: Any) -> bool:
    # StrEnum members compare equal to their text, so `sail.state == furled` works.
    return a == b


def _compare(op: str, a: Any, b: Any) -> bool:
    if op == "==":
        return _equal(a, b)
    if op == "!=":
        return not _equal(a, b)
    try:
        if op == "<":
            return a < b
        if op == "<=":
            return a <= b
        if op == ">":
            return a > b
        return a >= b
    except TypeError:
        raise ExpressionError(f"Cannot compare {a!r} {op} {b!r}.") from None


def evaluate_text(text: str, env: Env) -> Any:
    """Convenience: parse and evaluate in one call."""
    return evaluate(parse(text), env)
