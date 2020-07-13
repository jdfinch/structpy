
from structpy import implementation
from structpy.map.bijective.bimap_spec import BimapSpec


@implementation(BimapSpec)
class Bimap:

    def __init__(self, mapping=None):
        self._forward = {}
        self._reverse = {}
        if mapping is not None:
            for k, v in mapping.items():
               self.__setitem__(k, v)

    def reverse(self):
        reverse_bimap = Bimap()
        reverse_bimap._reverse = self._forward
        reverse_bimap._forward = self._reverse
        return reverse_bimap

    def __getitem__(self, item):
        return self._forward[item]

    def __setitem__(self, key, value):
        if key in self._forward:
            del self._forward[key]
        if value in self._reverse:
            del self.reverse()[value]
        self._forward[key] = value
        self._reverse.__setitem__(value, key)

    def __delitem__(self, key):
        value = self._forward[key]
        del self._reverse[value]
        del self._forward[key]


if __name__ == '__main__':
    print(BimapSpec.verify(Bimap))
