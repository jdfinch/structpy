
from inspect import getsource


def foo(x, y):
    z = x + y
    z /= 2
    return z

print(getsource(foo))