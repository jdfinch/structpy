import sys
from inspect import ismodule, getmembers, isfunction, getmodule

from structpy.system.specification.unit_test import UnitTest
from structpy.system.printer import Printer, capture_stdout


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
        condition = self._condition(condition)
        results = []
        printer = Printer('bold')
        for unit in self:
            if condition(unit):
                if output:
                    printer(f'{unit.name}:')
                stdout_cap = capture_stdout(silence=not output, indent=True)
                with stdout_cap:
                    result = unit.run(output=output)
                    results.append(result)
                if output:
                    printer()
        report = Report(results)
        if output:
            report.display()
        return report

    def _condition(self, condition):
        if condition is None:
            return lambda _: True
        elif callable(condition):
            return condition
        elif hasattr(condition, '__contains__'):
            return lambda x: x in condition
        else:
            return lambda _: condition

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

    @property
    def summary(self):
        succeeded = len(self.successful)
        failed = len(self.failed)
        time = f'{self.timedelta:.5f}s'
        return f'{succeeded} succeeded, {failed} failed in {time}'

    @property
    def timedelta(self):
        return sum((result.timedelta for result in self.results))

    def display(self):
        printer = Printer()
        fullcolor = {**{not self.successful: 'red'}, **{not self.failed: 'green'}}.get(True)
        with printer.mode('bold', end='', fg=fullcolor):
            if self.successful:
                printer.mode('green')(len(self.successful), 'succeeded')
            if self.failed:
                if self.successful:
                    printer(', ')
                printer.mode('red')(len(self.failed), 'failed')
            printer(f' in {self.timedelta:.5f}s')


    def __iter__(self):
        return iter(self.results)

    def __len__(self):
        return len(self.results)

    def __getitem__(self, item):
        return self.results[item]

    def __str__(self):
        return f'Report({", ".join((str(r) for r in self))})'



if __name__ == '__main__':

    def foo():
        print('testing foo')
        assert True

    def bat():
        print('testing bat')
        assert True

    def baz():
        print('testing baz')
        assert True

    tests = TestList(foo, bat, baz)
    tests.run()