
from structpy import implementation
from structpy.map.himap_spec import HimapSpec

from structpy.collection.enforcer import EnforcerHidir
from structpy.collection import Hidir


@implementation(HimapSpec)
class Himap(EnforcerHidir):

    def __init__(self, order, mapping=None):
        if isinstance(mapping, Himap) and not hasattr(mapping, 'codomain'):
            self.codomain = mapping
            EnforcerHidir.__init__(self, order,
                add_function=self._add_function, remove_function=self._remove_function)
        else:
            self.codomain = Himap(order, self)
            EnforcerHidir.__init__(self, order,
                add_function=self._add_function, remove_function=self._remove_function)
            if mapping is not None:
                self.update(mapping)

    def reverse(self):
        return self.codomain

    def _add_function(self, items):
        for item in items:
            print('Add:', item)
            keys, value = (item[-1], *item[1:-1]), item[0]
            if not Hidir.__contains__(self.codomain, keys):
                Hidir.__setitem__(self.codomain, keys, [value])
            else:
                set.add(Hidir.__getitem__(self.codomain, keys), value)

    def _remove_function(self, items):
        for item in items:
            print('Del:', item)
            keys, value = (item[-1], *item[1:-1]), item[0]
            valueset = Hidir.__getitem__(self.codomain, keys)
            set.remove(valueset, value)
            if not valueset:
                Hidir.__delitem__(self.codomain, keys)


if __name__ == '__main__':
    print(HimapSpec.verify(Himap))