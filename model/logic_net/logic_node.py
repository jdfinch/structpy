
from structpy import Pointer
from abc import ABC, abstractmethod
from enum import Enum
from structpy.graph.net import Net

class Arc(Enum):
    FIRST = 0
    SECOND = 1
    THIRD = 2

class LogicalOperator(Pointer, ABC):

    def __init__(self, value=0.0, p=1.0):
        Pointer.__init__(self, value)
        self._p = p

    @abstractmethod
    def update(self, x, y):
        pass

    @abstractmethod
    def update_reverse(self, x, y):
        pass

class Term(LogicalOperator):

    def update(self, x, y):
        pass

    def update_reverse(self, x, y):
        pass

class Thus(LogicalOperator):

    def update(self, x, y):
        pass

    def update_reverse(self, x, y):
        pass

class Or(LogicalOperator):

    def update(self, x, y):
        pass

    def update_reverse(self, x, y):
        pass
