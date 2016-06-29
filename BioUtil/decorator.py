#!/usr/bin/env python3 
import contextlib
import types
def context_decorator(cls):
    "decorator for class, add __enter__ and __exit__ method"
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        try: 
            self.close()
        finally:
            return
    default_attr = {
            '__enter__': __enter__,
            '__exit__': __exit__
            }
    for attr in default_attr.keys():
        if not hasattr(cls, attr):
            setattr(cls, attr, default_attr[attr])
    return cls

