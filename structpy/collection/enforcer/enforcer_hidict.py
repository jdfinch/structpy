
from structpy import implementation
from structpy.collection.enforcer.enforcer_hidict_spec import EnforcerHidictSpec

from structpy.collection.hidict import Hidict

from collections.abc import Hashable

@implementation(EnforcerHidictSpec)
class EnforcerHidict(Hidict):

    def _generate_subdict(self, order, superkeys):
        return EnforcerHidict(order, None, self.add_function, self.remove_function, superkeys)

    def __init__(self, order, dict_like=None, add_function=None, remove_function=None, superkeys=tuple()):
        Hidict.__init__(self, order, None, superkeys)
        self.add_function = add_function
        self.remove_function = remove_function
        if dict_like is not None:
            self.update(dict_like)

    def __setitem__(self, keys, value):
        if not isinstance(keys, tuple):
            keys = (keys,)
        assert len(keys) == self.order + 1 and all([isinstance(key, Hashable) for key in keys])
        if keys not in self:
            items = self.add_function([(*self.superkeys, *keys, value)])
            if items is not None:
                items = [item[len(self.superkeys):] for item in items]
                Hidict.update(self, items)
            else:
                Hidict.__setitem__(self, keys, value)
        else:
            original_value = self[keys]
            items = self.remove_function([(*self.superkeys, *keys, original_value)])
            if items is not None:
                items = [item[len(self.superkeys):] for item in items]
                for item in items:
                    Hidict.__delitem__(self, item[:-1])
            else:
                Hidict.__delitem__(self, keys)
            items = self.add_function([(*self.superkeys, *keys, value)])
            if items is not None:
                items = [item[len(self.superkeys):] for item in items]
                Hidict.update(self, items)
            else:
                Hidict.__setitem__(self, keys, value)


    def __delitem__(self, keys):
        if not isinstance(keys, tuple):
            keys = (keys,)
        value = self[keys]
        if len(keys) == self.order + 1:
            items = self.remove_function([(*self.superkeys, *keys, value)])
            if items is not None:
                items = [item[len(self.superkeys):] for item in items]
                for item in items:
                    Hidict.__delitem__(self, item[:-1])
            else:
                Hidict.__delitem__(self, keys)
        else:
            items_original = value.items()
            items = self.remove_function(items_original)
            if items is not None:
                items = [item[len(self.superkeys):] for item in items]
                for item in items:
                    Hidict.__delitem__(self, item[:-1])
                if keys in self and self[keys] == {}:
                    Hidict.__delitem__(self, keys)
            else:
                Hidict.__delitem__(self, keys)

    def clear(self):
        items = self.remove_function(self.items())
        if items is not None:
            items = [item[len(self.superkeys):] for item in items]
            for item in items:
                Hidict.__delitem__(self, item[:-1])
        else:
            Hidict.clear(self)

    def popitem(self):
        item = Hidict.popitem(self)
        items = self.remove_function([item])
        if items is not None:
            items = [item[len(self.superkeys):] for item in items]
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
        items = set()
        if isinstance(other, dict):
            stack = [(tuple(), other)]
            while stack:
                superkeys, subdict = stack.pop()
                if len(superkeys) == self.order:
                    for k, v in subdict.items():
                        items.add((*superkeys, k, v))
                else:
                    for k, v in subdict.items():
                        stack.append(((*superkeys, k), v))
        else:
            items = other
        items_to_remove = [(*item[:-1], Hidict.__getitem__(self, item[:-1]))
                           for item in items if item[:-1] in self]
        items_to_add = items
        items_to_remove_mod = self.remove_function([(*self.superkeys, *item) for item in items_to_remove])
        items_to_add_mod = self.add_function([(*self.superkeys, *item) for item in items_to_add])
        if items_to_remove_mod is not None:
            items_to_remove_mod = [item[len(self.superkeys):] for item in items_to_remove_mod]
            for item in items_to_remove_mod:
                Hidict.__delitem__(self, item[:-1])
        else:
            for item in items_to_remove:
                Hidict.__delitem__(self, item[:-1])
        if items_to_add_mod is not None:
            items_to_add_mod = [item[len(self.superkeys):] for item in items_to_add_mod]
            Hidict.update(self, items_to_add_mod)
        else:
            Hidict.update(self, items_to_add)


if __name__ == '__main__':
    print(EnforcerHidictSpec.verify(EnforcerHidict))