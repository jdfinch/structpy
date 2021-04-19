
from structpy.system.spec import spec
from structpy.system.printer import print as p

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


if __name__ == '__main__':

    class MyClass:

        def __init__(self, a, b):
            self.a = a
            self.b = b

        def my_method(self, c):
            return self.a + self.b + 2

        def z_method(self, x, y):
            return sum([self.a, self.b, x, y])

    spec.verify(MyClass)