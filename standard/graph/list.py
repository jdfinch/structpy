import standard.graph.sequence
Sequence = standard.graph.sequence.Sequence

class List(Sequence):

    def __init__(self, iterable):
        self._nodes = [e for e in iterable]

    