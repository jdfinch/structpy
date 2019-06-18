from standard.graph.node_tree import NodeTree

class PcfgParseTree(NodeTree):

    def get_last_child(self, node):
        epi = None
        for epi in self.epis(node):
            continue
        return epi

    def get_next(self, pcfg):
        """
        Finds the next child that needs to be accounted for in the parse tree based on the PCFG

        :param pcfg: a PCFG where the nodes are strings
        :return: a Node object of the parent from the parse tree that produced the need for the child &
                 a string representing the child that is needed based on the PCFG
        """
        parent = self.root()
        last_child = self.get_last_child(parent)
        while not self.is_complete(last_child,pcfg):
            parent = last_child
            last_child = self.get_last_child(parent)
        if self.is_complete(parent,pcfg):
            return None, None
        return parent, self.next_child(parent, pcfg)