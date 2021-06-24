
from inspect import getmembers, isfunction, ismodule

from structpy.system.transformation import Transformation
from structpy.system.specification.unit import Unit


class Spec(Transformation):

    def __init__(self, module=None, units=None):
        self._units = {}
        self._subunits = {}
        self._implementations = []
        self._module = module
        if module:
            self.add(module)
        if units:
            self.add(units)

    def add(self, units, init=None):
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
            if not isinstance(unit, Unit):
                unit = Unit(unit, self)
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

    def verify(self, *implementations):
        for implementation in implementations or self._implementations or [tuple()]:
            base_init = implementation
            init = None
            for unit in self:
                unit.verify(*base_init)


    @property
    def name(self):
        return self._module.__name__
