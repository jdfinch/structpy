
from structpy.language import spec, Implementation


@spec
class EnumerableSet:

    @spec.init
    def init(set, iterator=None, membership=None):
        pass