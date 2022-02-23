
from typing import Hashable, Iterable, Protocol, Any
from typing import TypeVar, Generic


class hashable(Protocol):

    def __hash__(self) -> int:
        ...


a: Iterable[Hashable] = [{}]
b: Iterable[hashable] = [{}] # builtin hashable doesn't work


class Foo:

    def foo(self, x: int) -> Iterable:
        return [5] * x

    def bar(self, y: str):
        return [1, 2, 3, y]

f = Foo()
c = f.foo(3)
c.reverse() # Annotating return as Iterable loses type hinting of actual type
d = f.bar('blah')
int_result = d[0].imag
str_result = d[3].replace('a', '_')


class MyTuple(tuple): pass

def bar(x: tuple) -> tuple:
    return x

e: tuple = bar(MyTuple())



T = TypeVar('T')

class Bar: # (Generic[T]):

    def __init__(self, x): # :T):
        self.data = [x] #: list[T] = [x]

    def add(self, x): # x: T):
        self.data.append(x)

g = Bar(2)
g.add('hello')
g.data.pop()






