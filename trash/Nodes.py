from Standard.Graph.Node import Node
from collections import deque

class acyclic:

    def TraversalPreOrder(self):
        stack = [self]
        while stack:
            n = stack.pop()
            yield n
            for child in n.ChildrenReversed():
                stack.append(child)

    def TraversalBreadthFirst(self):
        queue = deque([self])
        while queue:
            n = queue.pop()
            yield n
            for child in n.Children():
                queue.appendleft(child)

    def TraversalPostOrder(self):
        for child in self.Children():
            for n in child._traversalPostOrder(visited):
                yield n
        yield self


class Ordered(Node):

    def __init__(self, value):
        Node.__init__(self, value)
        self.children = []

    def Add(self, childNode):
        self.children.append(childNode)

    def Children(self):
        for child in self.children:
            yield child

    def ChildrenReversed(self):
        for i in range(len(self.children) - 1, -1, -1):
            yield self.children[i]

    def HasChild(self, child):
        return child in self.children

    def HasChildren(self):
        return len(self.children) > 0


class OrderedAcyclic(acyclic, Ordered):
    pass


class Unordered(Node):

    def __init__(self, value):
        Node.__init__(self, value)
        self.children = set()

    def Add(self, childNode):
        self.children.add(childNode)

    def Children(self):
        for child in self.children:
            yield child

    def ChildrenReversed(self):
        for child in self.children:
            yield child

    def HasChild(self, child):
        return child in self.children

    def HasChildren(self):
        return len(self.children) > 0


"""
[[Node.py#node]]
"""


class UnorderedAcyclic(acyclic, Unordered):
    pass
