from standard.graph.core.sequence import Sequence

class ListSequence(Sequence,list):

    def __init__(self, iterable):
        for e in iterable:
            self.append(e)

    def top(self):
        if len(self) > 0:
            return self[-1]
        return None

    def root(self):
        if len(self) > 0:
            return self[0]
        return None

    def child(self, node):
        idx = self.index(node)
        if idx < len(self)-1:
            return self[idx+1]
        return None

    def parent(self, node):
        idx = self.index(node)
        if idx > 0:
            return self[idx - 1]
        return None

    def node_at(self, index):
        if index < len(self):
            return self[index]
        return None


if __name__ == '__main__':
    ls = ListSequence([0, 1])


