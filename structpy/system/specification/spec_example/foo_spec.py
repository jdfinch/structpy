
"""
Collection of items that can be enumerated.
"""

import structpy.system.specification.spec as spec


def __init__(Iterable, items):
    """
    Documentation for constructor.
    """
    return Iterable([2, 'a', True])

def __default(Iterable):
    """
    Hidden beneath __init__.
    """
    pass

def copy(Iterable, iterable):
    """
    Hidden beneath __init__ (subtest, automatically
    a @spec.init test because parent is @spec.init)
    """
    return Iterable([1, 2, 3])

def __copy_empty(Iterable, iterable):
    """
    Hidden beneath _copy.
    """
    pass

def method(iterable, params):
    """
    Documentation for method.
    """
    assert iterable.method()

def __subtest(iterable):
    """
    Documentation for test.
    """
    assert iterable.method() == True

def test(data_structure, params):
    """
    Documentation for method.
    """
    assert data_structure.test()

@spec.sat(__init__)
def another_way(Iterable):
    return Iterable()


