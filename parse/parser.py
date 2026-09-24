#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import builtins
from itertokens import iter_tokens, Token
from node import Node, Num, Plus, Minus, Mul, Div


def next(tokens, default=None):
    tok = builtins.next(tokens, default)
    print(f"next {tok = }")
    return tok


class Parser:
    def __init__(self):
        self.tokens = None
        self.tok = None

    def expr(self):
        res: Node = self.term()
        while self.tok and self.tok.val in ("+", "-"):
            self._consume()
            right: Node = self.term()
            if self.tok.val == "+":
                res = Plus(res, right)
            else:
                res = Minus(res, right)
        return res

    def term(self) -> Node:
        res: Node = self.factor()
        while self.tok and self.tok.val in ("*", "/"):
            self._consume()
            right: Node = self.factor()
            if self.tok.val == "*":
                res = Mul(res, right)
            else:
                res = Div(res, right)
        return res

    def factor(self) -> Node:
        if self.tok.name == "LPAREN":
            self._consume()
            res = self.expr()
            self._expect("RPAREN")
        else:
            res = Num(float(self.tok.val))
            self._consume()
        return res

    def parse(self, sexpr: str) -> Node:
        self.tokens = iter_tokens(sexpr)
        self._advance()
        return self.expr()

    def _advance(self) -> Token:
        self.tok = next(self.tokens, None)
        return self.tok

    def _consume(self) -> None:
        self.tok = next(self.tokens, None)

    def _expect(self, expected: str) -> None:
        if self.tok.name != expected:
            raise SyntaxError(f"{self.tok}: expected {expected}")
        self._consume()


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    p = Parser()
    p.parse(sexpr)
    print(p)
