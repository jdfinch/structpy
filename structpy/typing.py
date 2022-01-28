
from typing import Protocol, Any
from typing import Iterable, Iterator
from typing import Mapping


class Hashable_(Protocol):
    def __hash__(self) -> int: ...
Hashable = Hashable_





