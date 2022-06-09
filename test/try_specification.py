
from structpy.specification.specification import Spec


spec = Spec()

with spec.params:

    a = ...
    b = 2

with spec:

    def foo(x, y, z):
        global a
        a = [1, 2, 3]
        assert b == 2

    def bar(a, c):
        global b
        b = 2
        assert a == [1, 2, 3]
        a.append(4)
        assert a == [1, 2, 3, 4]

    def bat(x, y, z):
        assert a == [1, 2, 3]
        assert b == 2


if __name__ == '__main__':

    import pprint

    spec.implementation([], 10)
    results = spec.run(True)

    for result in results:
        pprint.pp(result())
