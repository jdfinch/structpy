
from structpy.language.unit_test.scratch import my_dec, ref, A

@my_dec
class B:

    hello = 'hello'

    def bar(self, x):
        """
        doc for bar
        """
        return x * 3

    @ref(A.foo)
    def baz(self, x):
        """
        doc for baz
        """
        return x * 4

    def bat(self, x):
        """
        doc for bat
        """
        return 5


if __name__ == '__main__':

    print(B, '\n')
    for k, v in B.__dict__.items():
        print(k, v)
    print()
    print(B.bar(None, 4))
    print(B.baz(None, 4))
    print(B.x(None))
    print(B.y(None))
    print(B.bat(None, 4))
