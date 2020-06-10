
import types
from structpy.language.unit_test.unit import unit
from structpy.language.unit_test.unit_sequence import UnitSequence

def verify(spec, *args, **kwargs):
    spec.__units__.test(*args, **kwargs)

def specification(cls):
    properties = []
    for k, v in cls.__dict__.items():
        if hasattr(v, '__call__') and v.__name__[0].isalpha():
            properties.append(v)
    units = UnitSequence([unit(prop) for prop in properties])
    cls.__units__ = units
    cls.__verify__ = verify
    return cls


def rebuild(cls, prop_order):
    reorder = {}
    for item in prop_order:
        reorder[item] = cls.__dict__[item]
        delattr(cls, item)
    for k, v in reorder.items():
        setattr(cls, k, v)


def my_dec(cls):
    ordering = []
    for k, v in list(cls.__dict__.items()):
        if hasattr(v, '__call__'):
            ordering.append(k)
            if hasattr(v, 'extras'):
                for extra in v.extras:
                    setattr(cls, extra.__name__, extra)
                    ordering.append(extra.__name__)
    rebuild(cls, ordering)
    return cls


class ref:
    def __init__(self, other):
        self.other = other
    def __call__(self, f):
        f.extras = self.other.extras
        return f


class A:

    def foo(self, x):
        return x * 2

    def x(self):
        """
        doc for x
        """
        return 'x'

    def y(self):
        """
        doc for y
        """
        return 'y'

    foo.extras = [
        x, y
    ]

@my_dec
class B:

    hello = 'hello'

    def bar(self, x):
        """
        doc for bar
        """
        return x * 3

    @ref(A.foo)
    def baz(self, x):
        """
        doc for baz
        """
        return x * 4

    def bat(self, x):
        """
        doc for bat
        """
        return 5

if __name__ == '__main__':

    print(B, '\n')
    for k, v in B.__dict__.items():
        print(k, v)
    print()
    print(B.bar(None, 4))
    print(B.baz(None, 4))
    print(B.x(None))
    print(B.y(None))
    print(B.bat(None, 4))
