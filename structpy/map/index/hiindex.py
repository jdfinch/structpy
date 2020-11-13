
from structpy import implementation
from structpy.map.index.hiindex_spec import HiindexSpec

import structpy.map.function.hifunction as hifunction

from structpy.collection.enforcer import EnforcerHidir
from structpy.collection import Hidir, Hidict


@implementation(HiindexSpec)
class Hiindex(EnforcerHidir):

    def __init__(self, order, mapping=None):
        if isinstance(mapping, hifunction.Hifunction) and not hasattr(mapping, 'codomain'):
            self.codomain = mapping
            EnforcerHidir.__init__(self, order,
                add_function=self._add_function, remove_function=self._remove_function)
        else:
            self.codomain = hifunction.Hifunction(order, self)
            EnforcerHidir.__init__(self, order,
                add_function=self._add_function, remove_function=self._remove_function)
            if mapping is not None:
                self.update(mapping)

    def reverse(self):
        return self.codomain

    def _add_function(self, items):
        for item in items:
            keys, value = (item[-1], *item[1:-1]), item[0]
            if Hidict.__contains__(self.codomain, keys):
                replaced = self.codomain[keys]
                self[(replaced, *item[1:-1])].remove(item[-1])
            Hidict.__setitem__(self.codomain, keys, value)

    def _remove_function(self, items):
        for item in items:
            keys, _ = (item[-1], *item[1:-1]), item[0]
            Hidict.__delitem__(self.codomain, keys)


if __name__ == '__main__':
    print(HiindexSpec.verify(Hiindex))