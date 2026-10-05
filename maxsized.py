#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from abc import ABC, abstractmethod
import pytest


class Validator(ABC):
    def __init__(self, **kwargs):
        # for k, v in kwargs.items():
        #     setattr(self, k, v)
        pass

    def __set_name__(self, owner, name):
        self._name = f"sys_{name}"

    @abstractmethod
    def validate(self, instance, val):
        pass

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self._name)

    def __set__(self, instance, val):
        self.validate(instance, val)
        setattr(instance, self._name, val)


class Typed(Validator):
    def validate(self, instance, val):
        if not isinstance(val, self.expected):
            raise TypeError(f"{val}: must be of type {self.expected}")


class Unsigned(Validator):
    def validate(self, instance, val):
        if val < 0:
            raise ValueError(f"{val} must be positive")


class Integer(Typed):
    expected = int


class Float(Typed):
    expected = float


class String(Typed):
    expected = str


class SizedString(String):
    def __init__(self, size=8):
        super().__init__()
        self.size = size

    def validate(self, instance, val):
        super().validate(instance, val)
        if len(val) > self.size:
            raise ValueError(f"{val}: must have {self.size} chars or less")


class UnsignedInteger(Integer, Unsigned):
    def validate(self, instance, val):
        super().validate(instance, val)
        super(Typed, self).validate(instance, val)


class UnsignedFloat(Float, Unsigned):
    pass


class Stock:
    name = SizedString(size=8)
    shares = UnsignedInteger()
    price = UnsignedFloat()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def __repr__(self):
        return f"Stock({self.name}, {self.shares}, {self.price})"


def test_unsignedinteger():
    s = Stock("ACME", 90, 123.4)
    assert s.shares == 90
    with pytest.raises(TypeError, match="90.0: must be of type <class 'int'>"):
        s.shares = 90.0
    with pytest.raises(ValueError, match="-30 must be positive"):
        s.shares = -30


def test_string():
    s = Stock("ACME", 90, 123.4)
    assert s.name == "ACME"
    with pytest.raises(TypeError, match="401: must be of type <class 'str'>"):
        s.name = 401
    with pytest.raises(ValueError, match="ABRACADABRA: must have 8 chars or less"):
        s.name = "ABRACADABRA"


def test_stock():
    s = Stock("ACME", 90, 123.4)
    print(s)


if __name__ == "__main__":
    test_stock()
