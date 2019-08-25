from abc import ABC, abstractmethod
from structpy.utilities.simple import empty_generator
from structpy.collection.stack import Stack

class PointGraph(ABC):

    @abstractmethod
    def __init__(self):
        self._nodes = set()
        self._arcs = set()
        raise NotImplementedError(
            "Graph is abstract and cannot be initialized; \
            use one of its implementations (or make your own!)")

    def nodes(self):
        """
        :return: generator over nodes in this Graph
        """
        for node in self._nodes:
            yield node

    def arcs(self):
        """
        Iterates over all arcs in the graph

        Guideline implementation: return tuples in form (pro, epi)

        Default implementation: iterates over every pair of nodes
        """
        for pro in self.nodes():
            for epi in self.nodes():
                if self.has_arc(pro, epi):
                    yield (pro, epi)

    def nodes_number(self):
        """
        Returns the number of nodes in the graph

        Default implementation: counts number of nodes O(N)
        """
        i = 0
        for node in self.nodes():
            i += 1
        return i

    def arcs_number(self):
        """
        Returns the number of arcs in the graph

        Default implementation: counts the number of arcs O(A)
        """
        i = 0
        for arc in self.arcs():
            i += 1
        return i

    def has_node(self, node):
        """
        Returns boolean indicating whether the graph contains node

        Default implementation: iterates over nodes to check against node.
        O(T(`self.nodes`))
        """
        for n in self.nodes():
            if n is node:
                return True
        return False

    def has_arc(self, pro, epi):
        """
        Returns boolean indicating whether the graph contains arc

        Default implementation: routes to `self.arc`
        O(T(`self.arc`))
        """
        return (pro, epi) in self._arcs

    def has(self, node, epi=None):
        """
        Returns boolean indicating whether the graph contains node

        If epi is specified, instead returns whether an arc exists from pro to
        epi

        Default implementation: routes to either `self.has_node` or `self.arc`
        """
        if epi is None:
            return self.has_node(node)
        else:
            return self.has_arc(node, epi)

    def add_node(self, node):
        """
        Add a node to the graph, initialized without any arcs

        Default implementation: calls `self._nodes.add(node)`
        """
        self._nodes.add(node)

    def add_arc(self, pro, epi):
        """
        Add an arc from pro to epi to the graph. By default, unlabeled arcs are
        valued True. Does not add pro or epi to the graph explicitly

        Default implementation: calls `self._arcs.add((pro, epi, arc))`
        """
        self._arcs.add((pro, epi))

    def add(self, node, epi=None):
        """
        Add node and epi to the graph (caution, if already existing they will
        be added as duplicates in certain implementations). If epi is specified,
        an arc from node to epi will also be added with value arc

        Default implementation: routes to `self.add_node` and `self.add_arc`
        """
        if epi is not None:
            if not self.has_node(node):
                self.add_node(node)
            if not self.has_node(epi):
                self.add_node(epi)
            self.add_arc(node, epi)
        else:
            if not self.has_node(node):
                self.add_node(node)

    def add_pros(self, pros, node):
        """
        Add all pros as pros of node
        :param pros: nodes, preexisting or not
        :param node: epi node
        :return: None
        """
        for pro in pros:
            self.add(pro, node)

    def add_epis(self, node, epis):
        """
        Add all epis as epi of node
        :param node: pro node
        :param epis: epis to add
        :return: None
        """
        for epi in epis:
            self.add(node, epi)

    def epis(self, node):
        """
        Return the epis that node has arcs to

        Default implementation: iterate through `self.nodes()` and check if
        there is an arc from node to other_node using `self.arc(other_node, node)`
        O(T(`self.nodes`) * T(`self.arc`))
        """
        for n in self.nodes():
            if self.has_arc(node, n):
                yield n

    def pros(self, node):
        """
        Return the pros that have arcs where node is the epi

        Default implementation: iterate through `self.nodes()` and check if
        there is an arc from node to other_node using `self.arc(node, other_node)`
        O(T(`self.nodes`) * T(`self.arc`))
        """
        for n in self.nodes():
            if self.has_arc(n, node):
                yield n

    def epis_number(self, node):
        """
        Return the number of epis of node

        Default implementations: iterate and count `self.epis(node)`.
        O(T(`self.epis`))
        """
        i = 0
        for epi in self.epis(node):
            i += 1
        return i

    def pros_number(self, node):
        """
        Return the number of pros of node

        Default implementations: iterate and count `self.pros(node)`.
        O(T(`self.pros`))
        """
        i = 0
        for pro in self.pros(node):
            i += 1
        return i

    def remove(self, node, epi=None):
        """
        With one argument, removes a node from the graph.

        With two arguments, removes the arc from node to epi

        Default implementation: routes to `self.remove_node` and `self.remove_arc`
        """
        if epi is None:
            return self.remove_node(node)
        else:
            return self.remove_arc(node, epi)

    def remove_node(self, node):
        """
        Remove node from the graph
        """
        self._nodes.pop(node)

    def remove_arc(self, pro, epi):
        """
        Remove an arc from the graph by specifying its pro and epi
        """
        self._arcs.remove((pro, epi))

    def replace_node(self, old, new):
        """
        Replace the value of the node old with new, while preserving all
        node arcs
        """
        if not self.has_node(new):
            self.add_node(new)
        for pro in list(self.pros(old)):
            self.replace_epi(pro, old, new)
        for epi in list(self.epis(old)):
            self.replace_pro(old, epi, new)
        self.remove_node(old)

    def replace_pro(self, pro, epi, new_pro):
        """
        Change the epi of the arc specified by pro and epi to new_epi
        """
        self.remove_arc(pro, epi)
        self.add_arc(new_pro, epi)

    def replace_epi(self, pro, epi, new_epi):
        """
        Change the pro of the arc specified by pro and epi to new_epi
        """
        self.remove_arc(pro, epi)
        self.add_arc(pro, new_epi)

    def traversal_preorder(self, node):
        """
        Traverse the graph in pre-order without re-visiting nodes
        :param node: starting node
        :return: generator over traversal
        """
        visited = {node}
        s = Stack([node])
        while s:
            node = s.pop()
            yield node
            for epi in self.epis(node):
                if epi not in visited:
                    s.add(epi)
                    visited.add(epi)

    def copy(self):
        """
        Create a shallow copy of this graph: nodes are preserved,
        but the structure of the graph to maintain arcs, etc. is
        duplicated
        :return: a copy, same type as self
        """
        cls = self.__class__
        copy = cls()
        for node in self.nodes():
            copy.add_node(node)
        for arc in self.arcs():
            copy.add_arc(*arc)
        return copy


    def __eq__(self, other):
        """
        Checks set equality between this graph and graph other
        """
        arcs = set(self.arcs())
        nodes = set(self.nodes())
        other_arcs = set(other.arcs())
        other_nodes = set(other.nodes())
        return arcs == other_arcs and nodes == other_nodes

    def display(self, node=None):
        visited = set()
        while len(set(x[0] for x in visited)) != len(list(self.nodes())):
            if node is None:
                node_itr = self.nodes()
                node = next(node_itr)
                while node in set(x[0] for x in visited):
                    node = next(node_itr)
            tab = 0
            visited.add((node, tab))
            s = Stack([(node, tab)])
            while s:
                node = s.pop()
                print('\t'*node[1]+str(node[0]))
                tab += 1
                for epi in self.epis(node):
                    if epi not in visited:
                        s.add((epi,tab))
                        visited.add((epi,tab))
            node = None