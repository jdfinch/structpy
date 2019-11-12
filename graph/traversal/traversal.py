
class Traversal:

    def __init__(self, graph, frontier):
        self._graph = graph
        self._frontier = frontier
        self._step = self._frontier.step()
        self._step.init_frontier(self)

    def frontier(self):
        return self._frontier

    def __iter__(self):
        return self

    def __next__(self):
        if not self._frontier:
            raise StopIteration
        item = self._frontier.get()
        for following in item.next_steps(self._graph):
            self._frontier.add(following)
        return item.value()

    def __str__(self):
        return 'Traversal<' + str(self._graph) + ', ' + str(self._frontier) + '>'

    def __repr__(self):
        return str(self)