#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# import builtins
from itertokens import iter_tokens, Token
import operator
from node import Node, Num, Binary, Plus, Minus, Mul, Div


# def next(tokens, default=None):
#     tok = builtins.next(tokens, default)
#     print(f"next {tok = }")
#     return tok


class Parser:
    def __init__(self):
        self.tokens = None
        self.tok = None

    def expr(self):
        res: Node = self.term()
        while self.tok and (op := self.tok.val) in ("+", "-"):
            self._consume()
            right: Node = self.term()
            if op == "+":
                res = Plus(res, right)
            else:
                res = Minus(res, right)
        return res

    def term(self) -> Node:
        res: Node = self.factor()
        while self.tok and (op := self.tok.val) in ("*", "/"):
            self._consume()
            right: Node = self.factor()
            if op == "*":
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


def num_eval(self) -> float:
    return self.val


def binary_eval(self) -> float:
    return self._op(self.left.eval(), self.right.eval())


Num.eval = num_eval
Binary.eval = binary_eval
Plus._op = operator.add
Minus._op = operator.sub
Mul._op = operator.mul
Div._op = operator.truediv

if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    p = Parser()
    n: None = p.parse(sexpr)
    print(n)
    print(n.eval())
