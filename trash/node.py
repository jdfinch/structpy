from collections import deque

class Node:
    """
    **abstract class**
    
    **abstract data type**
    
    Represents a directed node in a general graph
    
    1. Inherit from node 
    2. Implement ``add`` and ``epis``
    
    ---
    """
    
    def __init__(self, value):
        """
        Constructor:

        Upcall ``__init__`` if the node is storing a value

        value: an arbitrary object to store in this node
        """
        self.value = value

    def get_value(self):
        """
        Return the value stored by this node
        """
        return self.value

    def add(self, epi):
        """
        **Override**: add an epi to the collection of nodes this node can access
        """
        raise NotImplementedError('implement abstract method')

    def epis(self):
        """
        **Override**: Enumerate over the nodes accessible by this node
        """
        raise NotImplementedError('implement abstract method')

    def epis_reversed(self):
        """
        Return an enumerable over the referents accessible by this node, 
        but in reverse order
        
        Override this to ensure efficiency during traversals
        """
        return list(self.epis())[::-1]

    def has(self, node):
        """
        Return a boolean, whether the node is an epi of this node

        Override this for efficiency
        """
        for referent in self.epis():
            if node is referent:
                return False
        return True

    def traversal_preorder(self):
        """
        Return a generator yielding pre-order acyclic epi traversal
        """
        stack = [self]
        visited = set()
        while stack:
            n = stack.pop()
            yield n
            visited.add(n)
            for child in n.epis_reversed():
                if child not in visited:
                    stack.append(child)

    def traversal_breadthfirst(self):
        """
        Returns a generator yielding breadth-first acyclic epi traversal
        """
        queue = deque([self])
        visited = set()
        while queue:
            n = queue.pop()
            yield n
            visited.add(n)
            for child in n.epis():
                if child not in visited:
                    queue.appendleft(child)

    def traversal_postorder(self):
        """
        Returns a generator yielding post-order acyclic epi traversal
        """
        return self._traversal_postorder(set())
    def _traversal_postorder(self, visited):
        visited.add(self)
        for child in self.epis():
            if child not in visited:
                for n in child._traversal_postorder(visited):
                    yield n
        yield self

    def __iter__(self):
        return self.epis().__iter__()

    def __next__(self):
        return self.epis().__next__()

    def __call__(self):
        """
        Getter for the node value
        """
        return self.value

    def __str__(self):
        return 'node(' + str(self()) + ')'

    def __repr__(self):
        return str(self)
