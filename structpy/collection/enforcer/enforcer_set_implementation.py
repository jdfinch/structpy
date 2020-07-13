
from structpy import implementation
from structpy.collection.enforcer.enforcer_set_spec import EnforcerSetSpec


@implementation(EnforcerSetSpec)
class EnforcerSet(set):

    def __init__(self, elements=None, add_function=None, remove_function=None):
        set.__init__(self)
        self.add_function = add_function
        self.remove_function = remove_function
        if elements is not None:
            self.update(elements)

    def add(self, element):
        l = len(self)
        set.add(self, element)
        if len(self) > l and self.add_function is not None:
            self.add_function([element])

    def remove(self, element):
        l = len(self)
        set.remove(self, element)
        if len(self) < l and self.remove_function is not None:
            self.remove_function([element])

    def discard(self, element):
        set.discard(self, element)
        if self.remove_function is not None:
            self.remove_function([element])

    def pop(self):
        e = set.pop(self)
        if self.remove_function is not None:
            self.remove_function([e])

    def clear(self):
        if self.remove_function is not None:
            self.remove_function(self)
        set.clear(self)

    def update(self, iterable):
        difference = set(iterable)
        difference.difference_update(self)
        set.update(self, difference)
        if self.add_function is not None:
            self.add_function(difference)

    def difference_update(self, iterable):
        intersection = set(iterable)
        intersection.intersection_update(self)
        set.difference_update(self, intersection)
        if self.remove_function is not None:
            self.remove_function(intersection)

    def symmetric_difference_update(self, iterable):
        intersection = set(iterable)
        intersection.intersection_update(self)
        set.difference_update(self, intersection)
        if self.remove_function is not None:
            self.remove_function(intersection)
        difference = set(iterable)
        difference.difference_update(intersection)
        set.update(self, difference)
        if self.add_function is not None:
            self.add_function(difference)



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
