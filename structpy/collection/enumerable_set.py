
from structpy.language import specification, implementation


@specification
class EnumerableSet:

    @specification.init
    def init(set, iterator=None, membership=None):
        pass