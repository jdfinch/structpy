import structpy.graph.core.dag as dag
from structpy.graph.core.point_tree import PointTree
from abc import ABC

class Tree(dag.Dag, PointTree):
    """
    """

    def __init__(self, root=None):
        PointTree.__init__(self, root)

    def postorder_traverse(self, start):
        """
        Postorder traversal
        :param start: node to start at
        :return: generator of nodes in traversal
        """
        return PointTree.postorder_traverse(self, start)

    def traverse(self, start):
        """
        Preorder traversal
        :param start: node to start at
        :return: generator of nodes in traversal
        """
        return PointTree.traverse(self, start)

    def traverse_reverse(self, start):
        return PointTree.traverse_reverse(self, start)

