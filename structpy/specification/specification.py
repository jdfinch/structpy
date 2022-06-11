
import inspect, importlib, copy
import sys

from structpy.specification.unit_test import UnitTest
from structpy.specification.default_binder import DefaultBinder
from structpy.system.printer import Printer, capture_stdout

spec_outline_print = Printer(bold=True)
imp_name_print = Printer(bold=True, indent=2)
test_name_print = Printer(bold=True, indent=2)


class Spec:

    def __init__(self, namespace=None, tests=(), implementations=(), params=None, doc=''):
        if not namespace:
            namespace = inspect.getmodule(inspect.currentframe().f_back)
            assert namespace is not None
        elif isinstance(namespace, str):
            namespace = importlib.import_module(namespace)
        else:
            namespace = importlib.import_module(namespace.__module__)
        assert not hasattr(namespace, '__specification__'), \
            f'Spec {namespace.__specification__} already defined on module {namespace}'
        namespace.__specification__ = self
        self.namespace = namespace
        self.parameters = {} if params is None else dict(params)
        self.tests = []
        self.implementations = []
        for test in tests:
            self.test(test)
        for implementation in implementations:
            self.implementation(implementation)
        self.params = Spec.ParameterContextManager(self)

    def run(self, *args, **kwargs):
        spec_outline_print('{:~^80}'.format(f' {self.name} '))
        spec_outline_print()
        all_results = []
        if args or kwargs:
            implementations = [(args, kwargs)]
        elif self.implementations:
            implementations = self.implementations
        else:
            implementations = [((), {})]
        for (args, kwargs) in implementations:
            results = []
            imp_header = ', '.join([
                *(str(arg) for arg in args),
                *(f'{kw}={arg}' for kw, arg in kwargs.items())
            ])
            imp_name_print('{:.^78}'.format(f' {imp_header} '))
            with capture_stdout(file=Printer(indent=2, file=sys.stdout)):
                binder = DefaultBinder(self.parameters)
                _, arguments = binder.arguments(*args, **kwargs)
                for test in self.tests:
                    arguments_copy = copy.deepcopy(arguments)
                    for name, value in arguments_copy.items():
                        setattr(self.namespace, name, value)
                    test.bind(**arguments_copy)
                    test_name_print(test.name)
                    with capture_stdout(file=Printer(indent=2, file=sys.stdout)):
                        result = test.run(output=True)
                    results.append(result)
                    for name, value in arguments_copy.items():
                        if getattr(self.namespace, name) is not value:
                            arguments[name] = getattr(self.namespace, name)
            all_results.extend(results)
            imp_name_print()
        passed = sum((1 for result in all_results if not result.error))
        failed = len(all_results) - passed
        if failed:
            spec_outline_print(
                f'{failed} failed, {passed} passed of {len(all_results)} tests for {self.name}',
                color='red'
            )
        else:
            spec_outline_print(f'all {passed} tests passed for {self.name}', color='green')
        spec_outline_print()
        spec_outline_print('~'*80)
        return all_results

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

    @property
    def name(self):
        return self.namespace.__name__


if __name__ == '__main__':
    ...


