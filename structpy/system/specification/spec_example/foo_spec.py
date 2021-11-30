
"""
Collection of items that can be enumerated.
"""

import structpy.system.specification.spec as spec


@spec.init
def __init__(Iterable, items):
    """
    Documentation for constructor.
    """
    return Iterable([2, 'a', True])

@spec.unit(sub=__init__, init=True)
def copy(Iterable, iterable):
    """
    Hidden beneath __init__ (subtest, automatically
    a @spec.init test because parent is @spec.init)
    """
    pass

@copy.sub
def copy_empty(Iterable, iterable):
    """
    Hidden beneath _copy.
    """
    pass

@spec.sub(__init__)
def default(Iterable):
    """
    Hidden beneath __init__.
    """
    pass

def method(iterable, params):
    """
    Documentation for method.
    """
    assert iterable.method()

def _subtest(iterable):
    """
    Documentation for test.
    """
    assert iterable.method() == True

def test(data_structure, params):
    """
    Documentation for method.
    """
    assert data_structure.test()

@spec.satisfies(__init__)
def another_way(Iterable):
    return Iterable()


