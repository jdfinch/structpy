from standard.graph.linked_graph import LinkedGraph
from standard.graph.tree import Tree

class LinkedTree(LinkedGraph, Tree):

    def __init__(self, root=None):
        LinkedGraph.__init__(self)
        Tree.__init__(self, root)