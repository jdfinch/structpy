from standard.graph.node_graph import NodeGraph
from standard.graph.core.tree import Tree

class NodeTree(NodeGraph, Tree):

    def __init__(self, root=None):
        NodeGraph.__init__(self)
        Tree.__init__(self, root)