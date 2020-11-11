
from structpy import implementation
from structpy.collection.enforcer.enforcer_hidir_spec import EnforcerHidirSpec

from structpy.collection.hidir import Hidir
from structpy.collection.enforcer import EnforcerSet


class EnforcerValueSet(EnforcerSet):

    def __init__(self, superkeys, add_function, remove_function):
        self.superkeys = superkeys
        self._hidir_add_function = add_function
        self._hidir_remove_function = remove_function
        EnforcerSet.__init__(self, add_function=self._add_function, remove_function=self._remove_function)

    def _add_function(self, items):
        hidir_items = self._hidir_add_function([(*self.superkeys, item) for item in items])
        return [item[-1] for item in hidir_items] if hidir_items is not None else None

    def _remove_function(self, items):
        hidir_items = self._hidir_remove_function([(*self.superkeys, item) for item in items])
        return [item[-1] for item in hidir_items] if hidir_items is not None else None

    def __str__(self):
        return '{' + ', '.join(["'" + x + "'" for x in self]) + '}'

    def __repr__(self):
        return str(self)


@implementation(EnforcerHidirSpec)
class EnforcerHidir(Hidir):

    def _generate_subdict(self, order, superkeys):
        return EnforcerHidir(order, None, self.add_function, self.remove_function, superkeys)

    def _generate_valueset(self, keys):
        return EnforcerValueSet(keys, add_function=self.add_function, remove_function=self.remove_function)

    def __init__(self, order, dict_like=None, add_function=None, remove_function=None, superkeys=tuple()):
        Hidir.__init__(self, order, None, superkeys)
        self.add_function = add_function
        self.remove_function = remove_function
        if dict_like is not None:
            self.update(dict_like)

    def __setitem__(self, keys, values):
        if not isinstance(keys, tuple):
            keys = (keys,)
        if keys not in self:
            items = self.add_function([(*self.superkeys, *keys, value) for value in values])
            if items is not None:
                items = [item[len(self.superkeys):] for item in items]
                Hidir.update(self, items)
            else:
                Hidir.__setitem__(self, keys, values)
        else:
            original_values = self[keys]
            items = self.remove_function([(*self.superkeys, *keys, ov) for ov in original_values])
            if items is not None:
                items = [item[len(self.superkeys):] for item in items]
                for item in items:
                    Hidir.__delitem__(self, item[:-1])
            else:
                Hidir.__delitem__(self, keys)
            items = self.add_function([(*self.superkeys, *keys, value) for value in values])
            if items is not None:
                items = [item[len(self.superkeys):] for item in items]
                Hidir.update(self, items)
            else:
                Hidir.__setitem__(self, keys, values)

    def __delitem__(self, keys):
        if not isinstance(keys, tuple):
            keys = (keys,)
        values = self[keys]
        if len(keys) == self.order + 1:
            items = self.remove_function([(*self.superkeys, *keys, value) for value in values])
            if items is not None:
                items = [item[len(self.superkeys):] for item in items]
                for item in items:
                    Hidir.__delitem__(self, item[:-1])
            else:
                Hidir.__delitem__(self, keys)
        else:
            items_original = values.items()
            items = self.remove_function(items_original)
            if items is not None:
                items = set(item[len(self.superkeys):-1] for item in items) # todo: del full items
                for item in items:
                    Hidir.__delitem__(self, item)
                if keys in self and self[keys] == {}:
                    Hidir.__delitem__(self, keys)
            else:
                Hidir.__delitem__(self, keys)

    def clear(self):
        items = self.remove_function(self.items())
        if items is not None:
            items = [item[len(self.superkeys):] for item in items]
            for item in items:
                Hidir.__delitem__(self, item[:-1])
        else:
            Hidir.clear(self)

    def pop(self, keys, default=None):
        if not isinstance(keys, tuple):
            keys = (keys,)
        if keys not in self and default is not None:
            return default
        values = self[keys]
        value = set.pop(values)
        set.add(values, value)
        items = self.remove_function([(*self.superkeys, *keys, value)])
        if items is not None:
            items = [item[len(self.superkeys):] for item in items]
            for item in items:
                Hidir.__delitem__(self, item[:-1])
        else:
            Hidir.__delitem__(self, keys)
        return value

    def popitem(self):
        keys = list(self.keys())[-1]
        values = self[keys]
        value = set.pop(values)
        set.add(values, value)
        items = self.remove_function([(*self.superkeys, *keys, value)])
        if items is not None:
            items = [item[len(self.superkeys):] for item in items]
            for item in items:
                Hidir.__delitem__(self, item[:-1])
        else:
            Hidir.__delitem__(self, keys)
        return (*keys, value)

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
                    for k, vs in subdict.items():
                        items.update([(*superkeys, k, v) for v in vs])
                else:
                    for k, vs in subdict.items():
                        stack.append(((*superkeys, k), vs))
        else:
            items = other
        items_to_remove = set(items) & set(self.items())
        items_to_add = items
        items_to_remove_mod = self.remove_function([(*self.superkeys, *item) for item in items_to_remove])
        items_to_add_mod = self.add_function([(*self.superkeys, *item) for item in items_to_add])
        if items_to_remove_mod is not None:
            items_to_remove_mod = [item[len(self.superkeys):] for item in items_to_remove_mod]
            for item in items_to_remove_mod:
                Hidir.__delitem__(self, item[:-1])
        else:
            for item in items_to_remove:
                Hidir.__delitem__(self, item[:-1])
        if items_to_add_mod is not None:
            items_to_add_mod = [item[len(self.superkeys):] for item in items_to_add_mod]
            Hidir.update(self, items_to_add_mod)
        else:
            Hidir.update(self, items_to_add)


if __name__ == '__main__':
    print(EnforcerHidirSpec.verify(EnforcerHidir))