
from inspect import getmodule

import structpy.system.specification.spec as specification


class Unit:

    units = {}

    def __new__(cls, f, spec=None, init=None, tags=None, satisfies=None, property=None, subunits=None):
        if f in Unit.units:
            unit = Unit.units[f]
            if spec is not None:
                unit.spec = spec
            if init is not None:
                unit.init = init
            if tags:
                unit.tags.update(tags)
            if satisfies is not None:
                unit.satisfies = satisfies
            if property is not None:
                unit.property = property
            if subunits:
                unit.subunits.extend(subunits)
        else:
            if property is None:
                property = False
            if init is None:
                init = False
            return super(Unit, cls).__new__(cls, f, init, spec, tags, satisfies, property, subunits)

    def __init__(self, f, init=False, spec=None, tags=None, satisfies=None, property=False, subunits=None):
        if f in Unit.units:
            return
        else:
            self.f = f
            self.spec = specification.Spec(getmodule(self.f) if spec is None else spec)
            self.init = init
            self.tags = set() if not tags else set(tags)
            self.satisfies = satisfies
            self.property = property
            self.subunits = [] if not subunits else list(subunits)
            self.spec = spec
            Unit.units[self.f] = self

    def verify(self, implementation=None):
        raise NotImplementedError


def unit(*tags, init=None, satisfies=None, property=None):
    def decorator(f):
        if f in Unit.units:
            unit = Unit.units[f]
            unit.tags.update(tags)
            if satisfies is not None:
                unit.satisfies = satisfies
            if property is not None:
                unit.property = property
        else:
            Unit(f, init=(init if init is not None else False),
                 tags=tags, satisfies=satisfies,
                 property=(property if property is not None else False))
        return f
    return decorator

def tags(*tags):
    def decorator(f):
        Unit(f, tags=tags)
        return f
    return decorator

def satisfies(unit):
    def decorator(f):
        Unit(f, satisfies=unit)
        return f
    return decorator

def property(f):
    Unit(f)
    return f

def init(f):
    Unit(f, init=True)
