
from inspect import signature, getmembers, getmodule, isfunction, ismodule
from copy import deepcopy
from functools import lru_cache

from structpy.system.specification.unit_test import UnitTest
from structpy.system.specification.test_list import TestList, Report
from structpy.system.printer import Printer, capture_stdout, capture_stderr


class Spec(TestList):

    def __init__(self, *units, imps=None):
        TestList.__init__(self, *Spec.units(*units))
        self.imps = imps

    def run(self, *imps, output=True, condition=None):
        if not imps:
            imps = self.imps
        if not imps:
            imps = [None]
        if not condition:
            condition = lambda x: True
        printer = Printer() if output else None
        units = list(filter(condition, self))
        copies = {unit.copy: None for unit in units}
        results = {}
        for imp in imps:
            for unit in units:
                if imp is None:
                    unit.try_bind_default()
                elif unit.is_init:
                    unit.try_bind_default(imp)
                elif unit.ref and unit.ref in results:
                    unit.try_bind_default(results[unit.ref].result)
                elif unit.copy and unit.copy in results:
                    unit.try_bind_default(deepcopy(copies[unit.copy]))
                elif ((unit.ref and unit.ref not in results)
                or (unit.copy and unit.copy not in results)):
                    continue
                else:
                    unit.try_bind_default()
                if output:
                    printer(f'\n{unit.name}', bold=True)
                cap_out = capture_stdout(indent=True)
                cap_err = capture_stderr(silence=True)
                with cap_out, cap_err:
                    result = unit.run(output=output)
                    results[unit] = result
                if unit in copies:
                    if unit.is_init:
                        copies[unit] = deepcopy(results[unit].result)
                    elif unit.ref:
                        copies[unit] = deepcopy(results[unit.ref].result)
                unit.unbind()
        return Report(results.values())

    @staticmethod
    @lru_cache(maxsize=None)
    def units(*units):
        result = []
        unit_list = []
        for unit in units:
            if ismodule(unit):
                unit_list.extend(utilities.functions_in(unit))
            elif isfunction(unit) :
                unit_list.append(unit)
            elif isinstance(unit, UnitTest):
                unit_list.append(unit.function)
            else:
                unit_list.extend(unit)
        all_units = unit_list
        init_param = None
        getunders = lambda x: 0 if x.endswith('__') else (len(x) - len(x.lstrip('_')))
        leveled_unit_list = [(unit, getunders(unit.__name__) // 2) for unit in all_units]
        family_sequence = utilities.familize(leveled_unit_list)
        fn_to_unit = {}
        for unit, parent, elder, level in family_sequence:
            params = signature(unit).parameters
            param = next(iter(params)) if params else None
            unders = getunders(unit.__name__)
            is_private = unders > 0
            is_continued = unders > 2 and unders % 2 == 1
            if not is_private and init_param is None:
                init_param = param
            is_init = param and param == init_param
            ref = None
            copy = None
            if not is_init:
                if elder and (is_continued or level == 0):
                    ref = elder
                elif parent:
                    copy = parent
            ref = fn_to_unit.get(ref)
            ref = ref if ref is None or ref.is_init else ref.ref
            copy = fn_to_unit.get(copy)
            unit = Spec.Unit(unit, is_init, ref, copy, is_private)
            fn_to_unit[unit.function] = unit
            result.append(unit)
        return result

    @staticmethod
    def sat(other):
        def wrap(f):
            f.sat = other
            return f
        return wrap

    class Unit(UnitTest):

        def __init__(self, unit, is_init=False, ref=None, copy=None, is_private=False):
            if isinstance(unit, UnitTest):
                unit = unit.function
            self.is_init = is_init
            self.ref = ref
            self.copy = copy
            self.sat = None
            self.is_private = is_private
            UnitTest.__init__(self, unit)


class utilities:

    @staticmethod
    def functions_in(module):
        is_valid_function = lambda m: isfunction(m) and (getmodule(m) is module)
        members = list(zip(*getmembers(module, predicate=is_valid_function)))[1]
        ordered_members = sorted(members, key=lambda f: f.__code__.co_firstlineno)
        return ordered_members

    @staticmethod
    def familize(sequence):
        result = []
        path = []
        for item, level in sequence:
            path = path[:level+1]
            elder = None
            parent = None
            if len(path) > level:
                elder = path[level]
            if len(path) > level - 1 and level > 0:
                parent = path[level - 1]
            while level >= len(path):
                path.append(None)
            path[level] = item
            result.append((item, parent, elder, level))
        return result


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
        assert sum(l) == 11

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
        l.append(3)
        return l


    import sys
    spec = Spec(sys.modules[__name__])
    report = spec.run(list)














