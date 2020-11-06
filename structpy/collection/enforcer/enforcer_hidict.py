
from structpy import implementation
from structpy.collection.enforcer.enforcer_hidict_spec import EnforcerHidictSpec

from structpy.collection.enforcer.enforcer_dict import EnforcerDict
from structpy.collection.hidict import Hidict

from functools import reduce


@implementation(EnforcerHidictSpec)
class EnforcerHidict(Hidict):

    def _generate_subdict(self, key):
        return EnforcerHidict(self.order - 1, None,
                              self.add_function, self.remove_function, *self.superkeys, key)

    def __init__(self, order, dict_like=None, add_function=None, remove_function=None, *superkeys):
        Hidict.__init__(self, order, None, *superkeys)
        self.add_function = add_function
        self.remove_function = remove_function
        if dict_like is not None:
            self.update(dict_like)

    def __setitem__(self, keys, value):
        if not isinstance(keys, tuple):
            keys = (keys,)
        if keys not in self:
            items = self.add_function([(*keys, value)])
            if items is not None:
                Hidict.update(self, items)
            else:
                Hidict.__setitem__(self, keys, value)
        else:
            original_value = self[keys]
            items = self.remove_function([(*keys, original_value)])
            if items is not None:
                for item in items:
                    Hidict.__delitem__(self, item[:-1])
            else:
                Hidict.__delitem__(self, keys)
            items = self.add_function([(*keys, value)])
            if items is not None:
                Hidict.update(self, items)
            else:
                Hidict.__setitem__(self, keys, value)

    def __delitem__(self, keys):
        if not isinstance(keys, tuple):
            keys = (keys,)
        value = self[keys]
        items = self.remove_function([(*keys, value)])
        if items is not None:
            for item in items:
                Hidict.__delitem__(self, item[:-1])
        else:
            Hidict.__delitem__(self, keys)

    def clear(self):
        items = self.remove_function(self.items())
        if items is not None:
            for item in items:
                Hidict.__delitem__(self, item[:-1])
        else:
            Hidict.clear(self)

    def pop(self, keys, default=None):
        if not isinstance(keys, tuple):
            keys = (keys,)
        if keys not in self and default is not None:
            return default
        value = self[keys]
        items = self.remove_function([(*keys, value)])
        if items is not None:
            for item in items:
                Hidict.__delitem__(self, item[:-1])
        else:
            Hidict.__delitem__(self, keys)
        return value

    def popitem(self):
        item = Hidict.popitem(self)
        items = self.remove_function([item])
        if items is not None:
            for item in items:
                Hidict.__delitem__(self, item[:-1])
        else:
            Hidict.__delitem__(self, item[:-1])
        return item

    def setdefault(self, keys, default=None):
        if not isinstance(keys, tuple):
            keys = (keys,)
        if keys in self:
            return self[keys]
        else:
            self[keys] = default
            return default

    def update(self, other):
        if isinstance(other, dict):
            stack = [(self, other, tuple())]
            while stack:
                this, other, superkeys = stack.pop()
                for key, value in dict.items(other):
                    keys = (*superkeys, key)
                    if key not in this:
                        dict.__setitem__(this, key, self._generate_subdict(key))
                    if len(keys) == self.order:
                        dict.update(dict.__getitem__(this, key), value)
                    else:
                        stack.append((dict.__getitem__(this, key), value, keys))
        else:
            for item in other:
                self[item[:-1]] = item[-1]

if __name__ == '__main__':
    print(EnforcerHidictSpec.verify(EnforcerHidict))