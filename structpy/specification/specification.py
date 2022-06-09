
import inspect, importlib, copy

from structpy.specification.unit_test import UnitTest
from structpy.specification.default_binder import DefaultBinder


class Spec:

    def __init__(self, namespace=None, tests=(), implementations=(), params=None, doc=''):
        if not namespace:
            namespace = inspect.getmodule(inspect.currentframe().f_back)
            assert namespace is not None
        elif isinstance(namespace, str):
            namespace = importlib.import_module(namespace)
        self.namespace = namespace
        self.parameters = {} if params is None else dict(params)
        self.tests = []
        self.implementations = []
        for test in tests:
            self.test(test)
        for implementation in implementations:
            self.implementation(implementation)
        self.params = Spec.ParameterContextManager(self)

    def run(self, output=True):
        results = []
        implementations = self.implementations
        if not implementations:
            implementations = [((), {})]
        for (args, kwargs) in implementations:
            binder = DefaultBinder(self.parameters)
            _, arguments = binder.arguments(*args, **kwargs)
            for test in self.tests:
                arguments_copy = copy.deepcopy(arguments)
                for name, value in arguments_copy.items():
                    setattr(self.namespace, name, value)
                test.bind(**arguments_copy)
                result = test.run(output)
                results.append(result)
                for name, value in arguments_copy.items():
                    if getattr(self.namespace, name) is not value:
                        arguments[name] = getattr(self.namespace, name)
        return results

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
        self._preexisting_globals = set(self.namespace.__dict__)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        new_globals = {
            k: v for k, v in self.namespace.__dict__.items()
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
            self._preexisting_globals = set(self.spec.namespace.__dict__)
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            new_globals = {
                k: v for k, v in self.spec.namespace.__dict__.items()
                if k not in self._preexisting_globals
            }
            for name, value in new_globals.items():
                self.spec.parameters[name] = value



if __name__ == '__main__':
    ...


