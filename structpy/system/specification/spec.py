
from inspect import getmembers, isfunction, ismodule

from structpy.system.conditional_singleton import ConditionalSingleton
from structpy.system.dclass import dclass
from structpy.system.specification.unit_test import UnitTest


class Spec(ConditionalSingleton):
    """
    Spec is a Tranformation of a python module (or list of functions)
    into a documented test suite.
    """

    def __init__(self, module=None, units=None):
        """
        module (python module) Returns previously constructed Spec if the
        module has already been transformed into a Spec object.

        units (list<function>)
        """
        self._units = []
        self._implementations = []
        self._module = module
        if module:
            self.add(module)
        if units:
            self.add(units)

    def add(self, units, init=None):
        """
        Add tests to the Spec.

        units (list<(function, UnitTest)>, python module, function, UnitTest)

        init (UnitTest) an init function constructing objects to be passed to all
        tests in units at test time.
        """
        if isfunction(units):
            units = [units]
        elif ismodule(units):
            lineno = lambda x: x[1].__code__.co_firstlineno
            units = list(zip(*sorted(getmembers(units, isfunction), key=lineno)))[1]
        elif isinstance(units, Spec):
            units = list(units._units)
        else:
            units = list(units)
        for unit in units:
            if not isinstance(unit, UnitTest):
                unit = UnitTest(unit, self)
            if unit.init and not unit.under:
                init = unit
            else:
                if unit.under:
                    self._subunits[unit.under].append(unit)
                if init:
                    self._units[init].append(unit)
            self._units[unit] = []
            self._subunits[unit] = []
            if unit.satisfies:
                spec = unit.satisfies.spec
                if not spec:
                    spec = Spec(unit.satisfies.f.__module__)
                self.add(spec, init=init)

    def units(self):
        """
        return (list<UnitTest>) in test-order.
        """
        result = []
        visited = set()
        for initunit, chain in self._units:
            for unit in [initunit] + chain:
                if unit not in visited:
                    visited.add(unit)
                    result.append(unit)
                    superunits = list(self._subunits[unit])
                    while superunits:
                        superunit = superunits.pop()
                        if superunit not in visited:
                            visited.add(superunit)
                            result.append(superunit)
                            superunits.extend(self._subunits[superunit])
        return result

    def __iter__(self):
        return iter(self.units())

    def verify(self, *implementations, report=None):
        report = report or Report()
        implementations = implementations or self._implementations or [None]
        for implementation in implementations:
            init = None
            num = None
            for unit in self:
                if unit.init and implementation is not None:
                    success, init, time, msg, err_msg = unit.verify(implementation)
                    num = unit.init
                elif init is None or implementation is None:
                    success, _, time, msg, err_msg = unit.verify()
                else:
                    if isinstance(num, int) and num > 1:
                        success, _, time, msg, err_msg = unit.verify(*init)
                    else:
                        success, _, time, msg, err_msg = unit.verify(init)
                report.add_result(implementation, self, unit, success, time, msg, err_msg)
        return report

    @property
    def name(self):
        return self._module.__name__

