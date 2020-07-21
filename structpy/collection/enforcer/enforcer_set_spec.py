from structpy import specification
from structpy.collection.set_spec import SetSpec


other = None


@specification
class EnforcerSetSpec:
    """
    Implementation of vanilla python `set` with Enforcer hooks
    `add_function` and `remove_function`.
    """

    @specification.init
    def ENFORCER_SET(EnforcerSet, elements=None, add_function=None, remove_function=None):
        """
        Create a Set with elements specified by iterable `elements`.

        `add_function` and `remove_function` can be specified, causing:

        when elements are added to enforcer_set: `add_function(elements)`

        when elements are removed from enforcer_set: `remove_function(elements)`
        """

        # In this example, we have an integer value stored in another object
        # The enforcer_set will enforce that this integer equals the sum
        # of elements in the enforcer_set
        class Other:
            def __init__(self):
                self.value = 0
            def add_function(self, elements):
                for element in elements: self.value += element
            def remove_function(self, elements):
                for element in elements: self.value -= element

        global other
        other= Other()

        enforcer_set = EnforcerSet(
            elements=(1, 3, 5),
            add_function=other.add_function,
            remove_function=other.remove_function
        )

        # Just by creating the enforcer_set with these functions,
        # other_object.value will be forced to 9
        assert other.value == 9

        return enforcer_set

    def add(enforcer_set, element):
        """
        Adding elements to the enforcer_set will result in a call
        to `add_function(elements)`, where `elements` is an iterable of
        all newly added elements.

        `.add(element)` and `.update(elements)` both have this behavior
        """
        enforcer_set.update((3, 4, 6))
        assert other.value == 22
        assert enforcer_set == {1, 3, 4, 5, 6}

    def remove(enforcer_set, element):
        """
        Similar to adding elements with `.add` or `.update`,
        removing elements with `.remove` or `.difference_update`
        results in a call to `remove_function(elements)` where `elements`
        is an iterable of elements that were removed from the enforcer Set.
        """
        enforcer_set.difference_update((1, 3, 9))
        assert other.value == 9
        assert enforcer_set == {4, 5, 6}

    @specification.init
    def ENFORCEMENT_FUNCTIONS_AS_MODIFIERS(EnforcerSet):
        """
        Enforcement functions `add_function` and `remove_function` can
        modify items added/removed by returning an updated items iterable.
        """

        class SumSet(EnforcerSet):

            def __init__(self, elements=None):
                self.sum = 0
                EnforcerSet.__init__(self,
                    elements,
                    add_function=self._add,
                    remove_function=self._remove
                )

            def _add(self, elements):
                new = set(elements) - self
                self.sum += sum(new)
                return new

            def _remove(self, elements):
                existing = set(elements) & self
                self.sum -= sum(existing)
                return existing

        sum_set = SumSet((1, 2, 3, 4, 5))
        assert sum_set.sum == 15

        sum_set.update({1, 6})
        assert sum_set.sum == 21

        sum_set.difference_update({2, 8})
        assert sum_set.sum == 19

        assert sum_set == {1, 3, 4, 5, 6}

        return sum_set

    @specification.satisfies(SetSpec.SET_OPERATIONS)
    def SET_OPERATIONS(EnforcerSet):
        return EnforcerSet



