from structpy.graph.pointer_graph import PointerGraph
from structpy.graph.core.tree import Tree


class PointerTree(PointerGraph, Tree):

    def __init__(self, root=None):
        PointerGraph.__init__(self)
        Tree.__init__(self, root)

