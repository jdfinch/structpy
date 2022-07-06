
from typing import Protocol


class FooProto(Protocol):

    def bar(self) -> int:
        return 5

    def alias(self) -> int:
        return ...


class Foo:

    @property
    def bar(self) -> int:
        return 5

    @property
    def alias(self) -> int:
        return 5


f: FooProto = Foo()

x: int = f.alias()

