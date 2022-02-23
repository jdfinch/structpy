
from structpy.spec import Spec, detail, expecting

from typing import Any
from typing import Iterable, Hashable, Mapping
from typing import Protocol


class Set(Spec, Protocol):
    """
    Specification for Python's built-in `set` collection.
    """

    def __init__(
            s
    ):
        s = Set({'a': 1, 'b': 2, 'c': 3})
