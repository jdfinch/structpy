
from unittest import TestSuite, TextTestRunner

class Verifier:
    """
    Manages a suite of specs associated with a specification.

    Adding a 'construction' spec sets up an object under test,
    which is passed to each subsequent 'definition' spec.
    """

    def __init__(self):
        self._specs = []
        self._benchmarks = []
        self._evaluations = []

    def verify(self, Implementation):
        suite = TestSuite()
        specs = []
        instance = None
        for spec in self._specs:
            if spec.type() == 'construction':
                spec.set_object(Implementation)
                try:
                    instance = spec.run_test()
                except Exception as e:
                    print('Error: {}'.format(spec))
                    print(e)
                    instance = None
            elif spec.type() == 'definition':
                spec.set_object(instance)
                specs.append(spec)
            else:
                spec.set_object(Implementation)
                specs.append(spec)
        suite.addTests(specs)
        TextTestRunner().run(suite)

    def add_from(self, other):
        self._specs.extend(other._specs)
        self._benchmarks.extend(other._benchmarks)
        self._evaluations.extend(other._evaluations)

    def add_spec(self, spec):
        self._specs.append(spec)


if __name__ == '__main__':
    from structpy.language.specification.spec import Spec
    class MyStruct:
        def __init__(self, a, b):
            self.a = a
            self.b = b
    def specinit(Struct):
        return Struct(1, 2)
    def specfn1(x):
        assert x.a == 1
        x.b = 4
    def specfn2(x):
        assert x.b == 4
    sc = Spec(specinit, 'construction')
    s1 = Spec(specfn1, 'definition')
    s2 = Spec(specfn2, 'definition')
    verifier = Verifier()
    verifier.add_spec(sc)
    verifier.add_spec(s1)
    verifier.add_spec(s2)
    verifier.verify(MyStruct)















