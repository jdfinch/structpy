from structpy import implementation
from structpy.collection.hidir_spec import HidirSpec

from structpy.collection.hidict import Hidict
from itertools import chain
from collections.abc import Hashable


@implementation(HidirSpec)
class Hidir(Hidict):

    def __init__(self, order, dict_like=None, superkeys=tuple()):
        Hidict.__init__(self, order, None, superkeys)
        if dict_like is not None:
            self.update(dict_like)

    def _generate_subdict(self, order, superkeys):
        return Hidir(order, None, superkeys)

    def _generate_valueset(self, keys):
        return set()

    def __contains__(self, keys):
        if not isinstance(keys, tuple):
            keys = (keys,)
        if len(keys) <= self.order + 1:
            assert len(keys) <= self.order + 1
            value = self
            for key in keys:
                if not dict.__contains__(value, key):
                    return False
                value = dict.__getitem__(value, key)
            return True
        elif len(keys) == self.order + 2:
            value = self
            for key in keys[:-1]:
                if not dict.__contains__(value, key):
                    return False
                value = dict.__getitem__(value, key)
            return keys[-1] in value
        else:
            raise KeyError(keys, self)

    def __setitem__(self, keys, values):
        valueset = self._generate_valueset((*self.superkeys, *keys))
        set.update(valueset, values)
        Hidict.__setitem__(self, keys, valueset)

    def update(self, other):
        if isinstance(other, dict):
            items = []
            stack = [(other, tuple())]
            while stack:
                other, superkeys = stack.pop()
                if len(superkeys) == self.order:
                    for key, value in dict.items(other):
                        items.extend([(*superkeys, key, v) for v in value])
                else:
                    for key, value in dict.items(other):
                        stack.append((value, (*superkeys, key)))
            other = items
        for item in other:
            assert all([isinstance(x, Hashable) for x in item])
            keys, value = item[:-1], item[-1]
            if Hidict.__contains__(self, keys):
                set.add(Hidict.__getitem__(self, keys), value)
            else:
                valueset = self._generate_valueset((*self.superkeys, *keys))
                set.add(valueset, value)
                Hidict.__setitem__(self, keys, valueset)

    def values(self):
        return chain(Hidict.values(self))

    def items(self):
        stack = [(self, tuple())]
        while stack:
            this, superkeys = stack.pop()
            for key, value in dict.items(this):
                keys = (*superkeys, key)
                if len(keys) == self.order + 1:
                    yield from [(*self.superkeys, *keys, v) for v in value]
                else:
                    stack.append((dict.__getitem__(this, key), keys))


if __name__ == '__main__':
    print(HidirSpec.verify(Hidir))