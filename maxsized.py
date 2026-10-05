#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from abc import ABC, abstractmethod


class Validator(ABC):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __set_name__(self, owner, name):
        self._name = name

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
        if len > self.size:
            raise ValueError(f"{val}: must have {self.size} chars or less")


class UnsignedInteger(Integer, Unsigned):
    pass


class UnsignedFloat(Float, Unsigned):
    pass


class Stock:
    name = SizedString("name", size=8)
    shares = UnsignedInteger("shares")
    price = UnsignedFloat("price")

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price
