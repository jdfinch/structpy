
from structpy.graph.labeled_digraph import MapDigraph as Graph


class StateMachine:

    def __init__(self, arcs=None, initial_state=None):
            self._graph = Graph()
            self._initial_state = None
            self._state = self._initial_state

    def graph(self):
        return self._graph

    def state(self):
        return self._state

    def reset(self):
        self._state = self._initial_state

    def next(self, input=None):
        return max([l(s, t, input)
                    for s, l, t in self.graph().arcs_out(self._state)])

    def __str__(self):
        return 'StateMachine<{}>'.format(str(self._state))
