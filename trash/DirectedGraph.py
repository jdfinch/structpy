
'''from Nodes import Ordered

class DirectedGraph:
    
    def __init__(self, nodeType=None):
        self.nodes = {}  # value : edges
        if nodeType is None:
            nodeType = Ordered
        self.nodeType = nodeType

    def nodeFromElement(self, element):
        if element not in self.nodes.keys():
            elementNode = self.nodeType(element)
            self.nodes[element] = elementNode
        else:
            elementNode = self.nodes[element]
        return elementNode
            
    def Add(self, element, children=[], parents=[]):
        elementNode = self.nodeFromElement(element)
        childNodes = [self.nodeFromElement(child) for child in children]
        parentNodes = [self.nodeFromElement(parent) for parent in parents]
        for childNode in childNodes:
            elementNode.Add(childNode)
        for parentNode in parentNodes:
            parentNode.Add(elementNode)

    def AddEdge(self, parent, child):
        parentNode = self.nodeFromElement(parent)
        childNode = self.nodeFromElement(child)
        parentNode.Add(childNode)

    def HasElement(self, element):
        return element in self.nodes.keys()

    def TraversalPreOrder(self, element):
        rootNode = self.nodes[element]
        for n in rootNode.TraversalPreOrder():
            yield n.Value()
                
    def TraversalBreadthFirst(self, element):
        rootNode = self.nodes[element]
        for n in rootNode.TraversalBreadthFirst():
            yield n.Value()

    def TraversalPostOrder(self, element):
        rootNode = self.nodes[element]
        for n in rootNode.TraversalPostOrder():
            yield n.Value()


        1
    2       3    4
   6 7    8  9 10

graph = DirectedGraph()
graph.Add(1, [2, 3])
graph.Add(6, [], [2])
graph.Add(2, [7])
graph.Add(3, [8, 9, 10])
graph.Add(4, [9, 10])
#graph.Add(9, [1])
print(list(graph.TraversalBreadthFirst(1)))
print(list(graph.TraversalPreOrder(3)))
'''