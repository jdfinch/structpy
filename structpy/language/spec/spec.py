
from inspect import getmembers, isfunction, getmodule, signature


class Verifier:

    def __init__(self):
        self.expected_errors = [None]
        self.specs = {}
        self.report = []

    @property
    def expected_error(self):
        return self.expected_errors[-1]

    def collect(self, spec):
        units = []
        functions = sorted(
            getmembers(spec, isfunction),
            key=lambda x:x[1].__code__.co_firstlineno
        )
        for name, unit in functions:
            params = list(signature(unit).parameters.keys())
            if params and params[0][0].isupper():
                units.append([unit])
            else:
                units[-1].append(unit)
        self.specs[spec] = units

    def verify(self, spec, cls, tags=None, verbosity=1):
        """
        Verify a specification defined by the module `spec`.
        """
        unitchains = self.specs.get(spec, [])
        for units in unitchains:
            constructor = units[0]
            args = [None for _ in signature(constructor).parameters.keys()]
            args[0] = cls
            try:
                obj = units[0](*args)
                print(units[0].__name__, 'passed!')
            except Exception:
                obj = None
                print(units[0].__name__, 'failed!')
            for unit in units[1:]:
                args = [None for _ in signature(unit).parameters.keys()]
                args[0] = obj
                try:
                    unit(*args)
                    print(unit.__name__, 'passed!')
                except Exception:
                    print(unit.__name__, 'failed!')


    def raises(self, error):
        verifier = self
        class ErrorExpectation:
            def __init__(self, error_type):
                self.error = error_type
            def __enter__(self):
                verifier.expected_errors.append(self)
                return self
            def __exit__(self, exc_type, exc_val, exc_tb):
                verifier.expected_errors.pop()
        return ErrorExpectation(error)


if __name__ == '__main__':

    class MyClass:

        def __init__(self, a, b):
            self.a = a
            self.b = b

        def my_method(self, c):
            return self.a + self.b + 2

    from structpy.language.spec import spec_spec as s
    v = Verifier()
    v.collect(s)
    v.verify(s, MyClass)