
from inspect import signature, Parameter, ismodule, getmembers, isfunction, getmodule
from copy import deepcopy

from structpy.system.specification.unit_test import UnitTest
from structpy.system.dclass import Dclass


class TestCollection:
    """

    """

    def __init__(self, *units):
        self._units = {}
        self._tree = {}
        self.implementations = None
        self.add_spec(*units)

    def add_spec(self, *units, parent=None):
        for unit_ in units:
            if ismodule(unit_):
                self._add_module(unit_)
            else:
                self._add_unit(unit_, parent)

    def _add_module(self, module, parent=None):
        is_module_unit = (
            lambda x: isinstance(x, UnitTest) or (
                      isfunction(x)
                      and getmodule(x) is module
                      and not (hasattr(x, 'helper') and x.helper))
        )
        units = getmembers(module, is_module_unit)
        parents = [parent, None]
        for unit in units:
            hidden = False
            name = unit.name if isinstance(unit, UnitTest) else unit.__name__
            if name.startswith('__') and name.endswith('__'):
                level = 0
            else:
                level = len(name) - len(name.lstrip('_'))
                hidden = level == 1
            if level == len(parents):
                parents.append(unit)
                unit = self._add_unit(unit, parents[-2])
                unit.hidden = hidden
            elif level < len(parents):
                parents = parents[:max(level, 2)]
                unit = self._add_unit(unit, parents[-2])
                unit.hidden = unit

    def _add_unit(self, unit, parent=None):
        if not isinstance(unit, UnitTest):
            unit = UnitTest(unit)
            self._units[unit] = unit
        parent_unit = self._units.get(parent, parent)
        self._tree.setdefault(parent_unit, []).append(unit)
        return unit

    def add_imp(self, implementation):
        if self.implementations is None:
            self.implementations = []
        self.implementations.append(implementation)

    def verify(self, implementation=None):
        if implementation is not None:
            return self._verify(implementation)
        elif self.implementations is not None:
            return [self._verify(imp) for imp in self.implementations]
        else:
            return self._verify()

    def _verify(self, implementation=None):
        results = []
        factory_param = [None]
        instance = [None]
        delevel = object()
        stack = list(reversed(self._tree.get(None, [])))
        while stack:
            u = stack.pop()
            if u is delevel:
                del instance[-1]
                continue
            children = self._tree.get(u, [])
            if children:
                instance_copy = [deepcopy(instance[-1])]
            else:
                instance_copy = []
            params = [
                p.name for p in signature(u.bound_function).parameters.values()
                if p.kind not in {Parameter.VAR_KEYWORD, Parameter.KEYWORD_ONLY}
            ]
            if implementation is not None and params:
                implementation_param = params[0]
                if implementation_param == factory_param[0] or instance[-1] is None:
                    if factory_param[0] is None:
                        factory_param[0] = implementation_param
                    result = u.run(implementation)
                    instance[-1] = result.result
                else:
                    result = u.run(instance[-1])
            else:
                result = u.run()
            result.level = len(instance) - 1
            results.append(result)
            if instance_copy:
                instance.append(instance_copy[0])
            stack.append(delevel)
            stack.extend(reversed(children))
        return results


class Report(Dclass):

    def __init__(self, results, **kwargs):
        self.results = tuple(results)
        Dclass.__init__(self, **kwargs)
        self.successful = tuple((r for r in results if r.success))
        self.failed = tuple((r for r in results if not r.success))

    def __iter__(self):
        return iter(self.results)

    def __len__(self):
        return len(self.results)

    def __getitem__(self, item):
        return self.results[item]

    def __str__(self):
        return f'Report({", ".join((str(r) for r in self))})'

