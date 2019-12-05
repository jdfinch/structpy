
from abc import ABC, abstractmethod
from structpy.graph.labeled_digraph import MapDigraph as Graph


class State(ABC):

    @abstractmethod
    def activate(self, source, label, input):
        pass

    def __call__(self, source, label, input):
        return self.activate(source, label, input)


class Transition(ABC):

    @abstractmethod
    def score(self, source, target, input):
        pass

    def __call__(self, source, target, input):
        return self.score(source, target, input)


class StateMachine:

    def __init__(self, arcs=None, initial_state=None):
        self._graph = Graph(arcs)
        self._initial_state = initial_state
        self._state = self._initial_state

    def graph(self):
        return self._graph

    def state(self):
        return self._state

    def reset(self):
        self._state = self._initial_state

    def next(self, input=None):
        score, s, t, l = max([(l.score(s, t, input), s, t, l)
                              for s, l, t in self.graph().arcs_out(self._state)])
        t.activate(s, l, input)
        self._state = t
        return self._state

    def __str__(self):
        return 'StateMachine<{}>'.format(str(self._state))
