
from structpy import implementation
from structpy.map.function.function_spec import FunctionSpec

import structpy.map.lookup.lookup as lookup

from structpy.collection.enforcer import EnforcerDict


@implementation(FunctionSpec)
class Function(EnforcerDict):

    def __init__(self, dict_like=None):
        EnforcerDict.__init__(self)
        self.codomain = None
        if hasattr(dict_like, 'codomain'):
            self.codomain = dict_like
        else:
            self.codomain = lookup.Lookup(self)
        self.update(dict_like)

    def _add_function(self, items):
        for key, value in items:
            self.codomain[value].add(key)

    def _remove_function(self, items):
        for key, value in items:
            self.codomain[value].remove(key)

    def reverse(self):
        return self.codomain


if __name__ == '__main__':
    print(FunctionSpec.verify(Function))