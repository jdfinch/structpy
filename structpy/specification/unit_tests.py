
from structpy.specification.unit_test import UnitTest


class UnitTests:
    """
    Collection of UnitTest objects representing a batch of tests to run against implementation code.
    """

    def __init__(self, constructors=None, /, **params):
        self.units = []
        self.params = {**params}
        self.constructors = list(constructors) if constructors else []

    def add_unit(self, unit, is_constructor=False):
        if not isinstance(unit, UnitTest):
            unit = UnitTest(unit)
        self.units.append(unit)
        if is_constructor:
            self.constructors.append(unit)

    def add_constructor(self, constructor):
        self.constructors.append(constructor)

    def set(self, **vars):
        self.params.update(vars)

    def run(self, output=False):
        results = []
        for unit in self.units:
            for constructor in self.constructors:
                constructor.run()
            with unit.try_bind_default():
                result = unit.run(output)
                results.append(result)
        return results


if __name__ == '__main__':

    def foo():
        print('foo run')
        assert True

    def bar():
        print('bar run')
        assert False

    def bat():
        print('bat run')
        assert True

    unit_tests = UnitTests()

