
from structpy import implementation
from structpy.map.bijective.bimap_spec import BimapSpec
from structpy.collection.enforcer import EnforcerDict


@implementation(BimapSpec)
class Bimap(EnforcerDict):

    def __init__(self, mapping=None):
        EnforcerDict.__init__(self)
        self.add_function = self._add_function
        self.remove_function = self._remove_function
        if isinstance(mapping, Bimap):
            self._reverse = mapping
        else:
            self._reverse = Bimap(self)
            if mapping is not None:
                self.update(mapping)

    def _add_function(self, items):
        for key, value in items:
            if key in self:
                del self[key]
            if value in self._reverse:
                del self._reverse[value]
            dict.__setitem__(self._reverse, value, key)


    def _remove_function(self, items):
        for key, value in items:
            dict.__delitem__(self._reverse, value)

    def reverse(self):
        return self._reverse

if __name__ == '__main__':
    print(BimapSpec.verify(Bimap))
