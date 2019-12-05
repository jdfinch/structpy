
from enum import Enum
from structpy.graph import Database
from structpy.graph.labeled_digraph import DeterministicMapDigraph
from structpy.language.simple import single

Graph = Database(DeterministicMapDigraph)


class Functions(Enum):
    Score = 0
    Activate = 1


class StateMachine:

    def __init__(self, arcs=None, initial_state=None):
        self._graph = Graph(arcs)
        self._initial_state = initial_state
        if initial_state is not None:
            self.set_initial_state(initial_state)
        self._state = self._initial_state

    def set_initial_state(self, initial_state):
        self._initial_state = initial_state
        if not self._graph.has_node(initial_state):
            self.add_state(initial_state)

    def add_state(self, state):
        self._graph.add_node(state)

    def add_transition(self, source_state, target_state, transition, transition_fn=None):
        self._graph.add(source_state, target_state, transition)
        if transition_fn is not None:
            self._graph.arc_data(source_state, target_state)[Functions.Transition] = transition_fn

    def graph(self):
        return self._graph

    def state(self):
        return self._state

    def reset(self):
        self._state = self._initial_state

    def next(self, input=None):
        if not self._graph.has_arc_label(self._state, input):
            scores = []
            for s, t, l in self._graph.arcs_out(self._state):
                score_fn = self._graph.arc_data(s, t)[Functions.Score]
                score = score_fn(input, *[self._graph.node(x) for x in (s, t, l)])
                scores.append((score, s, t, l))
            _, s, t, label = max(scores)
            self._state = t
        else:
            self._state = self._graph.target(self._state, input)
        return self._state

    def jump(self, state):
        self._state = state

    def __str__(self):
        return 'StateMachine<{}>'.format(str(self._state))
