
from structpy import specification
import structpy.map.function.function_spec as functionspec


@specification
class IndexSpec:
    """
    Finite one-to-many mapping between a domain and codomain.
    """

    @specification.init
    def INDEX(Index, mapping=None):
        index = Index({
            1: {'one', 'hana', 'uno'},
            2: {'dos', 'two'},
            3: {'three'}
        })
        return index

    def getitem(index, item):
        """
        Get a reference to the elements in the codomain associated
        with a domain element.
        """
        assert index[1] == {'one', 'hana', 'uno'}
        assert index[3] == {'three'}

        # Elements can be added individually using the reference.
        index[3].add('tres')
        assert 'tres' in index[3]

    def additem(index, key, values):
        """
        Set the domain elements associated with a key to all the
        elements present in values.

        Each element of values is added to the domain, without
        a direct reference to the provided values object.
        """
        index[4].add('four')
        index[4].update(['cuatro', 'net'])
        assert 4 in index
        assert index[4] == {'four', 'cuatro', 'net'}

        # Adding an keys can be done via subscript as well.
        index[5]
        assert 5 in index
        assert index[5] == set()

        # Many-to-one consistency enforced when adding
        index[5].add('cuatro')
        assert 'cuatro' not in index[4]
        assert 'cuatro' in index[5]
        index[4].add('cuatro')
        assert 'cuatro' in index[4]
        assert 'cuatro' not in index[5]

    def delitem(index, item):
        """
        Remove an element from the index domain.
        """
        del index[2]
        assert 2 not in index

    def update(index, mapping):
        """
        Join a many-to-many mapping of elements to the map.

        `mapping` should be like `dict<key: iterable<value>>`.
        """
        index.update(
            {
                0: {'zero'},
                1: {'1'},
                5: {'five', 'cinco'}
            }
        )
        assert index[0] == {'zero'}
        assert index[1] == {'one', 'uno', 'hana', '1'}
        assert index[5] == {'five', 'cinco'}

    def reverse(index):
        """
        Reverse an index into a `Function` representation.
        """
        f = index.reverse()
        assert f['one'] == 1
        assert f['uno'] == 1
        assert f['five'] == 5
        del f['one']
        assert 'one' not in index[1]


    # @specification.satisfies(functionspec.FunctionSpec.FUNCTION)
    # def REVERSE(Index):
    #     """
    #     Index reverses to a Function.
    #     """
    #     return Index(
    #         {
    #             1: {'one', 'uno'},
    #             2: {'two'}
    #         }
    #     ).reverse()

# functionspec.FunctionSpec.REVERSE = specification.satisfies(IndexSpec.INDEX)
