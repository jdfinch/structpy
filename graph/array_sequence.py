from structpy.graph.core.sequence import Sequence

class ArraySequence(Sequence, list):
    """
    Sequence implemented as a list
    """

    def __init__(self, iterable):
        """
        Initialize the array sequence with an iterable, in which the first 
        element will become the root of this sequence
        """
        list.__init__(self, iterable)

    def root(self):
        return list.__getitem__(self, 0)

    def nodes(self):
        return self

    def arcs(self):
        i = 0
        for i in range(list.__len__(self) - 1):
            yield (list.__getitem__(self, i), list.__getitem__(self, i + 1))
            
    def arc(self, pro, epi):
        for arc in self.arcs():
            if arc[0] is pro and arc[1] is epi:
                return arc

    has_node = list.__contains__

    nodes_number = list.__len__

    add_node = list.append

    remove_node = list.remove

    def replace_node(self, old, new):
        i = list.index(self, old)
        self.__setitem__(self, i, new)

    def traverse(self, start=None):
        if start is None:
            i = 0
        else:
            i = list.index(start)
        while i < list.__len__(self):
            yield list.__getitem__(self, i)
            i += 1
        
    def traverse_reverse(self, start=None):
        if start is None:
            i = list.__len__(self) - 1
        else:
            i = list.index(start)
        while i > -1:
            yield list.__getitem__(self, i)
            i -= 1


    
