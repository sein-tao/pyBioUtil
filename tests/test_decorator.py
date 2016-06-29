#!/usr/bin/env python3
import unittest
TestCase = unittest.TestCase
from BioUtil.decorator import context_decorator
import inspect

print(__file__)

class TestContextDecorator(TestCase):
    def test_no_enter(self):
        with self.assertRaises(AttributeError):
            class A:
                pass
            with A() as input:
                pass

    def test_decorator_enter(self):
        # test no raise
        @context_decorator
        class A:
            def __init__(self):
                pass
        with A() as input:
            pass

    def test_decorator_enter_override(self):
        with self.assertRaises(NotImplementedError):
            @context_decorator
            class A:
                def __enter__(self):
                    raise NotImplementedError()
            with A() as input:
                pass


