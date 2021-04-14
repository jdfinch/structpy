
# from structpy import spec

"""
Here is MyClass.

It is useless.
"""


def __init__(MyClass, a, b):
    """
    Here's how you initialize a MyClass.
    """
    my_object = MyClass(2, 4)
    return my_object

def z_method(x, y):
    pass

def my_method(my_object, c):
    """
    Here's a MyClass method.
    """
    my_value = my_object.my_method(4)
    assert my_value == 10

def zz_methodszz(a, b, c):
    pass

