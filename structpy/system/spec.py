
from inspect import getmembers, isfunction, signature
import sys, traceback
from structpy.system.printer import Printer
from structpy.utilities import catches


class Verifier:

    def __init__(self):
        self.expected_error = None
        self.specs = {}
        self.success = True
        self.log = Printer()

    def collect(self, spec):
        units = []
        functions = sorted(
            getmembers(spec, isfunction),
            key=lambda x:x[1].__code__.co_firstlineno
        )
        for name, unit in functions:
            params = list(signature(unit).parameters.keys())
            if not params or params[0][0].isupper():
                units.append([unit])
            else:
                units[-1].append(unit)
        self.specs[spec] = units
        return units

    def verify(self, *types, spec=None, tags=None, verbosity=1):
        """
        Verify a specification defined by the module `spec`.
        """
        if spec is None:
            spec = sys.modules['__main__']
        if not types:
            types = [None]
        unitchains = self.specs.get(spec, self.collect(spec))
        for cls in types:
            for units in unitchains:
                constructor = units[0]
                obj = self.execute(constructor, cls)
                for unit in units[1:]:
                    self.execute(unit, obj)

    def execute(self, unit, arg=None):
        args = [None for _ in signature(unit).parameters.keys()]
        if args:
            args[0] = arg
        report = []
        stdout = sys.stdout
        sys.stdout = self.log
        self.success = True
        try:
            with self.log.mode(file=report):
                result = unit(*args)
                self.success = True
        except Exception as e:
            result = None
            if not self.success:
                report.append(self.log.mode('red', file=[])(traceback.format_exc()))
        sys.stdout = stdout
        self.expected_error = None
        with self.log.mode('green' if self.success else 'red'):
            self.log(unit.__name__)
        with self.log.mode(4):
            self.log(''.join(report))
        return result

    def raises(self, error):
        verifier = self
        class ErrorExpectation:
            def __init__(self, error_type):
                self.error = error_type
            def __enter__(self):
                verifier.expected_error = self.error
                return self
            def __exit__(self, exc_type, exc_val, exc_tb):
                if (exc_val is None and verifier.expected_error is not None) or \
                        not catches(verifier.expected_error, exc_val):
                    verifier.success = False
                    raise WrongException(verifier.expected_error, exc_val)
                verifier.expected_error = None
        return ErrorExpectation(error)


class WrongException(Exception):

    def __init__(self, expected, actual):
        self.expected = expected
        self.actual = actual
        Exception.__init__(self)

    def __str__(self):
        return f'Expected exception {self.expected} but {self.actual} raised.'

    def __repr__(self):
        return str(self)


spec = Verifier()