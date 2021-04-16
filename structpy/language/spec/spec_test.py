
from structpy.language.spec import spec_spec as s
from structpy.language.spec.spec import Verifier

if __name__ == '__main__':

    class MyClass:

        def __init__(self, a, b):
            self.a = a
            self.b = b

        def my_method(self, c):
            return self.a + self.b + 2

        def z_method(self, x, y):
            return sum([self.a, self.b, x, y])


    v = Verifier()
    v.collect(s)
    v.verify(s, MyClass)