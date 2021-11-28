
from inspect import signature, getmembers, getmodule, isfunction, ismodule
from copy import deepcopy
from functools import lru_cache

from structpy.system.specification.unit_test import UnitTest
from structpy.system.dclass import Dclass
from structpy.system.specification.test_list import TestList, Report
from structpy.system.printer import Printer, capture_stdout, capture_stderr

default = object()


class Spec:

    pass


class Unit(UnitTest):

    def __init__(self, unit,
                 is_init=default,
                 ref=default,
                 copy=default,
                 is_private=default,
                 sat=default):
        if isinstance(unit, UnitTest):
            unit = unit.function
        if isinstance(unit, Unit):
            self.is_init = unit.is_init if is_init is default else is_init
            self.ref = unit.ref if ref is default else ref
            self.copy = unit.copy if copy is default else copy
            self.sat = unit.sat if sat is default else sat
            self.is_private = unit.is_private if is_private is default else is_private
        else:
            self.is_init = False if is_init is default else is_init
            self.ref = None if ref is default else ref
            self.copy = None if copy is default else copy
            self.sat = None if sat is default else sat
            self.is_private = False if is_private is default else is_private
        UnitTest.__init__(self, unit)


def units(*functions_or_modules, start=None):
    result = []
    unit_list = spec_units(*functions_or_modules, start=start)
    getunders = lambda x: 0 if x.endswith('__') else (len(x) - len(x.lstrip('_')))
    init_param = None
    first_unit = None
    visited = set()
    leveled_list = [(fn, getunders(fn.name) // 2) for fn in unit_list]
    for unit, parent, elder, level in familize(leveled_list):
        params = signature(unit).parameters
        param = next(iter(params)) if params else None
        unders = getunders(unit.name)
        unit.is_private = unders > 0
        is_continued = unders > 2 and unders % 2 == 1
        if not unit.is_private and init_param is None:
            init_param = param
        unit.is_init = param and param == init_param
        if not unit.is_init and elder and (is_continued or level == 0):
            unit.ref = elder if elder.is_init else elder.ref
        elif not unit.is_init and parent:
            unit.copy = parent
        if start:
            if first_unit is None:
                first_unit = unit
            elif unit.is_init or unit.ref not in visited or unit.copy not in visited:
                break
        visited.add(unit)
        result.append(unit)
        if hasattr(unit.function, 'sat'):
            sat = unit.function.sat
            sat_list = units(getmodule(sat), start=sat)[1:]
            for sat_unit in sat_list:
                if sat_unit.ref is sat:
                    sat_unit.ref = unit
                if sat_unit.copy is sat:
                    sat_unit.copy = unit
            result.extend(sat_list)
    return result


def spec_units(*functions_or_modules, start=None):
    result = []
    for fom in functions_or_modules:
        if ismodule(fom):
            result.extend((Unit(f) for f in module_spec_functions(fom)))
        elif isinstance(fom, UnitTest):
            result.append(Unit(fom.function))
        else:
            result.append(Unit(fom))
    if start is not None:
        try: result = result[result.index(start):]
        except ValueError: result = []
    return result


def module_spec_functions(module):
    is_valid_function = lambda m: isfunction(m) and (getmodule(m) is module)
    members = list(zip(*getmembers(module, predicate=is_valid_function)))[1]
    ordered_members = sorted(members, key=lambda f: f.__code__.co_firstlineno)
    return ordered_members


def familize(ls):
    path = []
    for item, level in ls:
        path = path[:level + 1]
        elder = None
        parent = None
        if len(path) > level:
            elder = path[level]
        if len(path) > level - 1 and level > 0:
            parent = path[level - 1]
        while level >= len(path):
            path.append(None)
        path[level] = item
        yield item, parent, elder, level



if __name__ == '__main__':
    pass