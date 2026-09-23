#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator
import re
from typeguard import typechecked


class Token:
    @typechecked
    def __init__(self, name: str, val: str | float):
        self.name = name
        self.val = val

    def __repr__(self):
        return f"Token({self.name}, {self.val!r})"


TOKENS = {
    "PLUS": r"\+",
    "MINUS": r"-",
    "MUL": r"\*",
    "DIV": r"/",
    "LPAREN": r"\(",
    "RPAREN": r"\)",
    "WS": r"\s+",
    "NUM": r"\d+",
    "NAME": r"[A-Za-z_]\w*",
}
PATTERNS = {key: rf"(?P<{key}>{val})" for key, val in TOKENS.items()}


def iter_tokens(sexpr: str) -> Iterator[Token]:
    masterpat = "|".join(PATTERNS.values())
    for match in re.finditer(masterpat, sexpr):
        tok = Token(match.lastgroup, match.group(0))
        if tok.name != "WS":
            yield tok


if __name__ == "__main__":
    for tok in iter_tokens("2 + (3 * 4) + 5"):
        print(tok)
