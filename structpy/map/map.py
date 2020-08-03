
from structpy import implementation
from structpy.map.map_spec import MapSpec

from structpy.collection.enforcer import EnforcerDict
from structpy.collection.enforcer import EnforcerSet


class DomainSet(EnforcerSet):

    def __init__(self, domain, element, elements=None):
        self.domain = domain
        self.element = element
        EnforcerSet.__init__(self,
            add_function=self._add_function,
            remove_function=self._remove_function
        )
        if elements is not None:
            self.update(elements)

    def _add_function(self, elements):
        elements = set(elements) - self
        for e in elements:
            set.add(self.domain[e], self.element)
        return elements

    def _remove_function(self, elements):
        elements = set(elements) & self
        for e in elements:
            set.remove(self.domain[e], self.element)
            if not self.domain[e]:
                dict.__delitem__(self.domain, e)
        return elements


@implementation(MapSpec)
class Map(EnforcerDict):

    def __init__(self, dict_like=None):
        EnforcerDict.__init__(self,
            add_function = self._add_function,
            remove_function = self._remove_function
        )
        self.codomain = None
        if hasattr(dict_like, 'codomain'):
            self.codomain = dict_like
        else:
            self.codomain = Map(self)
            self.update({k: DomainSet(self.codomain, k, values)
                         for k, values in dict_like.items()})

    def __getitem__(self, item):
        if item not in self:
            dict.__setitem__(self, item, DomainSet(self.codomain, item))
        return dict.__getitem__(self, item)

    def _add_function(self, items):
        for key, values in items:
            self[key].update(values)

    def _remove_function(self, items):
        for key, values in items:
            values.clear()

    def reverse(self):
        return self.codomain


if __name__ == '__main__':
    print(MapSpec.verify(Map))
