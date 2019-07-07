from structpy.graph.dictionary_graph import DictionaryGraph
from structpy.theoretical.pcfg import NodeType

class Node:

    def __init__(self, value=None):
        self.value = value

    def get_value(self):
        return self.value

    def isalpha(self):
        return self.value.isalpha()

    def __str__(self):
        return '(NODE) ' + str(self.get_value())

    def __repr__(self):
        return str(self)

class NodeGraph(DictionaryGraph):
    """
    Graph structure similar to DictionaryGraph that uses Node objects, not just strings
    Allows for the same node string to appear multiple times in the graph
    """
    def add(self, node, epi=None, arc=None):
        """
        If only 'node' is passed, then
            add a single node to the graph

        If both 'node' and 'epi' are passed, then
            add each (if it is not already in the graph) and
            add an arc between them

        If node or epi is new, then
            it is passed as a string value and
            it is converted into a Node object that is added into the graph
            (can also pass a new node or epi as a Node object and if it is not in the graph, it is added)

        If you want to link between existing nodes in the graph, MUST pass the node object directly
        """
        if epi is not None:
            if type(node) is not Node:
                node = Node(node)
            if not self.has(node):
                self.add_node(node)
            if type(epi) is not Node:
                epi = Node(epi)
            if not self.has(epi):
                self.add_node(epi)
            if arc is None:
                arc = True
            self.add_arc(node, epi, arc)
        else:
            if type(node) is not Node:
                node = Node(node)
            if not self.has(node):
                self.add_node(node)

    def add_node(self, node):
        if type(node) is not Node:
            node = Node(node)
        self._nodes[node] = {}
        return node

    def add_arc(self, pro, epi, arc=True):
        if type(epi) is not Node:
            epi = Node(epi)
        self._nodes[pro][epi] = arc

    def get_node(self, parent, child_value):
        """
        Get the Node object that is a child of the parent and has the desired value
        :param parent: a Node object
        :param child_value: the value of the desired child of the parent
        :return: a Node object if the child value is found in the epis of the parent;
                otherwise, None
        """
        for epi in self.epis(parent):
            if epi.get_value() == child_value:
                return epi
        return None

    def is_complete(self, node, pcfg):
        """
        Determines if the node has all of its children according to the PCFG

        :param node: the Node object to check if it is complete
        :param pcfg: a PCFG object where the nodes are strings
        :return: True if complete; False otherwise
        """
        if not self.has(node):
            return
        if pcfg.node_type(node.get_value()) is NodeType.AND:
            obtained = self.epis_number(node)
            required = pcfg.epis_number(node.get_value())
            if obtained == required:
                for epi in self.epis(node):
                    if not self.is_complete(epi, pcfg):
                        return False
                return True
            else:
                return False
        elif pcfg.node_type(node.get_value()) is NodeType.TERMINAL:
            return True

    def next_child(self, node, pcfg):
        """
        Identifies what children are missing from the node according to the PCFG

        :param node: the Node object to retrieve the next child from
        :param pcfg: a PCFG object where the nodes are strings
        :return: the next child of the node; None if no children left
        """
        return list(pcfg.epis(node.get_value()))[self.epis_number(node)]

