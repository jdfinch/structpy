
from structpy.language.unit_test.unit import unit, Unit
from structpy.language.unit_test.unit_sequence import UnitSequence


def verify(spec, *args, **kwargs):
    return spec.__units__.test(*args, **kwargs)


def _rebuild(cls, prop_order):
    reorder = {}
    for item in prop_order:
        reorder[item] = cls.__dict__[item]
        delattr(cls, item)
    for k, v in reorder.items():
        setattr(cls, k, v)


def specification(cls):
    ordering = []
    for k, v in list(cls.__dict__.items()):
        if hasattr(v, '__call__'):
            ordering.append(k)
            if hasattr(v, 'unit_sequence'):
                for extra in v.unit_sequence:
                    setattr(cls, extra.__name__, extra)
                    ordering.append(extra.__name__)
    _rebuild(cls, ordering)
    units = UnitSequence([Unit(cls.__dict__[prop]) for prop in ordering])
    cls.__units__ = units
    cls.__verify__ = classmethod(verify)
    return cls


class satisfies:
    def __init__(self, other):
        self.other = other
    def __call__(self, f):
        f.unit_sequence = list(self.other.unit_sequence)
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

    foo.unit_sequence = [
        x, y
    ]

@specification
class B:

    hello = 'hello'

    def bar(self, x):
        """
        doc for bar
        """
        return x * 3

    @satisfies(A.foo)
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

    print()
    print(B.__verify__())
