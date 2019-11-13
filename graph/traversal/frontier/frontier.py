
from abc import ABC, abstractmethod
from structpy.graph.traversal.traversal_step import TraversalStep

from structpy.graph.traversal.traversal_step import Step
from structpy.language import Mechanic


class Frontier(ABC):

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def add(self, step):
        pass


