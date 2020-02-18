
from structpy.language import Specification


class Himap(Specification):
    """
    Hierarchical Mapping


    """

    @Specification.example
    def mapping_with_himap(self, Struct):
        himap = Struct({'i': {'like': {'cat', 'bird'}, 'dislike': {'dog'}}, 'you': {'like': {'dog'}}})
        himap['you']['dislike'].add('cat')
        himap['she', 'like'].add('bird')
        assert himap['i', 'like'] == {'cat', 'bird'}
        assert himap['i'] == {'cat', 'bird', 'dog'}
        assert himap['she'] == {'bird'}


