
from structpy import specification


@specification
class FunctionSpec:
    """
    Many-to-one mapping between elements in a domain to elements in a codomain.
    """

    @specification.init
    def FUNCTION(Function):
        function = Function({
            'one': 1,
            'two': 2,
            'uno': 1
        })
        return function

    def getitem(function, item):
        """
        Get the value in the domain associated with a domain item.
        """
        assert function['one'] == 1
        assert function['two'] == 2
        assert function['three'] == 3

    def setitem(function, key, value):
        """
        Add a item pair that co-map.
        """
        function['dos'] = 2
        assert function['dos'] == 2

        # overwrite key-value pair
        function['dos'] = 3
        assert function['dos'] == 3

    def delitem(function, element):
        """
        Remove an item pair from the function by key (domain element).
        """
        del function['three']
        assert 'three' not in function

    def reverse(function):
        """
        Returns a lookup (one-to-many mapping) representing
        a function with domain and codomain swapped.
        """
        r = function.reverse()
        assert 'one' in r[1]
        assert 'uno' in r[1]
        assert 'two' in r[2]






