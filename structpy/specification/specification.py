
import inspect, importlib, copy

from structpy.specification.unit_test import UnitTest
from structpy.specification.default_binder import DefaultBinder


class Spec:

    def __init__(self, module_name=None, tests=(), implementations=(), params=None, doc=''):
        if not module_name:
            module_name = inspect.currentframe().f_back.__module__
        self.module = importlib.import_module(module_name)
        self.parameters = {} if params is None else dict(params)
        self.tests = []
        self.implementations = []
        for test in tests:
            self.test(test)
        for implementation in implementations:
            self.implementation(implementation)
        self.params = Spec.ParameterContextManager(self)

    def implementation(self, *args, **kwargs):
        if args or kwargs:
            self.implementations.append((args, kwargs))
            if args:
                return args[0]
        else:
            return self.implementation

    def test(self, test):
        if not isinstance(test, UnitTest):
            test = UnitTest(test)
        self.tests.append(test)
        return test

    def __enter__(self):
        self._preexisting_globals = set(self.module.__dict__)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        new_globals = {
            k: v for k, v in self.module.__dict__.items()
            if k not in self._preexisting_globals
        }
        for name, value in new_globals.items():
            if inspect.isfunction(value) and name not in self.parameters:
                self.test(value)
            else:
                self.parameters[name] = value

    class ParameterContextManager:

        def __init__(self, spec):
            self.spec = spec

        def __enter__(self):
            self._preexisting_globals = set(self.spec.module.__dict__)
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            new_globals = {
                k: v for k, v in self.spec.module.__dict__.items()
                if k not in self._preexisting_globals
            }
            for name, value in new_globals.items():
                self.spec.parameters[name] = value

    def run(self, output=True):
        for (args, kwargs) in self.implementations:
            binder = DefaultBinder(self.parameters)
            _, arguments = binder(*args, **kwargs)
            for test in self.tests:
                arguments_copy = copy.deepcopy(arguments)
                for name, value in arguments_copy:
                    setattr(self.module, name, value)
                with test.try_bind_default(**arguments_copy):
                    test.run(output)
                for name, value in arguments_copy:
                    if getattr(self.module, name) is not value:
                        arguments[name] = getattr(self.module, name)

if __name__ == '__main__':
    ...


