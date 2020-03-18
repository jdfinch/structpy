
from structpy.language import Specification, Implementation


@Specification
class EnumerableSet:

    @Specification.construction
    def init(set, iterator=None, membership=None):
        pass