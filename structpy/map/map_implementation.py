
from structpy import implementation
from structpy.map.map_spec import MapSpec

from structpy.collection.enforcer import EnforcerDict


@implementation(MapSpec)
class Map:

    def __init__(self, dict_like=None):
        if dict_like is None:
            dict_like = {}
        self.domain = EnforcerDict(
            add_function=None,
            remove_function=None
        )
        self.codomain = EnforcerDict(
            add_function=None,
            remove_function=None
        )



if __name__ == '__main__':
    print(MapSpec.verify(Map))
