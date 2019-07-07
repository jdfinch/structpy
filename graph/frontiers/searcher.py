from structpy.graph.frontiers.frontier import Frontier

from abc import ABC, abstractmethod

class Searcher(Frontier, ABC):
    """
    Frontier for searches, maintains and returns a result with the `.result`
    method, which represents the solution to the search
    """

    @abstractmethod
    def result(self):
        """
        Returns the result of a search as a `Sequence`
        """
        pass


