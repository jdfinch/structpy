

import sys
import importlib
import pkgutil
from inspect import getmembers, isfunction, ismodule

pythonproperty = property

from structpy.system.specification.spec import Spec
from structpy.system.specification.report import Report
from structpy.system.specification.unit_test import *


implementations = {}
specifications = {}

def verify(*implementations_or_specs):
    """
    Return and print a Report describing whether given implementations
    meet their corresponding specifications.

    implementations_or_specs: implementations decorated with @spec.implements
                     OR modules/Specs, in which case implementations are
                     automatically discovered
    """
    imps, specs = collect(*implementations_or_specs)
    raise NotImplementedError

def collect(*implementations_or_specs):
    """
    Collect a group of implementations.

    implementations_or_specs: implementations decorated with @spec.implements
                     OR modules/Specs, in which case implementations are
                     automatically discovered

    returns: set of implementations
    """
    if not implementations_or_specs:
        implementations_or_specs = [sys.modules['__main__']]
    imps = []
    specs = []
    for implementation in implementations_or_specs:
        if implementation in implements.map:
            imps.append(implementation)
        elif ismodule(implementation) or isinstance(implementation, str):
            modules = import_submodules(implementation)
            for name, module in modules.values():
                if module in Spec.specs:
                    specs.append(Spec.specs[module])
                elif 'spec.py' in name:
                    specs.append(Spec(module))
        else:
            raise ValueError(f'Unknown implementation {implementation}')
    specs = [spec for spec in specs
             if not any([spec in implements.map[imp] for imp in imps])]
    return imps, specs


class implements:
    """
    Decorator marking some python object, class, module, or function
    as an implementation of some specification(s).

    Decorated implementations are registered as implementations of the
    provided specifications.
    """

    def __init__(self, *specs):
        self.specs = set(specs)

    def __call__(self, obj):
        implementations.setdefault(obj, set()).update(self.specs)
        for spec in self.specs:
            specifications.setdefault(spec, set()).add(obj)
        return obj


def import_submodules(package, recursive=True):
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results





























