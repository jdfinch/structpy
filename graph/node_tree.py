from structpy.graph.node_graph import NodeGraph
from structpy.graph.core.tree import Tree

class NodeTree(NodeGraph, Tree):

    def __init__(self, root=None):
        NodeGraph.__init__(self)
        Tree.__init__(self, root)