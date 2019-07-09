import structpy.graph.core.dag as dag
from structpy.graph.core.point_tree import PointTree
from abc import ABC

class Tree(dag.Dag, PointTree):
    """
    """

    def __init__(self, root=None):
        PointTree.__init__(self, root)

    def traverse(self, start):
        return PointTree.traverse(self, start)

    def traverse_reverse(self, start):
        return PointTree.traverse_reverse(self, start)

