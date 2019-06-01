from collections import deque

class DictionaryGraph:
    """
    General directed graph implemented with dictionaries
    """

    def __init__(self):
        """
        `_nodes: dict<pro: object, dict<epi: object, edge: object>>` 
        """
        self._nodes = {}

    def nodes(self):
        """
        Returns an iterable over all nodes in the graph
        """
        for node in self._nodes.keys():
            yield node

    def has_node(self, node):
        """
        Checks node membership in the graph
        """
        return node in self._nodes

    def edges(self):
        """
        Returns an iterable over all edges (pairs of nodes) in the graph

        For each edge, the pro is accessed by edge[0], the epi by edge[1], 
        the value by edge[2]
        """
        for pro in self._nodes.keys():
            for epi in self._nodes[pro]:
                yield (pro, epi, self._nodes[pro][epi]) 

    def has_edge(self, pro, epi):
        """
        Checks edge membership in the graph
        """
        return pro in self._nodes and epi in self._nodes[pro]

    def epis(self, pro):
        """
        Returns an iterable over the epis of a given node
        """
        for epi in self._nodes[pro]:
            yield epi

    def edge(self, pro, epi):
        """
        Return the edge from node pro to node epi

        Raises exception if there is no edge from pro to epi
        """
        return self._nodes[pro][epi]

    def add_node(self, node):
        """
        Add a node to this graph if it doesn't already exist
        """
        if node not in self._nodes:
            self._nodes[node] = {}

    def add_edge(self, pro, epi, edge=None):
        """
        Add an edge between two existing nodes in the graph

        If the edge already exists, overwrite it with a new edge value

        Raises an exception if either node does not already exist in the graph
        """
        self._nodes[pro][epi] = edge

    def add(self, pro, epi=None, edge=None):
        """
        Add nodes pro and epi if they don't already exist, and set the edge between them

        If epi and pro are not specified, only pro will be added to the set of nodes
        """
        self.add_node(pro)
        if epi is not None:
            if epi not in self._nodes:
                self.add_node(epi)
            self.add_edge(pro, epi, edge)

    def remove_node(self, node):
        """
        Remove node from this graph
        """
        del self._nodes[node]

    def remove_edge(self, pro, epi):
        """
        Remove the edge between pro and epi
        """
        del self._nodes[pro][epi]

    def traversal_breadthfirst(self, start):
        """
        Traverse over nodes in breadth-first order starting with start node
        """
        q = deque()
        q.append(start)
        visited = set()
        while q:
            n = q.popleft()
            yield n
            visited.add(n)
            for epi in self.epis(n):
                if epi not in visited:
                    q.append(epi)

    def traversal_postorder(self, start):
        """
        Traverse over nodes in post-order starting with start node
        """
        pass

    def traversal_preorder(self, start):
        """
        Traverse over nodes in pre-order starting with start node
        """
        pass

    def traversal_breadthfirst_if(self, start, condition):
        """
        Traverse over nodes in breadth-first order starting with start node

        Nodes are only traversed, expanded, and yielded if condition(epi, edge)
        returns True, where epi is the node to expand and edge is the edge between
        epi and the pro that expanded to traverse to it

        `condition: function<bool>(pro, epi, edge)` 
        """
        pass

    def traversal_postorder_if(self, start, condition):
        """
        Traverse over nodes in post-order starting with start node

        Nodes are only traversed, expanded, and yielded if condition(epi, edge)
        returns True, where epi is the node to expand and edge is the edge between
        epi and the pro that expanded to traverse to it

        `condition: function<bool>(pro, epi, edge)` 
        """
        pass

    def traversal_preorder_if(self, start, condition):
        """
        Traverse over nodes in pre-order starting with start node

        Nodes are only traversed, expanded, and yielded if condition(epi, edge)
        returns True, where epi is the node to expand and edge is the edge between
        epi and the pro that expanded to traverse to it

        `condition: function<bool>(pro, epi, edge)` 
        """
        pass

    def traversal_costorder(self, start, cost_function=None):
        """
        Traverse the nodes in order of expansion cost, where lesser cost
        epis are expanded first

        `cost_function: function<comparable>(pro, epi, edge)`
        """
        pass
            
    def search_breadthfirst(self, start, end_condition):
        """
        Search over nodes in breadth-first order starting with start node
        until end_condition is reached

        End condition can be either a target node OR a condition function

        `end_condition: target: object 
                        OR function<bool>(this: dictionary_graph, path: list<object>)`
        """
        pass

    def search_depthfirst(self, start, end_condition):
        """
        Search over nodes in  depth-first order starting with start node
        until end_condition is reached

        End condition can be either a target node OR a condition function

        `end_condition: target: object 
                        OR function<bool>(this: dictionary_graph, path: list<object>)`
        """
        pass

    def search_iterdepth(self, start, end_condition):
        """
        Search over nodes in iterative deepening depth-first order starting with start 
        node until end_condition is reached

        End condition can be either a target node OR a condition function

        `end_condition: target: object 
                        OR function<bool>(this: dictionary_graph, path: list<object>)`
        """
        pass

    def search_breadthfirst_if(self, start, condition, end_condition):
        """
        Search over nodes in  breadth-first order starting with start node
        until end_condition is reached

        End condition can be either a target node OR a condition function

        Nodes are only traversed, expanded, and yielded if condition(epi, edge)
        returns True, where epi is the node to expand and edge is the edge between
        epi and the pro that expanded to traverse to it

        `end_condition: target: object 
                        OR function<bool>(this: dictionary_graph, path: list<object>)`

        `condition: function<bool>(pro, epi, edge)` 
        """
        pass

    def search_depthfirst_if(self, start, condition, end_condition):
        """
        Search over nodes in  depth-first order starting with start node
        until end_condition is reached

        End condition can be either a target node OR a condition function

        Nodes are only traversed, expanded, and yielded if condition(epi, edge)
        returns True, where epi is the node to expand and edge is the edge between
        epi and the pro that expanded to traverse to it

        `end_condition: target: object 
                        OR function<bool>(this: dictionary_graph, path: list<object>)`

        `condition: function<bool>(pro, epi, edge)` 
        """
        pass

    def search_iterdepth_if(self, start, condition, end_condition):
        """
        Search over nodes in iterative deepening depth-first order starting with start 
        node until end_condition is reached

        End condition can be either a target node OR a condition function

        Nodes are only traversed, expanded, and yielded if condition(epi, edge)
        returns True, where epi is the node to expand and edge is the edge between
        epi and the pro that expanded to traverse to it

        `end_condition: target: object 
                        OR function<bool>(this: dictionary_graph, path: list<object>)`

        `condition: function<bool>(pro, epi, edge)`
        """
        pass

    def search_costorder(self, start, end_condition, cost_function=None):
        """
        Search over nodes in order of least cost to expand the next node

        End condition can be either a target node OR a condition function

        `end_condition: target: object
                        OR function<bool>(this: dictionary_graph, path: list<object>)`

        `cost_function: function<comparable>(this: dictionary_graph, path: list<object>)`
        """
        pass

    
