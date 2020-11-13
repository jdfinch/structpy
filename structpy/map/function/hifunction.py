
from structpy import implementation
from structpy.map.function.hifunction_spec import HifunctionSpec

import structpy.map.index.hiindex as hiindex

from structpy.collection.enforcer import EnforcerHidict
from structpy.collection import Hidict, Hidir


@implementation(HifunctionSpec)
class Hifunction(EnforcerHidict):

    def __init__(self, order, mapping=None):
        if isinstance(mapping, hiindex.Hiindex) and not hasattr(mapping, 'codomain'):
            self.codomain = mapping
            EnforcerHidict.__init__(self, order,
                add_function=self._add_function, remove_function=self._remove_function)
        else:
            self.codomain = hiindex.Hiindex(order, self)
            EnforcerHidict.__init__(self, order,
                add_function=self._add_function, remove_function=self._remove_function)
            if mapping is not None:
                self.update(mapping)

    def reverse(self):
        return self.codomain

    def _add_function(self, items):
        for item in items:
            keys, value = (item[-1], *item[1:-1]), item[0]
            if not Hidir.__contains__(self.codomain, keys):
                Hidir.__setitem__(self.codomain, keys, [value])
            else:
                set.add(Hidir.__getitem__(self.codomain, keys), value)

    def _remove_function(self, items):
        for item in items:
            keys, value = (item[-1], *item[1:-1]), item[0]
            valueset = Hidir.__getitem__(self.codomain, keys)
            set.remove(valueset, value)
            if not valueset:
                Hidir.__delitem__(self.codomain, keys)


if __name__ == '__main__':
    print(HifunctionSpec.verify(Hifunction))