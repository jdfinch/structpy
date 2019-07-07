from structpy.graph.list_graph import ListGraph
from structpy.graph.core.tree import Tree

class ListTree(ListGraph, Tree):

    def __init__(self, root):
        ListGraph.__init__(self)
        Tree.__init__(self, root)