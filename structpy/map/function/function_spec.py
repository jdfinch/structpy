
from structpy import specification


@specification
class FunctionSpec:
    """
    Function Mapping

    many-to-one mapping between keys and values
    """

    @specification.init
    def FUNCTION(Function):
        return Function({'one': 1, 'two': 2, 'uno': 1})

    def __getitem__(function, item):
        """
        get the value in the domain associated with a domain item
        """
        assert function['one'] == 1
        assert function['two'] == 2
        assert function['three'] == 3

    def __setitem__(function, key, value):
        """
        add a item pair that co-map

        the first item is added to the domain
        the second item is added to the domain
        """
        function['dos'] = 2
        assert function['dos'] == 2

        # overwrite key-value pair
        function['dos'] = 3
        assert function['dos'] == 3

    def reverse(function):
        """
        returns a lookup (one-to-many mapping) representing
        a mapping with domain and domain swapped
        """
        r = function.reverse()
        assert 'one' in r[1]
        assert 'uno' in r[1]
        assert 'two' in r[2]






