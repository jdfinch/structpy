
from typing import Protocol


def spec(cls):
    return [1, 2, 3]


class Foo(Protocol):

    def __init__(self):
        return

    def bar(foo, x: int) -> str:
        assert foo.bar(5) == 'hello world'
        return ...


FooSpec = spec(Foo)



class FooImp:

    def __init__(self):
        return

    def bar(foo, x: int) -> str:
        return 'hello world'



f: Foo = FooImp()
x: str = f.bar(5)




