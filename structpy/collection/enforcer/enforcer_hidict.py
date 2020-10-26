
from structpy import implementation
from structpy.collection.enforcer.enforcer_hidict_spec import EnforcerHidictSpec

from structpy.collection.enforcer.enforcer_dict import EnforcerDict
from structpy.collection.hidict import Hidict

from functools import reduce


@implementation(EnforcerHidictSpec)
class EnforcerHidict(Hidict):

    def _generate_subdict(self, key):
        return EnforcerHidict(self.order - 1, None,
                              self.add_function, self.remove_function, *self.superkeys, key, root_hidict=self)

    def __init__(self, order, dict_like=None, add_function=None, remove_function=None, *superkeys, root_hidict=None):
        Hidict.__init__(self, order, None, *superkeys)
        self.add_function = add_function
        self.remove_function = remove_function
        # self = root_hidict if root_hidict else self
        if dict_like is not None:
            self.update(dict_like)

    def __setitem__(self, key, value):
        if not self.order <= 0:
            return Hidict.__setitem__(self, key, value)
        if not isinstance(key, tuple):
            key = (key,)
        if key not in self:
            items = self.add_function([(*self.superkeys, *key, value)])
            if items is not None:
                for item in items:
                    Hidict.__setitem__(self, item[-2], item[-1])
            else:
                Hidict.__setitem__(self, *key, value)
        else:
            original_value = self[key]
            items = self.remove_function([(*self.superkeys, *key, original_value)])
            if items is not None:
                for item in items:
                    Hidict.__delitem__(self, item[-2])
            else:
                Hidict.__delitem__(self, *key)
            items = self.add_function([(*self.superkeys, *key, value)])
            if items is not None:
                for item in items:
                    Hidict.__setitem__(self, item[-2], item[-1])
            else:
                Hidict.__setitem__(self, *key, value)

    def __delitem__(self, key):
        if not self.order <= 0:
            return Hidict.__delitem__(self, key)
        if not isinstance(key, tuple):
            key = (key,)
        value = self[key]
        items = self.remove_function([(*self.superkeys, *key, value)])
        if items is not None:
            for item in items:
                Hidict.__delitem__(self, item[-2])
        else:
            Hidict.__delitem__(self, *key)

    def clear(self):
        if not self.order <= 0:
            return Hidict.clear(self)
        items = self.remove_function(self.items())
        if items is not None:
            for item in items:
                Hidict.__delitem__(self, item[-2])
        else:
            Hidict.clear(self)

    def pop(self, key, default=None):
        if not self.order <= 0:
            return Hidict.pop(self, key, default)
        if not isinstance(key, tuple):
            key = (key,)
        if key not in self and default is not None:
            return default
        value = self[key]
        items = self.remove_function([(*self.superkeys, key, value)])
        if items is not None:
            for item in items:
                Hidict.__delitem__(self, item[-2])
        else:
            Hidict.__delitem__(self, key)
        return value

    def popitem(self):
        if not self.order <= 0:
            return Hidict.popitem(self)
        key, value = Hidict.popitem(self)
        items = self.remove_function([(*self.superkeys, key, value)])
        if items is not None:
            for item in items:
                Hidict.__delitem__(self, item[-2])
        else:
            Hidict.__delitem__(self, key)
        return key, value

    def setdefault(self, key, default=None):
        if not self.order <= 0:
            return Hidict.setdefault(self, key, default)
        if not isinstance(key, tuple):
            key = (key,)
        if key in self:
            return self[key]
        else:
            self[key] = default
            return default

    def update(self, other):
        if not self.order <= 0:
            return Hidict.update(self, other)
        intersection = set(other.keys()) & set(self.keys())
        delitems = self.remove_function([(*self.superkeys, k, self[k]) for k in intersection])
        additems = self.add_function([(*self.superkeys, *item) for item in other.items()])
        if delitems is None and additems is None:
            dict.update(self, other)
        else:
            if delitems is not None:
                for item in delitems:
                    dict.__delitem__(self, item[-2])
            else:
                for item in intersection:
                    dict.__delitem__(self, item[-2])
            if additems is not None:
                dict.update(self, [(item[-2], item[-1]) for item in additems])
            else:
                dict.update(self, other)


if __name__ == '__main__':
    print(EnforcerHidictSpec.verify(EnforcerHidict))