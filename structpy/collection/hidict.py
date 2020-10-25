
from structpy import implementation
from structpy.collection.hidict_spec import HidictSpec

from functools import reduce


@implementation(HidictSpec)
class Hidict(dict):

    def _generate_subdict(self, key):
        """
        Create a subdict. Abstract to allow derived classes (e.g. EnforcerHidict)
        to create custom subdict objects.
        """
        return Hidict(self.order - 1, None, *self.superkeys, key)

    def __init__(self, order, dict_like=None, *superkeys):
        dict.__init__(self)
        assert order >= 0
        self.order = order
        self.superkeys = superkeys
        if dict_like is not None:
            self.update(dict_like)

    def __getitem__(self, keys):
        if not isinstance(keys, tuple):
            keys = (keys,)
        value = self
        for key in keys:
            value = dict.__getitem__(value, key)
        return value

    def __setitem__(self, keys, value):
        if not isinstance(keys, tuple):
            keys = (keys,)
        key0, keys = keys[0], keys[1:]
        if self.order <= 0:
            dict.__setitem__(self, key0, value)
        else:
            if not dict.__contains__(self, key0):
                subdict = self._generate_subdict(key0)
                dict.__setitem__(self, key0, subdict)
            else:
                subdict = dict.__getitem__(self, key0)
            subdict[keys] = value

    def update(self, dict_like):
        if self.order <= 0:
            for key, value in dict_like.items():
                dict.__setitem__(self, key, value)
        else:
            for key, value in dict_like.items():
                subdict = self._generate_subdict(key)
                subdict.update(value)
                dict.__setitem__(self, key, subdict)

    def __delitem__(self, keys):
        key0, keys = keys[0], keys[1:]
        if len(keys) == 0 and self.order > 0:
            dict.__getitem__(self, key0).clear()
        elif self.order <= 0:
            dict.__delitem__(self, key0)
        else:
            del dict.__getitem__(self, key0)[keys]

    def pop(self, *keys, default=None):
        if keys not in self:
            return default
        value = self[keys]
        del self[keys]
        return value

    def popitem(self):
        if self.order <= 0:
            return dict.popitem(self)
        else:
            key, value = dict.popitem(self)
            dict.__setitem__(self, key, value)
            return (key,) + value.popitem()

    def setdefault(self, *keys, default=None):
        if keys in self:
            return self[keys]
        else:
            self[keys] = default
            return default

    def __contains__(self, keys):
        value = None
        value_included = False
        if not isinstance(keys, tuple):
            keys = (keys,)
        elif len(keys) > self.order + 1:
            keys, value = keys[:-1], keys[-1]
            value_included = True
        subdict = self
        for key in keys:
            if not dict.__contains__(subdict, key):
                return False
            else:
                subdict = dict.__getitem__(subdict, key)
        if value_included:
            return value == subdict
        else:
            return True

    def get(self, *keys, default=None):
        return self[keys] if keys in self else default

    def items(self):
        if self.order <= 0:
            return [(*self.superkeys, key, value) for key, value in dict.items(self)]
        else:
            return reduce(list.__add__,
                    [[]] + [value.items() for key, value in dict.items(self)])

    def keys(self):
        if self.order <= 0:
            return [(*self.superkeys, key) for key in dict.keys(self)]
        else:
            return reduce(list.__add__,
                          [[]] + [value.keys() for key, value in dict.items(self)])

    def reversed(self):
        return reversed(self.keys())

    def values(self):
        if self.order <= 0:
            return list(dict.values(self))
        else:
            return reduce(list.__add__, [value.values() for value in dict.values(self)])

    def copy(self):
        c = Hidict(self.order)
        for item in self.items():
            c[item[:-1]] = item[-1]
        return c


if __name__ == '__main__':
    print(HidictSpec.verify(Hidict))