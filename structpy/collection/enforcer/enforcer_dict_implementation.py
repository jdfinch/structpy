

from structpy import implementation
from structpy.collection.enforcer.enforcer_dict_spec import EnforcerDictSpec


@implementation(EnforcerDictSpec)
class EnforcerDict(dict):

    def __init__(self, dict_like=None, add_function=None, remove_function=None):
        if dict_like is None:
            dict_like = {}
        dict.__init__(self, dict_like)
        self.add_function = add_function
        self.remove_function = remove_function
        self.add_function(dict_like.items())

    def __setitem__(self, key, value):
        if key not in self:
            dict.__setitem__(self, key, value)
            self.add_function([(key, value)])
        else:
            original_value = self[key]
            self.remove_function([(key, original_value)])
            dict.__setitem__(self, key, value)
            self.add_function([(key, value)])

    def __delitem__(self, key):
        value = self[key]
        dict.__delitem__(self, key)
        self.remove_function([(key, value)])

    def clear(self):
        self.remove_function(self.items())
        dict.clear(self)

    def pop(self, key, default=None):
        if key not in self and default is not None:
            return default
        value = self[key]
        dict.__delitem__(self, key)
        self.remove_function([(key, value)])
        return value

    def popitem(self):
        key, value = dict.popitem(self)
        self.remove_function([(key, value)])
        return key, value

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        else:
            self[key] = default
            return default

    def update(self, other):
        intersection = set(other.keys()) & set(self.keys())
        self.remove_function([(k, self[k]) for k in intersection])
        self.add_function(other.items())
        dict.update(self, other)


if __name__ == '__main__':
    print(EnforcerDictSpec.verify(EnforcerDict))
