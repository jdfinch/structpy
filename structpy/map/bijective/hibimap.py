
from structpy import implementation
from structpy.map.bijective.hibimap_spec import HibimapSpec
from structpy.collection.enforcer import EnforcerHidict, EnforcerDict
from structpy.collection import Hidict


class ReverseHibidict(EnforcerDict):

    def __init__(self, reverse):
        EnforcerDict.__init__(self, add_function=self._add_function, remove_function=self._remove_function)
        self._reverse = reverse

    def _add_function(self, items):
        for key, value in items:
            if key in self:
                del self[key]
            if value in self._reverse:
                self._reverse._del_item(value)
            self._reverse._set_item(value, key)

    def _remove_function(self, items):
        for _, value in items:
            self._reverse._del_item(value)


@implementation(HibimapSpec)
class Hibimap(EnforcerHidict):

    def __init__(self, order, mapping=None):
        EnforcerHidict.__init__(self, order)
        self.add_function = self._add_function
        self.remove_function = self._remove_function
        if isinstance(mapping, Hibimap):
            self._reverse = mapping
        else:
            self._reverse = ReverseHibidict(self)
            if mapping is not None:
                self.update(mapping)

    def _add_function(self, items):
        for item in items:
            key, value = item[:-1], item[-1]
            if key in self:
                del self[key]
            if value in self._reverse:
                del self._reverse[value]
            dict.__setitem__(self._reverse, value, key)

    def _remove_function(self, items):
        for item in items:
            key, value = item[:-1], item[-1]
            dict.__delitem__(self._reverse, value)

    def _set_item(self, keys, value):
        self.add_function = None
        self.remove_function = None
        Hidict.__setitem__(self, keys, value)
        self.add_function = self._add_function
        self.remove_function = self._remove_function

    def _del_item(self, keys):
        self.remove_function = None
        Hidict.__delitem__(self, keys)
        self.remove_function = self._remove_function

    def reverse(self):
        return self._reverse

if __name__ == '__main__':
    print(HibimapSpec.verify(Hibimap))
