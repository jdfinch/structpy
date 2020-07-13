
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
        enforcer_set.add(2)
        assert other.value == 11

        # Since 3 is already in the Set, only 4 and 6 will be added
        enforcer_set.update((3, 4, 6))
        assert other.value == 21

        assert enforcer_set == {1, 2, 3, 4, 5, 6}
        assert sum(enforcer_set) == other.value

    def remove(enforcer_set, element):
        """
        Similar to adding elements with `.add` or `.update`,
        removing elements with `.remove` or `.difference_update`
        results in a call to `remove_function(elements)` where `elements`
        is an iterable of elements that were removed from the enforcer Set.
        """
        enforcer_set.remove(3)
        assert other.value == 18

        # 9 was not in enforcer_set, so it is not subtracted from other.value
        enforcer_set.difference_update((1, 2, 9))
        assert other.value == 15

        assert enforcer_set == {4, 5, 6}
        assert sum(enforcer_set) == other.value

    @specification.satisfies(SetSpec.SET_OPERATIONS)
    def SET_OPERATIONS(EnforcerSet):
        return EnforcerSet



