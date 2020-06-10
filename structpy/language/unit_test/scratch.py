
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