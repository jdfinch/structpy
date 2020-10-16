
from structpy import implementation
from structpy.map.index.index_spec import IndexSpec

from structpy.collection.enforcer import EnforcerDict, EnforcerSet
import structpy.map.function.function as function


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
        for element in elements:
            if element in self.domain:
                del self.domain[element]
        elements = set(elements) - self
        for e in elements:
            dict.__setitem__(self.domain, e, self.element)
        return elements

    def _remove_function(self, elements):
        elements = set(elements) & self
        for e in elements:
            dict.__delitem__(self.domain, e)
        return elements


@implementation(IndexSpec)
class Index(EnforcerDict):

    def __init__(self, dict_like=None):
        EnforcerDict.__init__(self,
            add_function=self._add_function,
            remove_function=self._remove_function
        )
        self.codomain = None
        if hasattr(dict_like, 'codomain'):
            self.codomain = dict_like
        else:
            self.codomain = function.Function(self)
            self.update(dict_like)

    def _add_function(self, items):
        for key, values in items:
            self[key].update(values)
        return []

    def _remove_function(self, items):
        for key, values in items:
            values.clear()

    def update(self, other):
        if isinstance(other, dict):
            other = other.items()
        for key, values in other:
            self[key].update(values)

    def __getitem__(self, item):
        if item not in self:
            dict.__setitem__(self, item, DomainSet(self.codomain, item))
        return dict.__getitem__(self, item)

    def __setitem__(self, key, values):
        EnforcerDict.__setitem__(self, key, DomainSet(self.codomain, key))
        self[key].update(values)

    def reverse(self):
        return self.codomain


if __name__ == '__main__':
    print(IndexSpec.verify(Index))

