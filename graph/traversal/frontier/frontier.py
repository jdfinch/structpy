
from abc import ABC, abstractmethod

class Frontier:

    def __init__(self, step, *initials):
        self._step = step
        for initial in initials:
            self.add(self._step(initial))

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def add(self, item):
        pass

    def step(self):
        return self._step

    @abstractmethod
    def __len__(self):
        pass

    def __bool__(self):
        return len(self) > 0
