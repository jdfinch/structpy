
from inspect import signature, Parameter, ismodule, getmembers, isfunction, getmodule
from copy import deepcopy

from structpy.system.specification.unit_test import UnitTest
from structpy.system.dclass import Dclass


class TestList(list):
    """

    """

    def __init__(self, *units):
        list.__init__(self)
        self.extend(units)

    def run(self, *args, **kwargs):
        for unit in self:
            result = unit.run(*args, **kwargs)


    def append(self, item):
        list.append(self, None)
        self[-1] = item

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def insert(self, index, item):
        list.insert(self, index, None)
        self[index] = item

    def __setitem__(self, key, value):
        unit = value if isinstance(value, UnitTest) else UnitTest(value)
        list.__setitem__(self, key, unit)





class Report(Dclass):

    def __init__(self, results, **kwargs):
        self.results = tuple(results)
        Dclass.__init__(self, **kwargs)
        self.successful = tuple((r for r in results if r.success))
        self.failed = tuple((r for r in results if not r.success))

    def __iter__(self):
        return iter(self.results)

    def __len__(self):
        return len(self.results)

    def __getitem__(self, item):
        return self.results[item]

    def __str__(self):
        return f'Report({", ".join((str(r) for r in self))})'

