
from structpy import specification
# import structpy.map.index.index_spec as indexspec


@specification
class HifunctionSpec:
    """
    Many-to-one hierarchichal mapping between elements in a domain to elements in a codomain.
    """

    @specification.init
    def HIFUNCTION(Hifunction, mapping=None):
        hifunction = Hifunction(2, {
            'Mary': {
                'like': {
                    'lot': 'Steve',
                    'little': 'Carl'
                },
                'dislike': {
                    'lot': 'Joe',
                }
            },
            'Sue': {
                'like': {
                    'lot': 'Steve',
                },
                'dislike': {
                    'little': 'Joe'
                }
            }
        })
        return hifunction

    def getitem(hifunction, item):
        """
        Get the value in the domain associated with a domain keys.
        """
        assert hifunction['Mary', 'like', 'lot'] == 'Steve'
        assert hifunction['Sue', 'dislike', 'little'] == 'Joe'

    def setitem(hifunction, key, value):
        """
        Add a keys pair that co-map.
        """
        hifunction['Sue', 'like', 'little'] = 'Chris'
        assert hifunction['Sue', 'like', 'little'] == 'Chris'

        # overwrite key-value pair
        hifunction['Sue', 'like', 'little'] = 'Carl'
        assert hifunction['Sue', 'like', 'little'] == 'Carl'

    def delitem(hifunction, element):
        """
        Remove an keys pair from the hifunction by key (domain element).
        """
        del hifunction['Sue', 'dislike']
        assert 'dislike' not in hifunction['Sue']

    def update(hifunction, mapping):
        hifunction.update({
            'Sue': {
                'like': {
                    'little': 'Joe'
                },
                'dislike': {
                    'little': 'Carl'
                }
            }
        })
        assert hifunction == {
            'Mary': {
                'like': {
                    'lot': 'Steve',
                    'little': 'Carl'
                },
                'dislike': {
                    'lot': 'Joe',
                }
            },
            'Sue': {
                'like': {
                    'lot': 'Steve',
                    'little': 'Joe'
                },
                'dislike': {
                    'little': 'Carl'
                }
            }
        }

    def reverse(hifunction):
        """
        Reverses a `Hifunction` into an `Index` representation.
        """
        idx = hifunction.reverse()
        assert idx == {
            'Steve': {
                'like': {
                    'lot': {'Mary', 'Sue'}
                }
            },
            'Carl': {
                'like': {
                    'little': {'Mary'}
                }
            },
            'Joe': {
                'like': {
                    'little': {'Sue'}
                },
                'dislike': {
                    'lot': {'Mary'}
                }
            }
        }

    # @specification.satisfies(indexspec.IndexSpec.INDEX)
    # def REVERSE(Hifunction):
    #     """
    #     Returns a index (one-to-many mapping) representing
    #     a hifunction with domain and codomain swapped.
    #     """
    #     return Hifunction({
    #         'one': 1,
    #         'hana': 1,
    #         'uno': 1,
    #         'dos': 2,
    #         'two': 2,
    #         'three': 3
    #     }).reverse()






