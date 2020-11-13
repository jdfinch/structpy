
from structpy import specification
# import structpy.map.function.function_spec as functionspec


@specification
class HiindexSpec:
    """
    Finite one-to-many hierarchichal mapping between a domain and codomain.
    """

    @specification.init
    def HIINDEX(Hiindex, mapping=None):
        hiindex = Hiindex(2, {
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
                'dislike': {
                    'lot': {'Mary'},
                    'little': {'Sue'}
                }
            }
        })
        return hiindex

    def getitem(hiindex, item):
        """
        Get a reference to the elements in the codomain associated
        with a domain element.
        """
        assert hiindex['Steve', 'like', 'lot'] == {'Mary', 'Sue'}
        assert hiindex['Carl', 'like', 'little'] == {'Mary'}

    def additem(hiindex, key, values):
        """
        Set the domain elements associated with a key to all the
        elements present in values.

        Each element of values is added to the domain, without
        a direct reference to the provided values object.
        """
        hiindex['Steve', 'like', 'little'] = ['Jon', 'Sue']
        assert hiindex['Steve', 'like', 'little'] == {'Jon', 'Sue'}

        # Many-to-one consistency enforced when adding
        hiindex['Carl', 'like', 'lot'] = {'Mary'}
        assert hiindex['Carl', 'like', 'lot'] == {'Mary'}
        assert 'Mary' not in hiindex['Steve', 'like', 'lot']

    def delitem(hiindex, item):
        """
        Remove an element from the hiindex domain.
        """
        del hiindex['Joe', 'dislike']
        assert 'dislike' not in hiindex['Joe']
        assert hiindex['Joe'] == {}

    def update(hiindex, mapping):
        """
        Join a many-to-many mapping of elements to the map.

        `mapping` should be like `dict<key: iterable<value>>`.
        """
        hiindex.update({
            'Steve': {
                'like': {
                    'little': {'Rob'}
                }
            },
            'Joe': {
                'like': {
                    'little': {'Mark'}
                }
            }
        })
        assert hiindex == {
            'Steve': {
                'like': {
                    'lot': {'Sue'},
                    'little': {'Jon', 'Sue', 'Rob'}
                }
            },
            'Carl': {
                'like': {
                    'little': {'Mary'},
                    'lot': {'Mary'}
                }
            },
            'Joe': {
                'like': {
                    'little': {'Mark'}
                }
            }
        }

    def reverse(hiindex):
        """
        Reverse an hiindex into a `Function` representation.
        """
        f = hiindex.reverse()
        comparison = {
            'Sue': {
                'like': {
                    'lot': 'Steve',
                    'little': 'Steve'
                },
                'dislike': {}
            },
            'Jon': {
                'like': {
                    'little': 'Steve'
                }
            },
            'Mary': {
                'like': {
                    'lot': 'Carl',
                    'little': 'Carl'
                },
                'dislike': {}
            },
            'Mark': {
                'like': {
                    'little': 'Joe'
                }
            },
            'Rob': {
                'like': {
                    'little':
                        'Steve'
                }
            }
        }
        assert f == comparison


    # @specification.satisfies(functionspec.FunctionSpec.FUNCTION)
    # def REVERSE(Hiindex):
    #     """
    #     Hiindex reverses to a Function.
    #     """
    #     return Hiindex(
    #         {
    #             1: {'one', 'uno'},
    #             2: {'two'}
    #         }
    #     ).reverse()

# functionspec.FunctionSpec.REVERSE = specification.satisfies(HiindexSpec.HIINDEX)
