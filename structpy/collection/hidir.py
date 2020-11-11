from structpy import implementation
from structpy.collection.hidir_spec import HidirSpec

from structpy.collection.hidict import Hidict
from itertools import chain


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
            stack = [(self, other, tuple())]
            while stack:
                this, other, superkeys = stack.pop()
                for key, values in dict.items(other):
                    keys = (*superkeys, key)
                    if key not in this:
                        dict.__setitem__(this, key, self._generate_subdict(self.order - len(keys), keys))
                    if len(keys) == self.order:
                        dict_updating = dict.__getitem__(this, key)
                        for k, v in values.items():
                            valueset = self._generate_valueset((*keys, k))
                            valueset.update(v)
                            dict.__setitem__(dict_updating, k, valueset)
                    else:
                        stack.append((dict.__getitem__(this, key), values, keys))
        else:
            for item in other:
                keys, value = item[:-1], item[-1]
                if not Hidict.__contains__(self, keys):
                    Hidict.__setitem__(self, keys, self._generate_valueset((*self.superkeys, keys)))
                set.add(Hidict.__getitem__(self, keys), value)

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