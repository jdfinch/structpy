
from structpy.graph.flex.flex_forest import FlexForest
from structpy.graph.core.tree import Tree

class FlexTree(FlexForest, Tree):

    def __init__(self, root):
        FlexForest.__init__(self)
        Tree.__init__(self,root)

    def postorder_traversal(self, start):
        pass

    def traverse(self, start):
        return Tree.traverse(self, start)
