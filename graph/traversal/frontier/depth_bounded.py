
from structpy import I

def DepthBounded(frontier_cls, depth):

    class DepthBoundedFrontier(frontier_cls):

        def __init__(self, *args, **kwargs):
            self._depth = 0
            self._max_depth = depth
            frontier_cls.__init__(self, *args, **kwargs)

        def add(self, item):
            if self._depth <= self._max_depth:
                item = I(
                    item,
                    depth=(lambda this: depth)
                )
                frontier_cls.add(self, item)

        def get(self):
            item = frontier_cls.get(self)
            d = item.depth()
            self._depth = d + 1
            return item

    return DepthBoundedFrontier

