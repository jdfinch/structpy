
from inspect import signature, Parameter, ismodule, getmembers, isfunction, getmodule
from copy import deepcopy

from structpy.system.specification.unit_test import UnitTest
from structpy.system.dclass import Dclass
from structpy.system.printer import capture_stdout, capture_stderr


class TestList(list):
    """

    """

    def __init__(self, *units):
        list.__init__(self)
        for unit in units:
            if ismodule(unit):
                self.extend(unit)
            else:
                self.append(unit)

    def run(self, output=True, condition=None):
        results = []
        for unit in self:
            if not condition or condition(unit):
                if output:
                    print(unit)
                stdout_cap = capture_stdout(silence=not output, indent=True)
                stderr_cap = capture_stderr(silence=True)
                with stdout_cap, stderr_cap:
                    result = unit.run()
                    results.append(result)
        report = Report(results)
        if output:
            print(report)
        return report

    def bind(self, *args, **kwargs):
        for unit in self:
            unit.try_bind_default(*args, **kwargs)
        return self

    def unbind(self):
        for unit in self:
            unit.unbind()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unbind()

    def append(self, item):
        list.append(self, None)
        self[-1] = item

    def extend(self, iterable):
        if ismodule(iterable):
            iterable = [
                f for f in getmembers(iterable)
                if isfunction(f) and getmodule(f) is iterable
            ]
        for item in iterable:
            self.append(item)

    def insert(self, index, item):
        list.insert(self, index, None)
        self[index] = item

    def __setitem__(self, key, value):
        unit = value if isinstance(value, UnitTest) else UnitTest(value)
        list.__setitem__(self, key, unit)


class Report:

    def __init__(self, results):
        self.results = tuple(results)
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

