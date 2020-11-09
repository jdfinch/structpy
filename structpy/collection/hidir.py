from structpy import implementation
from structpy.collection.hidir_spec import HidirSpec

from structpy.collection.hidict import Hidict


@implementation(HidirSpec)
class Hidir(Hidict):

    def __init__(self, order, dict_like=None, superkeys=tuple()):
        Hidict.__init__(self, order, None, superkeys)
        if dict_like is not None:
            self.update(dict_like)

    def _generate_subdict(self, key):
        return Hidir(len(self.superkeys), None, self.superkeys)

    def __setitem__(self, keys, values):
        Hidict.__setitem__(self, keys, set(values))

    def update(self, other):
        if isinstance(other, dict):
            stack = [(self, other, tuple())]
            while stack:
                this, other, superkeys = stack.pop()
                for key, values in dict.items(other):
                    keys = (*superkeys, key)
                    if key not in this:
                        dict.__setitem__(this, key, self._generate_subdict(key))
                    if len(keys) == self.order:
                        dict.update(dict.__getitem__(this, key), {k: set(v) for k, v in values.items()})
                    else:
                        stack.append((dict.__getitem__(this, key), values, keys))
        else:
            for item in other:
                Hidict.__setitem__(self, item[:-1],  set(item[-1]))


if __name__ == '__main__':
    print(HidirSpec.verify(Hidir))