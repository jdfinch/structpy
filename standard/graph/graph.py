class Graph:
    """
    General graph structure

    **Abstract Class**

    ## Methods summary:

    ### Graph-level properties:

    - `nodes()`: iterate over nodes
    - `arcs()`: iterate over arcs
    - `has(node, epi=None)`: membership of node or arc by pro & epi
    - `has_node(node)`: node membership
    - `has_arc(arc)`: arc membership by arc value
    - `number_nodes()`: count of nodes
    - `number_arcs()`: count of arcs
    
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
    - `replace_arc_pro(pro, epi, new_pro)`: change the pro of an arc
    - `replace_arc_epi(pro, epi, new_epi)`: change the epi of an arc

    ### Properties for finding nodes:

    - `epis(node)`: iterate over epis of a node
    - `pros(node)`: iterate over pros of a node
    - `pro(arc)`: returns the pro of an arc
    - `epi(arc)`: returns the epi of an arc
    - `epis_number(node)`: returns a count of a node's epis
    - `pros_number(node)`: returns a count of a nodes's pros

    ### Properties for finding arcs:

    - `arc(pro, epi)`: returns the arc from pro to epi
    - `arcs_out(node)`: iterate over the arcs the node is the pro of
    - `arcs_in(node)`: iterate over the arcs the node is an epi of
    - `arcs_out_number(node)`: count of the arcs the node is the pro of
    - `arcs_in_number(node)`: count of the arcs the node is an epi of

    ### Graph navigation:

    - `traverse(start, frontier, condition=None)`: memoryless node traversal
    - `search(start, frontier, end_condition, condition)`: path search
    - `explore(start, frontier, end_condition, condition)`: generator search

    ## Implementation patterns:

    ### Node-based:

    1. Implement `nodes` to iterate (use an iterable or a generator
    implementation) over nodes. Alternatively, assign `self._nodes` to a 
    collection to hold nodes

    2. Implement `add_node(node)` and `add_arc(arc)` (alternatively, 
    if you assign `self._nodes` to a collection that implements 
    `.add(e)` and `.remove(e)` to add/remove element e, you may skip
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

    def __init__(self):
        self._nodes = set()
        self._arcs = set()
        raise NotImplementedError(
            "Graph is abstract and cannot be initialized; \
            use one of its implementations (or make your own!)")

    def nodes(self):
        """
        Iterates over all nodes in the graph

        Default implementation: iterates over `self._nodes`. O(N)
        """
        for node in self._nodes:
            yield node

    def arcs(self):
        """
        Iterates over all arcs in the graph.

        Default implementation: iterates over every pair of nodes and checks
        if there is an arc between them using `self.arc(n1, n2)`. 
        O(N * N * T(`self.arc`))
        """
        for pro in self.nodes():
            for epi in self.nodes():
                arc = self.arc(pro, epi)
                if arc is not None:
                    yield arc

    def arcs_out(self, node):
        """
        Iterates over the arcs that the node is a pro of

        Default implementation: iterates over `self.nodes()` and checks if 
        `self.arc(node, other: Node)` exists. O(T(`self.nodes`) * T(`self.arcs`))
        """
        for other in self.nodes():
            arc = self.arc(node, other)
            if arc is not None:
                yield arc

    def arcs_in(self, node):
        """
        Iterates over the arcs that the node is an epi of

        Default implementation: iterates over `self.nodes()` and checks if 
        `self.arc(other: Node, node)` exists. O(T(`self.nodes`)) * T(`self.arc`)) 
        """
        for other in self.nodes():
            arc = self.arc(other, node)
            if arc is not None:
                yield arc

    def arcs_in_number(self, node):
        """
        Returns a count of the arcs with node as their epi
        """
        i = 0
        for arc in self.arcs_in(node):
            i += 1
        return i

    def arcs_out_number(self, node):
        """
        Returns a count of the arcs with node as their pro
        """
        i = 0
        for arc in self.arcs_out(node):
            i += 1
        return i

    def arc(self, pro, epi):
        """
        Returns the arc from pro to epi, or None if none exists

        Default implementation: iterates over `self.arcs()` and returns an arc
        where `self.pro(arc)` and `self.epi(arc)` match pro and epi 
        respectively. O(T(`self.pro`) * T(`self.epi`) * T(`self.arc`))
        """
        for arc in self.arcs():
            if self.pro(arc) is pro and self.epi(arc) is epi:
                return arc

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
            return self.arc(node, epi) is not None       
    
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

    def has_arc(self, arc):
        """
        Returns boolean indicating whether the graph contains arc

        Default implementation: iterates over arcs to check against arc.
        O(T(`self.arcs`))
        """
        for e in self.arcs():
            if e is arc:
                return True
        return False
    
    def pro(self, arc):
        """
        Returns the pro of arc

        Default implementation: iterates through pairs of nodes and checks if
        arc matches the arc returned by `self.arc(n1, n2)`.
        O(N * N * T(`self.arc`))
        """
        for n1 in self.nodes():
            for n2 in self.nodes():
                if self.arc(n1, n2) is arc:
                    return n1

    def epi(self, arc):
        """
        Returns the epi of arc

        Default implementation: iterates through pairs of nodes and checks if
        arc matches the arc returned by `self.arc(n1, n2)`.
        O(N * N * T(`self.arc`))
        """
        for n1 in self.nodes():
            for n2 in self.nodes():
                if self.arc(n1, n2) is arc:
                    return n2
    
    def add(self, node, epi=None, arc=None):
        """
        Add node and epi to the graph (caution, if already existing they will
        be added as duplicates in certain implementations). If epi is specified,
        an arc from node to epi will also be added with value arc

        Default implementation: routes to `self.add_node` and `self.add_arc`
        """
        if epi is not None:
            self.add_node(node)
            self.add_node(epi)
            if arc is None:
                arc = True
            self.add_arc(node, epi, arc)
        else:
            self.add_node(node)

    def add_node(self, node):
        """
        Add a node to the graph, initialized without any arcs

        Default implementation: calls `self._nodes.add(node)`
        """
        self._nodes.add(node)

    def add_arc(self, pro, epi, arc=True):
        """
        Add an arc from pro to epi to the graph. By default, unlabeled arcs are
        valued True. Does not add pro or epi to the graph explicitly

        Default implementation: calls `self._arcs.add((pro, epi, arc))`
        """
        self._arcs.add((pro, epi, arc))

    def epis(self, node):
        """
        Return the epis that node has arcs to

        Default implementation: iterate through `self.nodes()` and check if
        there is an arc from node to other_node using `self.arc(other_node, node)`
        O(T(`self.nodes`) * T(`self.arc`))
        """
        for n in self.nodes():
            if self.arc(node, n) is not None:
                yield n

    def pros(self, node):
        """
        Return the pros that have arcs where node is the epi

        Default implementation: iterate through `self.nodes()` and check if
        there is an arc from node to other_node using `self.arc(node, other_node)`
        O(T(`self.nodes`) * T(`self.arc`))
        """
        for n in self.nodes():
            if self.arc(n, node) is not None:
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
        self._nodes.remove(node)        

    def remove_arc(self, pro, epi):
        """
        Remove an arc from the graph by specifying its pro and epi
        """
        self._arcs.remove(self.arc(pro, epi))

    def replace_node(self, old, new):
        """
        Replace the value of the node old with new, while preserving all
        node arcs
        """
        self.remove_node(old)
        self.add_node(new)
        for pro in self.pros(old):
            self.replace_arc_epi(pro, old, new)
        for epi in self.epis(old):
            self.replace_arc_pro(old, epi, new)

    def replace_arc(self, pro, epi, new):
        """
        Replace the value of the arc specified by pro and epi with new
        """
        self.remove_arc(pro, epi)
        self.add_arc(pro, epi, new)

    def replace_arc_pro(self, pro, epi, new_pro):
        """
        Change the epi of the arc specified by pro and epi to new_epi
        """
        arc = self.arc(pro, epi)
        self.remove_arc(pro, epi)
        self.add_arc(new_pro, epi, arc)

    def replace_arc_epi(self, pro, epi, new_epi):
        """
        Change the pro of the arc specified by pro and epi to new_epi
        """
        arc = self.arc(pro, epi)
        self.remove_arc(pro, epi)
        self.add_arc(pro, new_epi, arc)

    def traverse(self, start, frontier, condition=None):
        """
        """
        pass

    def search(self, start, frontier, end_condition, condition=None):
        """
        """
        pass

    def explore(self, start, frontier, end_condition, condition=None):
        """
        """
        pass
    
