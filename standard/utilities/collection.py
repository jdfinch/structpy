from abc import ABC, abstractmethod

class Collection(ABC):
    """

    """

    @abstractmethod
    def add(self, element):
        """
        Add an element to the collection
        """
        pass

    @abstractmethod
    def pop(self, key=None):
        """
        Remove an element from the collectoin
        """