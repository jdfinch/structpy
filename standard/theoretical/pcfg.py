
from standard.graph.typed_node_graph import TypedNodeGraph
from standard.graph.bidictionary_graph import BidictionaryGraph

from enum import Enum

class NodeType(Enum):
    TERMINAL = 0
    AND = 1
    OR = 2

class _Node:

    def __init__(self, value=None):
        if value is None:
            self.node_type = NodeType.AND
        if value.islower():
            self.node_type = NodeType.TERMINAL
        elif value.isupper():
            self.node_type = NodeType.OR
        self.value = value

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return self.value.__hash__()

    def __str__(self):
        return str(self.value) + ': ' + str(self.node_type)
    

class Pcfg(TypedNodeGraph):

    @staticmethod
    def from_string(string):
        """
        Creates a PCFG from a string, with expansion rules like

        A -> NONTERM OTHER | terminal_thing A other_thing | B x D
        """
        pcfg = Pcfg()
        rules = string.split('\n')
        for j in range(len(rules)):
            rule = rules[j].strip()
            lhs, rhs = tuple(rule.split(' -> '))
            productions = rhs.split(' | ')
            for i in range(len(productions)):
                productions_list = productions[i].split()
                productions[i] = (productions_list[:-1], float(productions_list[-1]))
            i = 0
            for production in productions:
                production_list, prob = production
                and_node = lhs+str(i)
                pcfg.add(lhs, and_node, prob)
                for symbol in production_list:
                    pcfg.add(and_node, symbol)
                i += 1
        return pcfg
        
    def __init__(self):
        self._nodes = {}
        self._reverse = {}

    def node_type(self, node):
        if not node.isalpha():
            return NodeType.AND
        if node.islower():
            return NodeType.TERMINAL
        elif node.isupper():
            return NodeType.OR

    def arcs(self):
        for node in self._nodes:
            epis = self._nodes[node]
            if type(epis) == list:
                i = 0
                for epi in epis:
                    yield (node, epi, i)
                    i += 1
            elif type(epis) == dict:
                for epi in epis:
                    yield (node, epi, epis[epi])
            else:
                return
    
    def has_node(self, node):
        return node in self._nodes

    def has_arc(self, pro, epi):
        return pro in self._nodes and epi in self._nodes[pro]

    def nodes_number(self):
        return len(self._nodes)

    def add_node(self, node: str):
        if self.node_type(node) is NodeType.AND:
            self._nodes[node] = []
        elif self.node_type(node) is NodeType.TERMINAL:
            self._nodes[node] = None
        elif self.node_type(node) is NodeType.OR:
            self._nodes[node] = {}
        self._reverse[node] = set()

    def add_arc(self, pro, epi, arc=True):
        if self.node_type(pro) is NodeType.AND:
            self._nodes[pro].append(epi)
        elif self.node_type(pro) is NodeType.TERMINAL:
            raise ValueError()
        elif self.node_type(pro) is NodeType.OR:
            self._nodes[pro][epi] = arc
        self._reverse[epi].add(pro)

    def epis(self, node):
        for epi in self._nodes[node]:
            yield epi

    def pros(self, node):
        for pro in self._reverse[node]:
            yield pro

    def epis_number(self, node):
        return len(self._nodes[node])

    def pros_number(self, node):
        return len(self._reverse[node])

    def pro(self, arc):
        raise NotImplementedError()

    def epi(self, arc):
        raise NotImplementedError()

    def arc(self, pro, epi):
        if self.node_type(pro) is NodeType.AND:
            return self._nodes[pro].index(epi)
        elif self.node_type(pro) is NodeType.OR:
            return self._nodes[pro][epi]

    
    
