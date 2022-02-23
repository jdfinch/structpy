
from typing import Generic, TypeVar


d = {1: 'hello', 2: 'world'}
d[3] = 4

U = TypeVar('U')
T = TypeVar('T')

class MyThing(Generic[T, U]):

    def __init__(self, a:T, b:U, c:T, d:U):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

m = MyThing(1, 'hello', 2, 3)



V = TypeVar('V')

def foo(x: set[V]) -> set[V]:
    return x

f = foo({1, 2, 'hello'})
b = f.pop().rstrip()
c = f.pop().real

