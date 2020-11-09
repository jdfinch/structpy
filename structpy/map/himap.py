
from structpy import implementation
from structpy.map.himap_spec import HimapSpec

from structpy.collection import Hidir


@implementation(HimapSpec)
class Himap:

    def __init__(self, order, mapping=None):
        self._hidir = Hidir(order)
        if isinstance(mapping, Himap) and not hasattr(mapping, 'reverse'):
            self.reverse = mapping
        else:
            self.reverse = Himap(order)
            self.update(mapping)

    def __getitem__(self, item):
        pass


class HimapView:

    def __init__(self):
        pass



if __name__ == '__main__':
    print(HimapSpec.verify(Himap))