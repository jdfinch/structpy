
from structpy import specification


@specification
class MapSpec:
    """
    Finite many-to-many mapping between a domain and codomain.
    """

    @specification.init
    def MAP(Map, mapping=None):
        map = Map({
                'avengers': {'scarlett', 'chris'},
                'marriage story': {'scarlett', 'adam'},
                'star wars': {'adam'}
            })
        return map

    def getitem(map, item):
        """
        Get a reference to the elements in the codomain associated
        with domain element item.
        """
        assert map['avengers'] == {'scarlett', 'chris'}
        assert map['star wars'] == {'adam'}

        # Elements can be added individually using the reference
        map['avengers'].add('robert')
        assert map['avengers'] == {'scarlett', 'chris', 'robert'}

    def setitem(map, key, values):
        """
        Set the codomain elements associated with a key to all the
        elements present in values.

        Each element of values is added to the codomain, without
        a direct reference to the provided values object.
        """
        map['star wars'] = ['adam', 'daisy']
        assert map['star wars'] == {'adam', 'daisy'}

    def reverse(map):
        """
        Returns a view of the map that swaps the domain and codomain
        for reverse mapping.
        """
        r = map.reverse()
        assert r['chris'] == {'avengers'}
        assert r['adam'] == {'marriage story', 'star wars'}
