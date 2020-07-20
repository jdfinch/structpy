

from structpy import implementation
from structpy.collection.enforcer.enforcer_dict_spec import EnforcerDictSpec


@implementation(EnforcerDictSpec)
class EnforcerDict(dict):

    def __init__(self, dict_like=None, add_function=None, remove_function=None):
        dict.__init__(self)
        self.add_function = add_function
        self.remove_function = remove_function
        if dict_like is not None:
            self.update(dict_like)

    def __setitem__(self, key, value):
        if key not in self:
            items = self.add_function([(key, value)])
            if items is not None:
                dict.update(self, items)
            else:
                dict.__setitem__(self, key, value)
        else:
            original_value = self[key]
            items = self.remove_function([(key, original_value)])
            if items is not None:
                for k, _ in items:
                    dict.__delitem__(self, k)
            else:
                dict.__delitem__(self, key)
            items = self.add_function([(key, value)])
            if items is not None:
                dict.update(self, items)
            else:
                dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        value = self[key]
        items = self.remove_function([(key, value)])
        if items is not None:
            for k, _ in items:
                dict.__delitem__(self, k)
        else:
            dict.__delitem__(self, key)

    def clear(self):
        items = self.remove_function(self.items())
        if items is not None:
            for k, _ in items:
                dict.__delitem__(self, k)
        else:
            dict.clear(self)

    def pop(self, key, default=None):
        if key not in self and default is not None:
            return default
        value = self[key]
        items = self.remove_function([(key, value)])
        if items is not None:
            for k, _ in items:
                dict.__delitem__(self, k)
        else:
            dict.__delitem__(self, key)
        return value

    def popitem(self):
        key, value = dict.popitem(self)
        items = self.remove_function([(key, value)])
        if items is not None:
            for k, _ in items:
                dict.__delitem__(self, k)
        else:
            dict.__delitem__(self, key)
        return key, value

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        else:
            self[key] = default
            return default

    def update(self, other):
        intersection = set(other.keys()) & set(self.keys())
        delitems = self.remove_function([(k, self[k]) for k in intersection])
        additems = self.add_function(other.items())
        if delitems is None and additems is None:
            dict.update(self, other)
        else:
            if delitems is not None:
                for k, _ in delitems:
                    dict.__delitem__(self, k)
            else:
                for k, _ in intersection:
                    dict.__delitem__(self, k)
            if additems is not None:
                dict.update(self, additems)
            else:
                dict.update(self, other)


if __name__ == '__main__':
    print(EnforcerDictSpec.verify(EnforcerDict))
