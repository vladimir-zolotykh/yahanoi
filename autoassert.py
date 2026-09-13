#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from functools import wraps
from inspect import signature, _empty


def autoassert(func):
    sig = signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for name, parm in sig.parameters.items():
            if parm.annotation is not _empty:
                assert isinstance(
                    bound.arguments[name], parm.annotation
                ), f"{name!r}: type mismatch, expected {parm.annotation!r}"
        res = func(*args, **kwargs)
        return res

    return wrapper
