
from structpy import implementation
from structpy.collection.hidict_spec import HidictSpec

from functools import reduce


@implementation(HidictSpec)
class Hidict(dict):

    def __init__(self, order, dict_like=None):
        dict.__init__(self)
        assert isinstance(order, int) and order > 0
        self.order = order
        if dict_like is not None:
            self.update(dict_like)

    def __getitem__(self, keys):
        value = self
        for key in keys:
            value = dict.__getitem__(value, key)
        return value

    def __setitem__(self, keys, value):
        key0, keys = keys[0], keys[1:]
        if self.order > 1:
            if not dict.__contains__(self, key0):
                dict.__setitem__(self, key0, Hidict(self.order - 1))
            dict.__getitem__(self, key0)[keys] = value
        else:
            if not dict.__contains__(self, key0):
                dict.__setitem__(self, key0, {})
            dict.__getitem__(self, key0)[keys[0]] = value

    def update(self, dict_like):
        if self.order == 1:
            for key, value in dict_like.items():
                dict.__setitem__(self, key, {k: v for k, v in value.items()})
        else:
            for key, value in dict_like.items():
                subdict = Hidict(self.order - 1)
                subdict.update(value)
                dict.__setitem__(self, key, subdict)

    def __delitem__(self, keys):
        key0, keys = keys[0], keys[1:]
        if len(keys) == 0:
            dict.__getitem__(self, key0).clear()
        elif self.order == 1:
            dict.__getitem__(self, key0).__delitem__(keys[0])
        else:
            dict.__getitem__(self, key0).__delitem__(keys)

    def pop(self, *keys, default=None):
        if keys not in self and default is not None:
            return default
        value = self.__getitem__(*keys)
        del self[keys]
        return value

    def popitem(self):
        key, value = dict.popitem(self)
        dict.__setitem__(self, key, value)
        return (key,) + value.popitem()

    def setdefault(self, *keys, default=None):
        if keys in self:
            return self[keys]
        else:
            self[keys] = default
            return default

    def __contains__(self, item):
        if not isinstance(item, tuple):
            item = (item,)
        key0, keys = item[0], item[1:]
        if self.order == 1 and len(keys) == 2:
            return dict.__contains__(self, key0) and dict.__getitem__(self, key0)[keys[0]] == keys[1]
        elif self.order == 1:
            return dict.__contains__(self, key0) and (not keys or keys[0] in dict.__getitem__(self, key0))
        else:
            return dict.__contains__(self, key0) and (not keys or keys in dict.__getitem__(self, key0))

    def get(self, *keys, default=None):
        return self[keys] if keys in self else default

    def items(self, _previous_keys=tuple()):
        items = list(dict.items(self))
        if self.order == 1:
            return reduce(list.__add__,
                          [[(*_previous_keys, key1, key2, val) for key2, val in value.items()]
                           for key1, value in items])
        else:
            return reduce(list.__add__,
                          [value.items((*_previous_keys, key))
                           for key, value in items])

    def keys(self, _previous_keys=tuple()):
        items = list(dict.items(self))
        if self.order == 1:
            return reduce(list.__add__,
                          [[(*_previous_keys, key1, key2) for key2 in value.keys()]
                           for key1, value in items])
        else:
            return reduce(list.__add__,
                          [value.keys((*_previous_keys, key))
                           for key, value in items])

    def reversed(self):
        return reversed(self.keys())

    def values(self):
        items = list(dict.items(self))
        return reduce(list.__add__, [value.values() for _, value in items])

    def copy(self):
        c = Hidict()
        for item in self.items():
            c[item[:-1]] = item[-1]
        return c


if __name__ == '__main__':
    print(HidictSpec.verify(Hidict))