
from structpy import specification


@specification
class LookupSpec:
    """
    Finite one-to-many mapping between a domain and codomain.
    """

    @specification.init
    def LOOKUP(Lookup, mapping=None):
        """

        """
        lookup = Lookup({
            1: {'one', 'hana', 'uno'},
            2: {'dos', 'two'},
            3: {'three'}
        })
        return lookup

    def getitem(lookup, item):
        """
        Get a reference to the elements in the codomain associated
        with a domain element.
        """
        assert lookup[1] == {'one', 'hana', 'uno'}
        assert lookup[3] == {'three'}

        # Elements can be added individually using the reference.
        lookup[3].add('tres')
        assert 'tres' in lookup[3]

    def delitem(lookup, item):
        """
        Remove an element from the lookup domain.
        """
        del lookup[2]
        assert 2 not in lookup

    def update(lookup, mapping):
        """
        Join a many-to-many mapping of elements to the map.

        `mapping` should be like `dict<key: iterable<value>>`.
        """
        lookup.up
