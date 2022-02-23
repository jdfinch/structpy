
from typing import Protocol


class expecting:

    def __init__(self, expected_error=Exception):
        self.expected_error = expected_error

    def __enter__(self): pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            raise exc_type
        except self.expected_error:
            return True
        except:
            return False


class SpecMeta:

    @classmethod
    def __getitem__(cls, item):
        def dec(f):
            return f
        return dec


class Spec(metaclass=SpecMeta):

    @staticmethod
    def subtest(f):
        return f


class detail:
    def __init__(self, header: str=None):
        self.header = header
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return

class testing(detail): pass

class spec:

    Spec = Spec
    details = detail


__all__ = [
    'expecting',
    'Spec',
    'detail',
    'testing',
    'spec',
    'Protocol'
]


