
from structpy import specification
# import structpy.map.index.index_spec as indexspec


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
        del function['two']
        assert 'two' not in function

    def reverse(function):
        """
        Reverses a `Function` into an `Index` representation.
        """
        idx = function.reverse()
        assert 'one' in idx[1]
        assert 'uno' in idx[1]
        assert 'dos' in idx[3]
        del idx[3]
        assert 'dos' not in function

    # @specification.satisfies(indexspec.IndexSpec.INDEX)
    # def REVERSE(Function):
    #     """
    #     Returns a index (one-to-many mapping) representing
    #     a function with domain and codomain swapped.
    #     """
    #     return Function({
    #         'one': 1,
    #         'hana': 1,
    #         'uno': 1,
    #         'dos': 2,
    #         'two': 2,
    #         'three': 3
    #     }).reverse()






