
from structpy import implementation
from structpy.map.function.function_spec import FunctionSpec

import structpy.map.index.index as index

from structpy.collection.enforcer import EnforcerDict


@implementation(FunctionSpec)
class Function(EnforcerDict):

    def __init__(self, dict_like=None):
        EnforcerDict.__init__(self,
            add_function=self._add_function,
            remove_function=self._remove_function
        )
        self.codomain = None
        if hasattr(dict_like, 'codomain'):
            self.codomain = dict_like
            for key, values in self.codomain.items():
                for value in values:
                    self[value] = key
        else:
            self.codomain = index.Index(self)
            self.update(dict_like)

    def _add_function(self, items):
        for key, value in items:
            set.add(self.codomain[value], key)

    def _remove_function(self, items):
        for key, value in items:
            set.discard(self.codomain[value], key)
            if len(self.codomain[value]) == 0:
                del self.codomain[value]

    def reverse(self):
        return self.codomain


if __name__ == '__main__':
    print(FunctionSpec.verify(Function))