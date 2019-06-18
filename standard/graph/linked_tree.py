from standard.graph.linked_graph import LinkedGraph
from standard.graph.tree import Tree

class LinkedTree(LinkedGraph, Tree):

    def __init__(self, root=None):
        LinkedGraph.__init__(self)
        Tree.__init__(self, root)

    def get_last_child(self, node):
        epi = None
        for epi in self.epis(node):
            continue
        return epi

    def get_next(self, pcfg):
        parent = self.root()
        last_child = self.get_last_child(parent)
        while not self.is_complete(last_child,pcfg):
            parent = last_child
            last_child = self.get_last_child(parent)
        if self.is_complete(parent,pcfg):
            return None
        return self.next_child(parent, pcfg)