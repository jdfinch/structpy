
from typing import Hashable, Iterable, Protocol


class hashable(Protocol):

    def __hash__(self) -> int:
        ...


a: Iterable[Hashable] = [{}]
b: Iterable[hashable] = [{}]














