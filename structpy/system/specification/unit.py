
from time import time
from inspect import signature

from structpy.system.defaulted import Defaulted


class Unit(Defaulted):

    defaults = {
        'init': False,
        'tags': set,
        'satisfies': False,
        'property': False
    }

    def __init__(self, f, spec=None, init=None, tags=None, satisfies=None, property=None, under=None):
        self.f = f
        self.sig = signature(self.f)
        self.spec = spec
        self.init = init
        self.tags = tags
        self.satisfies = satisfies
        self.property = property
        self.under = under

    def verify(self, *args, **kwargs):
        ti = None
        try:
            binding = self.sig.bind_partial(*args, **kwargs)
            binding.apply_defaults()
            fullbinding = {**{k: None for k in self.sig.parameters}, **binding.arguments}
            ti = time()
            result = self.f(**fullbinding)
            return True, result, ti or (time() - ti)
        except Exception:
            return False, None, ti or (time() - ti)


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
