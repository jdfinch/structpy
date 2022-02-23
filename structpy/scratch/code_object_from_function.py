
import inspect

def foo(x, y):
    """
    foo
    :param x: do
    :param y: some
    :return: stuff
    """
    z = x + y
    l = [x, y, z]
    # sort the list
    l.sort()
    return l

input()
code = inspect.getsource(foo)
print(code)