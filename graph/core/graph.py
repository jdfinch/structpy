from abc import ABC, abstractmethod
from structpy.utilities.simple import empty_generator
from structpy.graph.core.point_graph import PointGraph
from collections import defaultdict
import os

class Graph(PointGraph, ABC):
    """
    General graph structure

    ## Guidelines:

    - nodes and arcs are assumed to be sets without duplicates

    ## Methods summary:

    ### Graph-level properties:

    - `nodes()`: iterate over nodes
    - `arcs()`: iterate over arcs
    - `has(node, epi=None)`: membership of node or arc by pro & epi
    - `has_node(node)`: node membership
    - `has_arc(pro, epi)`: arc membership by pro & epi
    - `nodes_number()`: count of nodes
    - `arcs_number()`: count of arcs
    
    ### Construction:

    - `add(node, epi=None, arc=None)`: add node, or (pro, epi, arc)
    - `add_node(node)`: add node
    - `add_arc(pro, epi, arc=True)`: add arc

    ### Destruction:

    - `remove(node, epi=None)`: remove node, or arc by pro & epi
    - `remove_node(node)`: remove node
    - `remove_arc(pro, epi)`: remove arc by pro and epi

    ### Mutation:

    - `replace_node(old, new)`: replace a node while preserving its arcs
    - `replace_arc(pro, epi, new)`: replace an arc by its node endpoints
    - `replace_pro(pro, epi, new_pro)`: change the pro of an arc
    - `replace_epi(pro, epi, new_epi)`: change the epi of an arc

    ### Properties for finding nodes:

    - `epis(node)`: iterate over epis of a node
    - `pros(node)`: iterate over pros of a node
    - `epis_number(node)`: returns a count of a node's epis
    - `pros_number(node)`: returns a count of a nodes's pros

    ### Properties for finding arcs:

    - `arc(pro, epi)`: returns the arc from pro to epi
    - `arcs_out(node)`: iterate over the arcs the node is the pro of
    - `arcs_in(node)`: iterate over the arcs the node is an epi of

    ### Graph navigation:

    - `traverse(frontier, start)`: traversal that yields visited nodes
    - `search(frontier, start)`: search that returns a solution Sequence
    - `explore(frontier, start)`: search that yields multiple solutions
    - `traverse_reverse(frontier, start)`
    - `search_reverse(frontier, start)`
    - `explore_reverse(frontier, start)`

    ## Implementation patterns:

    ### Node-based:

    1. Implement `nodes` to iterate (use an iterable or a generator
    implementation) over nodes. Alternatively, assign `self._nodes` to a 
    collection to hold nodes

    2. Implement `add_node(node)` and `add_arc(arc)` (alternatively, 
    if you assign `self._nodes` to a collection that implements 
    `.add(e)` and `.pop(e)` to add/remove element e, you may skip
    this step)

    3. Implement `arc(pro, epi)` to return the arc from pro to epi, or None
    if none exists. Return True for label-less arcs.

    4. If you want to be able to remove things from the graph, implement
    `remove_node` and `remove_arc`

    4. If you want to improve the efficiency of other methods, you
    can re-implement them. Especially, the default implementations of
    the following methods may be inefficient, although they will work
    if the above 3 steps have been followed:

        - `epis`
        - `pros`
        - `pro`
        - `epi`
        - `arcs`

    ### Arc-based:

    1. lorem ipsum

    ### 
    """

    @abstractmethod
    def __init__(self):
        Graph.__init__(self)
        self._arcs = set()
        raise NotImplementedError(
            "Graph is abstract and cannot be initialized; \
            use one of its implementations (or make your own!)")

    def arcs(self):
        """
        Iterates over all arcs in the graph

        Guideline implementation: return tuples in form (pro, epi, arc_value)

        Default implementation: iterates over every pair of nodes and checks
        if there is an arc between them using `self.arc(n1, n2)`. 
        O(N * N * T(`self.arc`))
        """
        for pro in self.nodes():
            for epi in self.nodes():
                arc = self.arc(pro, epi)
                if arc is not None:
                    yield (pro, epi, arc)

    def arcs_out(self, node):
        """
        Iterates over the arcs that the node is a pro of

        Should yield arcs in the same order as epis are yielded by `self.epis`

        Default implementation: iterates over `self.epis()`.
        O(T(`self.epis`))
        """
        for other in self.epis(node):
            yield self.arc(node, other)

    def arcs_in(self, node):
        """
        Iterates over the arcs that the node is an epi of

        Should yield arcs in the same order corresponding to `self.pros`

        Default implementation: iterates over `self.epis()`.
        O(T(`self.epis`))
        """
        for other in self.pros(node):
            yield self.arc(other, node)

    def arc(self, pro, epi):
        """
        Returns the arc from pro to epi, or None if none exists

        Guideline implementation: return a tuple `(pro, epi, arc_value)`, or
        `(pro, epi)` if the arc is valueless

        Default implementation: iterates over `self.arcs()` and returns an arc
        where `self.pro(arc)` and `self.epi(arc)` match pro and epi 
        respectively. O(T(`self.pro`) * T(`self.epi`) * T(`self.arc`))
        """
        for arc in self.arcs():
            if self.pro(arc) is pro and self.epi(arc) is epi:
                return arc

    def has_arc(self, pro, epi):
        """
        Returns boolean indicating whether the graph contains arc

        Default implementation: routes to `self.arc`
        O(T(`self.arc`))
        """
        return self.arc(pro, epi) is not None

    def has_arc_value(self, arc):
        """
        Returns boolean indicating whether the graph contains arc

        Default implementation: iterates over arcs to check against arc.
        O(T(`self.arcs`))
        """
        for e in self.arcs():
            if e[2] is arc:
                return True
        return False

    def pros(self, node, arc_value=None):
        """
        Get the pros of the node, optionally filtering by an arc value
        :param node: node in the graph
        :param arc_value: value that arcs have to be equal to between this
                          node and the pro for the pro to be yielded
        :return: generator over pros
        """
        if arc_value is None:
            yield from PointGraph.pros(self, node)
        for pro in PointGraph.pros(self, node):
            if self.arc(pro, node) == arc_value:
                yield pro

    def epis(self, node, arc_value=None):
        """
        Get the epis of the node, optionally filtering by an arc value
        :param node: node in the graph
        :param arc_value: value that arcs have to be equal to between this
                          node and the epi for the epi to be yielded
        :return: generator over epis
        """
        if arc_value is None:
            yield from PointGraph.epis(self, node)
        for epi in PointGraph.epis(self, node):
            if self.arc(node, epi) == arc_value:
                yield epi

    def epis_number(self, node, arc_value=None):
        """
        Return the number of epis of node

        Default implementations: iterate and count `self.epis(node)`.
        O(T(`self.epis`))
        """
        i = 0
        for epi in self.epis(node, arc_value):
            i += 1
        return i

    def pros_number(self, node, arc_value=None):
        """
        Return the number of pros of node

        Default implementations: iterate and count `self.pros(node)`.
        O(T(`self.pros`))
        """
        i = 0
        for pro in self.pros(node, arc_value):
            i += 1
        return i
    
    def add(self, node, epi=None, arc=None):
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
            if arc is None:
                arc = True
            self.add_arc(node, epi, arc)
        else:
            if not self.has_node(node):
                self.add_node(node)

    def add_pros(self, pros, node, arcs=None):
        """
        Add all pros as pros of node
        :param pros: nodes iterable, preexisting or not
        :param node: epi node
        :param arcs: iterable over arcs, same length as pros
        :return: None
        """
        if arcs is None:
            arcs = [True for _ in pros]
        for pro in pros:
            self.add(pro, node, next(arcs))

    def add_epis(self, node, epis, arcs=None):
        """
        Add all epis as epi of node
        :param node: pro node
        :param epis: epis to add
        :param arcs: iterable over arcs, same length as epis
        :return: None
        """
        if arcs is None:
            arcs = [True for _ in epis]
        for epi in epis:
            self.add(node, epi, next(arcs))

    def replace_pro(self, pro, epi, new_pro):
        arc = self.arc(pro, epi)
        self.remove_arc(pro, epi)
        self.add_arc(new_pro, epi, arc)

    def replace_epi(self, pro, epi, new_epi):
        arc = self.arc(pro, epi)
        self.remove_arc(pro, epi)
        self.add_arc(pro, new_epi, arc)

    def add_arc(self, pro, epi, arc=True):
        """
        Add an arc from pro to epi to the graph. By default, unlabeled arcs are
        valued True. Does not add pro or epi to the graph explicitly

        Default implementation: calls `self._arcs.add((pro, epi, arc))`
        """
        self._arcs.add((pro, epi, arc))

    def replace_arc(self, pro, epi, new):
        """
        Replace the value of the arc specified by pro and epi with new
        """
        self.remove_arc(pro, epi)
        self.add_arc(pro, epi, new)

    def replace_node(self, old, new):
        """
        replace old node with new while preserving arcs and their types
        :param new:
        :param old:
        :return:
        """
        if not self.has_node(new):
            self.add_node(new)
        for pro in self.pros(old):
            arc = self.arc(pro, old)
            self.add_arc(pro, new, arc)
        for epi in self.epis(old):
            arc = self.arc(old, epi)
            self.add_arc(new, epi, arc)
        self.remove_node(old)


    def traverse(self, frontier, start=None):
        """
        Traverses the graph starting at `start` and yields each visited node,
        including `start`

        Node expansion is determined by the arcs in this graph, namely the 
        `.epis` method

        Expansion order and stop conditions are determined by `frontier`,
        which should be a `Frontier` Tree or Sequence
        """
        if start is not None:
            frontier.add(start)
        while not frontier.complete():
            new = frontier.pop()
            yield new
            for epi in self.epis(new):
                frontier.add(epi)

    def search(self, frontier):
        """
        Returns a `Sequence` representing a solution path in the graph
        for the goal specified by `frontier`

        `frontier`: a search tree frontier structure
        """
        new = frontier.root() # assume root is already popped off
        while not frontier.complete():
            frontier.add_epis(new, self.epis(new), self.arcs_out(new))
            new = frontier.pop()
        return frontier.result()

    def explore(self, frontier, start):
        """
        """
        pass

    def traverse_reverse(self, frontier, start):
        """
        """
        pass

    def search_reverse(self, frontier):
        """
        Returns a `Sequence` representing a solution path in the graph
        for the goal specified by `frontier`

        `frontier`: a search tree frontier structure
        """
        new = frontier.root()
        while not frontier.complete():
            frontier.add_epis(new, self.pros(new), self.arcs_in(new))
            new = frontier.pop()
        return frontier.result()

    def explore_reverse(self, frontier, start):
        """
        """
        pass

    def save(self, filename):
        pass

    def load(self, filename, node_fun=None, arc_fun=None):
        if filename[-4:] != '.lgt':
            filename += '.lgt'

        with open(filename) as file:
            pro = None
            arc = None
            for line in file:
                if line.strip() != "":
                    tabs = 0
                    while line[tabs] == '\t':
                        tabs += 1
                    if len(line) == 0 or line[tabs] == '#':
                        continue
                    if line[tabs] == '\\' and len(line) > 1 \
                            and line[tabs + 1] == '#':
                        line = line[:tabs] + line[tabs + 1:]
                    if tabs == 0:
                        pro = line.strip()
                    elif tabs == 1:
                        arc = line.strip()
                    elif tabs == 2:
                        epi = line.strip()
                        if node_fun is not None:
                            pro = node_fun(pro)
                            epi = node_fun(epi)
                        if arc_fun is not None:
                            arc = arc_fun(arc)
                        self.add(pro, epi, arc)
        return self

    def save(self, filename, node_fun=None, arc_fun=None):
        if filename[-4:] != '.lgt':
            filename += '.lgt'
        with open(filename, 'w') as file:
            for pro in self.nodes():
                links = defaultdict(list)
                for epi in self.epis(pro):
                    arc_val = self.arc(pro, epi)
                    links[arc_val].append(epi)
                file.write(pro+'\n')
                for link,epis in links.items():
                    file.write('\t'+link+'\n')
                    for epi in epis:
                        file.write('\t\t'+epi+'\n')
                file.write('\n')







