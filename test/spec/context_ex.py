"""
Map

Mapping between keys and values.
"""

from structpy.specification.specification import Spec


MapSpec = Spec()
with MapSpec.params:
    Map = ...
    map = ...

with MapSpec:

    def __init__(self):
        """
        Constructor for Map.
        """
        global map
        map = Map((
            (1, 'one'),
            (2, 'two')
        ))

    def update(self, items):
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

    def __contains__(self, item):
        """
        Check if a key is in Map.
        """
        assert 1 in map
        assert 3 not in map


if __name__ == '__main__':

    MapSpec.implementation(dict)
    MapSpec.implementation(list)
    MapSpec.implementation(set)
    results = MapSpec.run()
