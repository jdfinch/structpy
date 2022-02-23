from typing import Protocol


class FooProto(Protocol):

    def __init__(self, x: float) -> None:
        self.x = x
        self.y = 'hello'

    def __init__(self, z: list) -> None:
        self.z = z

    def bat(self) -> str:
        self.z.pop()
        _ = FooProto(3).x + self.x
        return 'hello'


class Foo:

    def __init__(self, *args: ..., **kwargs: ...) -> ...:
        ...

    def bat(self) -> str:
        return 'hello'


f: FooProto = Foo(4)

