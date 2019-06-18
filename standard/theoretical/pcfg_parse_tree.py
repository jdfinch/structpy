from standard.graph.node_tree import NodeTree

class PcfgParseTree(NodeTree):

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