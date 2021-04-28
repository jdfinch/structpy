
from inspect import getmembers, isfunction, signature, getmodule
import sys, traceback
from copy import deepcopy
from structpy.system.printer import Printer


class Verifier:

    def __init__(self):
        self.specs = {}         # {module: {constructor: [unit]}}
        self.log = Printer()

    def collect(self, spec):
        if spec in self.specs:
            return self.specs[spec]
        else:
            self.specs[spec] = {}
        functions = sorted(
            getmembers(spec, isfunction),
            key=lambda x:x[1].__code__.co_firstlineno
        )
        constructor = None
        for name, unit in functions:
            params = list(signature(unit).parameters.keys())
            if hasattr(unit, 'satisfies'):
                other = unit.satisfies
                othermod = getmodule(other)
                unitchain = self.specs.setdefault(othermod, self.collect(othermod))[other]
                self.specs[spec][unit] = unitchain
            if not params or isconstructor(unit):
                if isconstructor(unit):
                    constructor = unit
                self.specs[spec].setdefault(unit, [])
            else:
                self.specs[spec][constructor].append(unit)
        return self.specs[spec]

    def verify(self, types=None, spec=None, tags=None, verbosity=1):
        """
        Verify a specification defined by the module `spec`.
        """
        if not isinstance(types, list):
            types = [types]
        if spec is None:
            spec = sys.modules['__main__']
        for cls in types:
            results = []
            for constructor, units in self.specs.get(spec, self.collect(spec)).items():
                obj, success, report = self.execute(constructor, cls)
                results.append([(constructor, success, report)])
                for unit in units:
                    _, success, report = self.execute(unit, deepcopy(obj))
                    results[-1].append((unit, success, report))
            self.log(''.join(self.report(cls, results)))

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
            success = True
        except Exception:
            result = None
            tbmode = self.log.mode('red', file=None)
            report.append(tbmode(traceback.format_exc().strip()))
            success = False
        sys.stdout = stdout
        report = ''.join(report)
        return result, success, report

    def report(self, cls, results):
        reports = []
        with self.log.mode(file=None):
            successes = 0
            total = 0
            for resultchain in results:
                for unit, success, report in resultchain:
                    if success: successes += 1
                    total += 1
                    with self.log.mode('green' if success else 'red', 4):
                        reports.append(self.log.mode('bold')(displayname(unit)))
                        if report.strip():
                            with self.log.mode(4):
                                reports.append(self.log(report))
            with self.log.mode('green' if successes == total else 'red'):
                reports.append(self.log.mode('bold', end='  ')(cls.__name__))
                reports.append(self.log(f'{successes}/{total}'))
        return reports

    class satisfies:
        def __init__(self, spec_referent):
            self.spec_referent = spec_referent
        def __call__(self, spec_function):
            spec_function.satisfies = self.spec_referent
            return spec_function


def isconstructor(unit):
    params = list(signature(unit).parameters.keys())
    return params and params[0][0].isupper()

def isattribute(unit):
    return unit.__name__.startswith('o__')

def displayname(unit):
    if isattribute(unit):
        return '.' + unit.__name__[3:]
    else:
        return unit.__name__


spec = Verifier()