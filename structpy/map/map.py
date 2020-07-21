
from structpy import implementation
from structpy.map.map_spec import MapSpec

from structpy.collection.enforcer import EnforcerDict
from structpy.collection.enforcer import EnforcerSet


class DomainSet(EnforcerSet):

    def __init__(self, domain, element):
        self.domain = domain
        self.element = element
        EnforcerSet.__init__(self,
            add_function=self._add_function,
            remove_function=self._remove_function
        )

    def _add_function(self, elements):
        for e in elements:
            if e not in self.domain:
                self.domain[e] = DomainSet(self.domain, e)
            self.domain[e].add(self.element)

    def _remove_function(self, elements):
        for e in elements:
            self.domain[e].remove(self.element)
            if not self.domain[e]:
                dict.__delitem__(self.domain, e)


@implementation(MapSpec)
class Map(EnforcerDict):

    def __init__(self, dict_like=None):
        dict.__init__(self)
        self.add_function = self._add_function
        self.remove_function = self._remove_function
        self.codomain = None
        if hasattr(dict_like, 'codomain'):
            self.codomain = dict_like
        else:
            self.codomain = Map(self)
            self.update(dict_like)

    def __getitem__(self, item):
        if item not in self:
            self[item] = DomainSet(self.codomain, item)
        return dict.__getitem__(self, item)

    def _add_function(self, items):
        for key, values in items:
            dict.__setitem__(self, key, DomainSet(self.codomain, key))
            self[key].update(values)

    def _remove_function(self, items):
        for key, values in items:
            values.clear()

    def reverse(self):
        return self.codomain


if __name__ == '__main__':
    print(MapSpec.verify(Map))
