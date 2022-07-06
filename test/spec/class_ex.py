
from structpy.specification.specification import Spec; Spec = ...


@Spec.cls
class Map:
    """
    Map

    Mapping between keys and values.
    """

    def Map(map):
        """
        Constructor for Map.
        """
        map = Map((
            (1, 'one'),
            (2, 'two')
        ))
        return map

    def update(map, items):
        """
        Add items to Map.
        """
        map.update((
            (3, 'three'),
            (4, 'four')
        ))
        assert 3 in map
        assert 4 in map
        assert 5 not in map

        map.update({
            5: 'five',
            6: 'six'
        })
        assert 5 in map
        assert 6 in map
        assert 7 not in map

    def __contains__(map, item):
        """
        Check if a key is in Map.
        """
        assert 1 in map
        assert 3 not in map


if __name__ == '__main__':

    Map.implementation(dict)
    Map.implementation(list)
    Map.implementation(set)
    results = Map.run()
