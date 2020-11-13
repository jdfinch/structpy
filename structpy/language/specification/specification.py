
from structpy.language.specification.unit import Unit
from structpy.language.specification.unit_sequence import UnitSequence
from structpy.language.specification.result_list import ResultList


def verify(spec, implementation=None):
    if implementation is None:
        results = ResultList()
        for implementation in spec.__implementations__:
            results += spec.__units__.test(implementation)
        return results
    else:
        return spec.__units__.test(implementation)


class SpecificationUnitSequence(UnitSequence):

    def test(self, implementation=None):
        results = ResultList()
        arg = None
        for unit in self:
            if hasattr(unit.method, 'is_init'):
                result = unit.test(implementation)
                arg = result.obj
            else:
                result = unit.test(arg)
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
    cls.verify = classmethod(verify)
    cls.__implementations__ = []
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


class implementation:

    def __init__(self, *specs):
        self.specifications = specs

    def __call__(self, cls):
        cls.__specifications__ = self.specifications
        for spec in self.specifications:
            spec.__implementations__.append(cls)
        return cls


@specification
class A:

    @specification.init
    def foo(struct):
        return struct([1, 2 ,3])

    def x(struct):
        """
        doc for x
        """
        struct.append(5)

    def y(struct):
        """
        doc for y
        """
        assert len(struct) == 4 and struct[-1] == 5

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
        return struct([3, 4, 4])

    def bat(struct):
        """
        doc for bat
        """
        assert 4 in struct
        assert 1 not in struct

@implementation(B)
class MyList(list):
    pass

if __name__ == '__main__':
    ml = MyList([1, 2, 3])
    print(B.verify(list))
