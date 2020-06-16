
from structpy.language.unit_test.unit import Unit
from structpy.language.unit_test.unit_sequence import UnitSequence
from structpy.language.unit_test.result_list import ResultList


def verify(spec, *args, **kwargs):
    return spec.__units__.test(*args, **kwargs)


class SpecificationUnitSequence(UnitSequence):

    def test(self):
        results = ResultList()
        arg = None
        for unit in self:
            result = unit.test(arg)
            obj = result.obj
            if obj is not None:
                arg = obj
            results.append(result)
        return results


def _rebuild(cls, prop_order):
    reorder = {}
    for item in prop_order:
        reorder[item] = cls.__dict__[item]
        delattr(cls, item)
    for k, v in reorder.items():
        setattr(cls, k, v)


def specification(cls):
    cls.__sequence__ = []
    sequenced = cls
    ordering = []
    for k, v in list(cls.__dict__.items()):
        if hasattr(v, '__call__'):
            ordering.append(k)
            if hasattr(v, 'is_ref'):
                for prop in v.__sequence__:
                    setattr(cls, prop.__name__, prop)
                    ordering.append(prop.__name__)
            if hasattr(v, 'is_init'):
                sequenced = v
            else:
                sequenced.__sequence__.append(v)
    _rebuild(cls, ordering)
    units = SpecificationUnitSequence()
    for method_name in ordering:
        method = cls.__dict__[method_name]
        unit = Unit(method, 'specification')
        units.append(unit)
    cls.__units__ = units
    cls.__verify__ = classmethod(verify)
    return cls


def init(f):
    f.is_init = True
    f.__sequence__ = []
    return f


class satisfies:
    def __init__(self, other):
        self.other = other
    def __call__(self, f):
        f = init(f)
        f.is_ref = True
        f.__sequence__ = list(self.other.__sequence__)
        return f


specification.satisfies = satisfies
specification.init = init


@specification
class A:

    @specification.init
    def foo(struct):
        return []

    def x(struct):
        """
        doc for x
        """
        struct.append(5)

    def y(struct):
        """
        doc for y
        """
        assert len(struct) == 1 and struct[0] == 5

@specification
class B:


    def bar(struct):
        """
        doc for bar
        """
        assert True

    @satisfies(A.foo)
    def baz(struct):
        """
        doc for baz
        """
        return []

    def bat(struct):
        """
        doc for bat
        """
        assert True

if __name__ == '__main__':

    print(B.__verify__())
