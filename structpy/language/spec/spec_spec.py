
from structpy.language.spec.spec import spec
from structpy.language.printer.printer import print as p

"""
Here is MyClass.

It is useless.
"""


def __init__(MyClass, a, b):
    """
    Here's how you initialize a MyClass.
    """
    my_object = MyClass(2, 4)
    print(my_object)
    return my_object

def z_method(my_object, x, y):
    print('Here is something happening!')
    print(f'X: {my_object.z_method(5, 9)}')

def my_method(my_object, c):
    """
    Here's a MyClass method.
    """
    my_value = my_object.my_method(4)
    print(my_value)
    with spec.raises(AssertionError('1')):
        assert False

def anothertest(Mycl):
    print('Another test!')
    return Mycl(0, 0)

def zz_methodszz(my_object, a, b, c):
    p(my_object)
    p('Something else:')
    with p.mode('indent'):
        p('...')
        p('...')
    p.mode('blue')('Done!')

def other_test():
    p('Hello')
    with p.indent:
        p.mode('blue')('...\n\n...\n')
    p('done.')