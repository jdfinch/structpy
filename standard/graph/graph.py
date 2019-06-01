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
    - `remove_arc(arc)`: remove arc by value

    ### Mutation:

    - `replace_node(old, new)`: replace a node while preserving its arcs
    - `replace_arc(pro, epi, new)`: replace an arc by its node endpoints

    ### Properties for finding nodes:

    - `epis(node)`: iterate over epis of a node
    - `pros(node)`: iterate over pros of a node
    - `pro(arc)`: returns the pro of an arc
    - `epi(arc)`: returns the epi of an arc
    - `number_epis(node)`: returns a count of a node's epis
    - `number_pros(node)`: returns a count of a nodes's pros

    ### Properties for finding arcs:

    - `arc(pro, epi)`: returns the arc from pro to epi
    - `arcs_out(node)`: iterate over the arcs the node is the pro of
    - `arcs_in(node)`: iterate over the arcs the node is an epi of
    - `number_arcs_out(node)`: count of the arcs the node is the pro of
    - `number_arcs_in(node)`: count of the arcs the node is an epi of

    ### Graph navigation:

    - `traverse(start, frontier, condition=None)`: memoryless node traversal
    - `search(start, frontier, end_condition, condition)`: path search
    - `explore(start, frontier, end_condition, condition)`: generator search

    ## Implementation patterns:

    ### Node-based:

    1. Implement `nodes` to iterate (use a generator with the yield
    keyword) over nodes. Alternatively, assign `self._nodes` to a 
    collection to hold nodes

    2. Implement `add_node(node)` and `add_arc(arc)` (alternatively, 
    if you assign `self._nodes` to a collection that implements 
    `.add(e)` and `.remove(e)` to add/remove element e, you may skip
    this step)

    3. Implement `arc(pro, epi)` to return the arc from pro to epi, or None
    if none exists. Return True for label-less arcs.

    4. If you want to improve the efficiency of other methods, you
    can re-implement them. Especially, the default implementations of
    the following methods may be inefficient, although they will work
    if the above 3 steps have been followed:

        - `epis`
        - `pros`
        - `pro`
        - `epi`

    ### Edge-based:

    1. lorem ipsum

    ### 
    """

    def __init__(self):
        self._nodes = set()
        self._arcs = set()
        raise NotImplementedError(
            "Graph is abstract and cannot be initialized; \
            use one of its implementations ")

    def nodes(self):
        """
        Iterates over all nodes in the graph

        Default implementation: iterates over `self._nodes`. O(N)
        """
        for node in self._nodes:
            yield node

    def arcs(self):
        """
        Iterates over all arcs in the graph
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
        `self._arc(node, other: Node)` exists. O(N * T(`self.arc`)) efficiency
        """
        for other in self.nodes():
            arc = self.arc(node, other)
            if arc is not None:
                yield arc

    def arcs_in(self, node):
        """
        Iterates over the arcs that the node is an epi of

        Default implementation: iterates over `self.nodes()` and checks if 
        `self._arc(other: Node, node)` exists. O(N * T(`self.arc`)) efficiency 
        """
        for other in self.nodes():
            arc = self.arc(other, node)
            if arc is not None:
                yield arc

    def arc(self, pro, epi):
        """
        Returns the arc from pro to epi, or None if none exists

        Default implementation: iterates over `self.arcs()` and returns an arc
        where `self.pro(arc)` and `self.epi(arc)` match pro and epi 
        respectively 
        """
        for arc in self.arcs():
            if self.pro(arc) is pro and self.epi(arc) is epi:
                return arc

    def has(self, node, epi=None):
        """
        Returns whether the graph contains node

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
        """
        for n in self.nodes():
            if n is node:
                return True
        return False

    def has_arc(self, arc):
        """
        """
        for e in self.arcs():
            if e is arc:
                return True
        return False
    
    def pro(self, arc):
        """
        """
        for n1 in self.nodes():
            for n2 in self.nodes():
                if self.arc(n1, n2) is arc:
                    return n1

    def epi(self, arc):
        """
        """
        for n1 in self.nodes():
            for n2 in self.nodes():
                if self.arc(n1, n2) is arc:
                    return n2
    
    def add(self, node, epi=None, arc=None):
        """
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
        """
        self._nodes.add(node)

    def add_arc(self, pro, epi, arc=True):
        """
        """
        self._arcs.add((pro, epi, arc))

    def epis(self, node):
        """
        """
        for n in self.nodes():
            if self.arc(node, n) is not None:
                yield n

    def pros(self, node):
        """
        """
        for n in self.nodes():
            if self.arc(n, node) is not None:
                yield n

    def remove(self, node, epi=None):
        """
        """
        pass
    
    def remove_node(self, node):
        """
        """
        pass

    def remove_arc(self, arc):
        """
        """
        pass

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

    def traverse_arcs(self, start, frontier, condition=None):
        """
        """
        pass

    def search_arcs(self, start, frontier, end_condition, condition=None):
        """
        """
        pass

    def explore_arcs(self, start, frontier, end_condition, condition=None):
        """
        """
        pass

    
