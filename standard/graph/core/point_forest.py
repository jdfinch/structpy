from abc import abstractmethod
from standard.graph.core.point_dag import PointDag

class PointForest(PointDag):

    @abstractmethod
    def __init__(self):
        self._roots = set()

