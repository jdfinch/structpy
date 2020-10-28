

from structpy import specification


@specification
class HimapSpec:
    """
    Finite many-to-many mapping between a domain and domain.
    """

    @specification.init
    def HIMAP(Himap, mapping=None):
        himap = Himap(2, {
            'Mary': {
                'like': {
                    'lot': {'Bob', 'Steve'},
                    'little': {'Carl'}
                },
                'dislike': {
                    'lot': {'Joe'},
                    'little': {'Sally', 'Sam'}
                }
            },
            'Sue': {
                'like': {
                    'lot': {'Joe', 'Jim'},
                    'little': {'Bob'}
                },
                'dislike': {
                    'lot': {'Carl'}
                }
            }
        })
        return himap

    def getitem(himap, item):
        """
        Get a reference to the elements in the codomain associated
        with domain element keys.
        """
        assert himap['Mary', 'like', 'lot'] == {'Bob', 'Steve'}
        assert himap['Mary', 'dislike', 'little'] == {'Sally', 'Sam'}

    def additem(himap, key, values):
        """
        Set the domain elements associated with a key to all the
        elements present in values.

        Each element of values is added to the domain, without
        a direct reference to the provided values object.
        """
        himap['Sue', 'dislike', 'little'] = ['Jason', 'Dave']
        assert himap['Sue', 'dislike', 'little'] == {'Jason', 'Dave'}

        # Overwriting
        himap['Mary', 'like', 'lot'] = ['Jim']
        assert himap['Mary', 'like', 'lot'] != {'Bob', 'Steve'}
        assert himap['Mary', 'like', 'lot'] == {'Jim'}

        # Add from lower level
        himap['Mary', 'like', 'lot'].add('Jason')
        assert himap['Mary', 'like', 'lot'] == {'Jim', 'Jason'}

    def delitem(himap, element):
        """
        Remove an element from the map domain.
        """
        del himap['Sue', 'dislike']
        assert ('Sue', 'dislike') not in himap
        assert ('Sue', 'dislike', 'lot') not in himap
        assert ('Sue', 'dislike', 'little') not in himap

    def update(himap, mapping):
        """
        Join a many-to-many mapping of elements to the map.

        `mapping` should be a dict-like.
        """
        himap.update(
            {
                'Sue': {
                    'dislike': {
                        'little' : {'Jason'}
                    }
                },
                'Mary': {
                    'like': {
                        'lot': {'Joe'}
                    }
                }
            }
        )
        assert himap == {
            'Mary': {
                'like': {
                    'lot': {'Jim', 'Jason', 'Joe'},
                    'little': {'Carl'}
                },
                'dislike': {
                    'lot': {'Joe'},
                    'little': {'Sally', 'Sam'}
                }
            },
            'Sue': {
                'like': {
                    'lot': {'Joe', 'Jim'},
                    'little': {'Bob'}
                },
                'dislike': {
                    'little': {'Jason'}
                }
            }
        }

    def reverse(himap):
        """
        Returns a view of the map that swaps the domain and domain
        for reverse mapping.
        """
        r = himap.reverse()
        assert r == {
            'Jim': {
                'like': {
                    'lot': {'Mary', 'Sue'}
                }
            },
            'Jason': {
                'like': {
                    'lot': {'Mary'}
                },
                'dislike': {
                    'litte': {'Sue'}
                }
            },
            'Joe': {
                'like': {
                    'lot': {'Mary', 'Sue'}
                },
                'dislike': {
                    'lot': {'Mary'}
                }
            },
            'Carl': {
                'Mary': {
                    'like': {
                        'little': {'Mary'}
                    }
                }
            },
            'Sam': {
                'dislike': {
                    'little': {'Mary'}
                }
            },
            'Sally': {
                'dislike': {
                    'little': {'Mary'}
                }
            },
            'Bob': {
                'like': {
                    'little': {'Sue'}
                }
            }
        }
