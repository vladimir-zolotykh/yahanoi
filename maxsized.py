#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from abc import ABC, abstractmethod


class Validator:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __set_name__(self, owner, name):
        self._name = name

    @abstractmethod
    def validate(self, instance, value):
        pass

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self._name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self._name, value)


class Typed(Validator):
    pass


class Unsigned(Validator):
    pass


class Integer(Typed):
    pass


class Float(Typed):
    pass


class String(Typed):
    pass


class SizedString(String):
    pass


class UnsignedInteger(Integer):
    pass


class UnsignedFloat(Float):
    pass


class Stock:
    # Specify constraints
    name = SizedString("name", size=8)
    shares = UnsignedInteger("shares")
    price = UnsignedFloat("price")

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price
