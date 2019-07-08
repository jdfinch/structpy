from structpy.graph.core.graph import Graph

class ArcGraph(Graph):

    def pro(self, arc):
        """
        Returns the pro of arc

        Default implementation: iterates through pairs of nodes and checks if
        arc matches the arc returned by `self.arc(n1, n2)`.
        O(N * N * T(`self.arc`))
        """
        for n1 in self.nodes():
            for n2 in self.nodes():
                if self.arc(n1, n2) is arc:
                    return n1

    def epi(self, arc):
        """
        Returns the epi of arc

        Default implementation: iterates through pairs of nodes and checks if
        arc matches the arc returned by `self.arc(n1, n2)`.
        O(N * N * T(`self.arc`))
        """
        for n1 in self.nodes():
            for n2 in self.nodes():
                if self.arc(n1, n2) is arc:
                    return n2