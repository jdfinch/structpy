
from structpy import implementation
from structpy.collection.enforcer.enforcer_set_spec import EnforcerSetSpec


@implementation(EnforcerSetSpec)
class EnforcerSet(set):

    def __init__(self, elements=None, add_function=None, remove_function=None):
        set.__init__(self)
        self.add_function = add_function
        self.remove_function = remove_function
        if elements is not None:
            self.update(elements if isinstance(elements, set) else set(elements))

    def add(self, element):
        if self.add_function is None:
            return set.add(self, element)
        elements = self.add_function([element])
        if elements is not None:
            set.update(self, elements)
        else:
            set.add(self, element)

    def remove(self, element):
        if self.remove_function is None:
            return set.remove(self, element)
        elements = self.remove_function([element])
        if elements is not None:
            set.difference_update(self, elements)
        else:
            set.remove(self, element)

    def discard(self, element):
        if self.remove_function is None:
            return set.discard(self, element)
        elements = self.remove_function([element])
        if elements is not None:
            set.difference_update(self, elements)
        else:
            set.discard(self, element)

    def pop(self):
        if self.remove_function is None:
            return set.pop(self)
        e = set.pop(self)
        set.add(self, e)
        elements = self.remove_function([e])
        if elements is not None:
            set.difference_update(self, elements)
        else:
            set.discard(self, e)
        return e

    def clear(self):
        if self.remove_function is None:
            return set.clear(self)
        elements = self.remove_function(self, self)
        if elements is not None:
            set.difference_update(self, elements)
        else:
            set.clear(self)

    def update(self, iterable):
        if self.add_function is None:
            return set.update(iterable)
        elements = self.add_function(iterable)
        if elements is not None:
            set.update(self, elements)
        else:
            set.update(self, iterable)

    def difference_update(self, iterable):
        if self.remove_function is None:
            return set.difference_update(self, iterable)
        elements = self.remove_function(iterable)
        if elements is not None:
            set.difference_update(self, elements)
        else:
            set.difference_update(self, iterable)

    def symmetric_difference_update(self, iterable):
        if self.add_function is None and self.remove_function is None:
            return set.symmetric_difference_update(self, iterable)
        other = set(iterable)
        intersection = other & self
        difference = other.difference_update(intersection)
        self.difference_update(intersection)
        self.update(difference)

if __name__ == '__main__':
    import sys
    print('Size of python set, 0 elements:', sys.getsizeof(set()))
    print('Size of EnforcerSet, 0 elements:', sys.getsizeof(EnforcerSet()))
    print('Size of python set, 10 elements:', sys.getsizeof(set(range(10))))
    print('Size of python set, 100 elements:', sys.getsizeof(set(range(50))))
    print('Size of EnforcerSet, 10 elements:', sys.getsizeof(EnforcerSet(range(10))))
    print('Size of EnforcerSet, 100 elements:', sys.getsizeof(EnforcerSet(range(50))))
    """
    Size of python set, 0 elements: 232
    Size of EnforcerSet, 0 elements: 240
    Size of python set, 10 elements: 744
    Size of python set, 100 elements: 2280
    Size of EnforcerSet, 10 elements: 752
    Size of EnforcerSet, 100 elements: 2288
    """
    print(EnforcerSetSpec.verify(EnforcerSet))
