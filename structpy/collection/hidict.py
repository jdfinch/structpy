from structpy import implementation
from structpy.collection.hidict_spec import HidictSpec


@implementation(HidictSpec)
class Hidict(dict):

    def _generate_subdict(self, order, superkeys):
        return Hidict(order, None, superkeys)

    def __init__(self, order, dict_like=None, superkeys=tuple()):
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
            return value == keys[-1]
        else:
            raise KeyError(keys, self)

    def __setitem__(self, keys, value):
        if not isinstance(keys, tuple):
            keys = (keys,)
        assert len(keys) <= self.order + 1
        if len(keys) == self.order + 1:
            keys, keyprime = keys[:-1], keys[-1]
            d = self
            for i, key in enumerate(keys):
                if key not in d:
                    superkeys = keys[:i+1]
                    dict.__setitem__(d, key,
                        self._generate_subdict(self.order - i - 1, (*self.superkeys, *superkeys)))
                d = dict.__getitem__(d, key)
            dict.__setitem__(d, keyprime, value)
        else:
            if keys in self:
                del self[keys]
            d = self
            for i, key in enumerate(keys):
                if key not in d:
                    superkeys = keys[:i+1]
                    dict.__setitem__(d, key,
                        self._generate_subdict(self.order - i - 1, (*self.superkeys, *superkeys)))
                d = dict.__getitem__(d, key)
            stack = [(d, value, keys)]
            while stack:
                this, other, superkeys = stack.pop()
                if len(superkeys) == self.order:
                    dict.update(this, other)
                else:
                    for key, value in dict.items(other):
                        keys = (*superkeys, key)
                        if keys not in this:
                            dict.__setitem__(this, key, self._generate_subdict(self.order - len(keys), keys))
                        stack.append((dict.__getitem__(this, key), value, keys))

    def update(self, other):
        if isinstance(other, dict):
            stack = [(self, other, tuple())]
            while stack:
                this, other, superkeys = stack.pop()
                for key, value in dict.items(other):
                    keys = (*superkeys, key)
                    if key not in this:
                        dict.__setitem__(this, key, self._generate_subdict(self.order - len(keys), keys))
                    if len(keys) == self.order:
                        dict.update(dict.__getitem__(this, key), value)
                    else:
                        stack.append((dict.__getitem__(this, key), value, keys))
        else:
            for item in other:
                Hidict.__setitem__(self, item[:-1],  item[-1])

    def __delitem__(self, keys):
        if not isinstance(keys, tuple):
            keys = (keys,)
        assert len(keys) <= self.order + 1
        keys, keyprime = keys[:-1], keys[-1]
        value = self
        trail = []
        for key in keys:
            trail.append((value, key))
            value = dict.__getitem__(value, key)
        dict.__delitem__(value, keyprime)
        for d, key in trail[::-1]:
            if not dict.__getitem__(d, key):
                dict.__delitem__(d, key)
            else:
                break

    def pop(self, *keys, default=None):
        if keys not in self:
            return default
        value = self[keys]
        del self[keys]
        return value

    def popitem(self):
        raise AttributeError

    def setdefault(self, *keys, default=None):
        if keys in self:
            return self[keys]
        else:
            self[keys] = default
            return default

    def get(self, *keys, default=None):
        return self[keys] if keys in self else default

    def items(self):
        stack = [(self, tuple())]
        while stack:
            this, superkeys = stack.pop()
            for key, value in dict.items(this):
                keys = (*superkeys, key)
                if len(keys) == self.order + 1:
                    yield (*self.superkeys, *keys, value)
                else:
                    stack.append((dict.__getitem__(this, key), keys))

    def keys(self):
        stack = [(self, tuple())]
        while stack:
            this, superkeys = stack.pop()
            for key, value in dict.items(this):
                keys = (*superkeys, key)
                if len(keys) == self.order + 1:
                    yield (*self.superkeys, *keys)
                else:
                    stack.append((dict.__getitem__(this, key), keys))

    def reversed(self):
        return reversed(list(self.keys()))

    def values(self):
        stack = [(self, 0)]
        while stack:
            this, superkeys = stack.pop()
            for key, value in dict.items(this):
                keys = superkeys + 1
                if keys == self.order + 1:
                    yield value
                else:
                    stack.append((dict.__getitem__(this, key), keys))

    def copy(self):
        c = Hidict(self.order)
        c.update(self.items())
        return c


if __name__ == '__main__':
    print(HidictSpec.verify(Hidict))