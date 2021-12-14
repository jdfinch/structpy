
from inspect import signature, getmembers, getmodule, isfunction, ismodule
from copy import deepcopy
from functools import partial
from pkgutil import walk_packages

from structpy.system.specification.unit_test import UnitTest
from structpy.system.specification.report import Report
from structpy.system.printer import Printer, capture_stdout, capture_stderr

default = object()
orderedset = dict.fromkeys
IMP = '__imp__'


def iter_modules_recursive(*starts):
    for start in starts:
        for loader, module_name, is_pkg in walk_packages(start.__path__):
            module = loader.find_module(module_name).load_module(module_name)
            yield module

def collect_specs_and_imps(*modules):
    if not modules:
        modules = [sys.modules['__main__']]
    modules = orderedset(iter_modules_recursive(*modules))
    specs = [s for mod in modules if hasattr(mod, IMP) for s in getattr(mod, IMP)]
    return specs


def verify(*modules):
    results = []
    specs = collect_specs_and_imps(*modules)
    for s in specs:
        report = s.verify()
        results.append(report)
    return results

def imp(specification, implementation=None):
    if implementation is None:
        return partial(imp, specification)
    else:
        if not isinstance(specification, Spec):
            specification = Spec(specification)
        specification.imps.append(implementation)
        imp_mod = getmodule(implementation)
        if not hasattr(imp_mod, IMP):
            setattr(imp_mod, IMP, {})
        getattr(imp_mod, IMP).setdefault(specification)
        return specification

class Spec:

    def __init__(self, *units, imps=None):
        self.units = Spec._units_from(*units)
        self.imps = imps or []

    def verify(self, *imps, output=True, condition=None, summary=True):
        if not imps:
            imps = self.imps
        if not imps:
            imps = [None]
        if not condition:
            condition = lambda x: True
        printer = Printer() if output else None
        units = list(filter(condition, self.units))
        results = {}
        for imp in imps:
            if output and imp is not None:
                printer('\n')
                printer(imp, underline=True)
            copies = {unit.copy: None for unit in units}
            outputs = {}
            for unit in units:
                if imp is None:
                    unit.try_bind_default()
                elif unit.is_init:
                    unit.try_bind_default(imp)
                elif unit.ref and unit.ref in outputs:
                    unit.try_bind_default(outputs[unit.ref].result)
                elif unit.copy and unit.copy in outputs:
                    unit.try_bind_default(deepcopy(copies[unit.copy]))
                elif ((unit.ref and unit.ref not in outputs)
                or (unit.copy and unit.copy not in outputs)):
                    continue
                else:
                    unit.try_bind_default()
                if output:
                    printer(f'\n{unit.name}', bold=True)
                cap_out = capture_stdout(indent=True)
                cap_err = capture_stderr(silence=True)
                with cap_out, cap_err:
                    result = unit.run(output=output)
                    outputs[unit] = result
                    results[(imp, unit)] = result
                if unit in copies:
                    if unit.is_init:
                        copies[unit] = deepcopy(outputs[unit].result)
                    elif unit.ref:
                        copies[unit] = deepcopy(outputs[unit.ref].result)
                unit.unbind()
        report = Report(results.values())
        if summary:
            printer()
            report.display()
        return report


    class Unit(UnitTest):

        def __init__(self, unit,
                     is_init=default,
                     ref=default,
                     copy=default,
                     is_private=default,
                     sat=default):
            if isinstance(unit, UnitTest):
                unit = unit.function
            if isinstance(unit, Spec.Unit):
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

    @staticmethod
    def sat(other):
        def wrap(f):
            f.sat = other
            return f

        return wrap

    @staticmethod
    def _units_from(*functions_or_modules, start=None):
        result = []
        unit_list = Spec._spec_units(*functions_or_modules, start=start)
        getunders = lambda x: 0 if x.endswith('__') else (len(x) - len(x.lstrip('_')))
        init_param = None
        first_unit = None
        visited = {None}
        leveled_list = [(fn, getunders(fn.name) // 2) for fn in unit_list]
        for unit, parent, elder, level in Spec._familize(leveled_list):
            params = signature(unit.function).parameters
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
                sat_list = Spec._units_from(getmodule(sat), start=sat)
                sat, sat_list = sat_list[0], sat_list[1:]
                for sat_unit in sat_list:
                    if sat_unit.ref is sat:
                        sat_unit.ref = unit
                    if sat_unit.copy is sat:
                        sat_unit.copy = unit
                result.extend(sat_list)
        return result

    @staticmethod
    def _spec_units(*functions_or_modules, start=None):
        result = []
        for fom in functions_or_modules:
            if ismodule(fom):
                result.extend((Spec.Unit(f) for f in Spec._module_spec_functions(fom)))
            elif isinstance(fom, UnitTest):
                result.append(Spec.Unit(fom.function))
            else:
                result.append(Spec.Unit(fom))
        if start is not None:
            to_find, _ = next(((i, e) for i, e in enumerate(result) if e.function is start))
            try: result = result[to_find:]
            except ValueError: result = []
        return result

    @staticmethod
    def _module_spec_functions(module):
        is_valid_function = lambda m: isfunction(m) and (getmodule(m) is module)
        members = list(zip(*getmembers(module, predicate=is_valid_function)))[1]
        ordered_members = sorted(members, key=lambda f: f.__code__.co_firstlineno)
        return ordered_members

    @staticmethod
    def _familize(ls):
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

    def foo(List, blah):
        ls = List((1, 2, 3))
        return ls

    def bar(l):
        print(l)
        assert sum(l) == 6

    def __bat(l):
        l.append(4)
        print(l)
        assert sum(l) == 10

    def __bak(l):
        l.append(9)
        print(l)

    def baz(l):
        l.append(5)
        print(l)
        assert sum(l) == 11

    def bam(List):
        print(List((4, 5, 6)))

    @Spec.sat(foo)
    def sats(List):
        l = List([1, 2])
        print(l)
        l.append(3)
        return l


    import sys
    spec = Spec(sys.modules[__name__])
    spec.imp(list)
    spec.imp(set)
    spec.verify()