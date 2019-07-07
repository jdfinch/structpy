from abc import abstractmethod
from structpy.graph.core.point_dag import PointDag

class PointForest(PointDag):

    @abstractmethod
    def __init__(self):
        self._roots = set()

