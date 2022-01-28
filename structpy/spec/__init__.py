
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


class Spec:

    def __init__(self, cls=None, *, instance=None, factory=None):
        pass

    def __call__(self, cls):
        return self

    def run_tests(self):
        return True

    def __getattribute__(self, item):
        return getattr(self, item)



__all__ = [
    'expecting',
    'Spec',
    'Protocol'
]


