
from inspect import getmembers, isfunction, getmodule, signature
from structpy.language.printer.printer import Printer
import sys, traceback


class Verifier:

    def __init__(self):
        self.expected_errors = [None]
        self.specs = {}
        self.report = []
        self.log = Printer()

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
        try:
            with self.log.mode(file=report):
                result = unit(*args)
                success = self.expected_error is None
        except Exception as e:
            result = None
            success = isinstance(e, type(self.expected_error))
            report.append(self.log.mode('red', file=[])(traceback.format_exc()))
        sys.stdout = stdout
        with self.log.mode('green' if success else 'red'):
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
                verifier.expected_errors.append(self)
                return self
            def __exit__(self, exc_type, exc_val, exc_tb):
                verifier.expected_errors.pop()
        return ErrorExpectation(error)


spec = Verifier()