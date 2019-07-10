
from structpy.graph.flex.flex_forest import FlexForest
from structpy.graph.core.tree import Tree

class FlexTree(FlexForest, Tree):

    def __init__(self, root):
        FlexForest.__init__(self)
        Tree.__init__(self,root)

    def postorder_traverse(self, start):
        """
        Postorder traversal
        :param start: node to start at
        :return: generator of nodes in traversal
        """
        return Tree.postorder_traverse(self, start)

    def traverse(self, start):
        """
        Preorder traversal
        :param start: node to start at
        :return: generator of nodes in traversal
        """
        return Tree.traverse(self, start)
