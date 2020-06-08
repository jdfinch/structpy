
from unittest import TestSuite, TextTestRunner
from traceback import print_exc
from sys import stderr
from structpy.language.specification.spec_list import SpecList

class Verifier:
    """
    Manages a suite of specs associated with a specification.

    Adding a `init` spec sets up an object under unit,
    which is passed to each subsequent `prop` or `unit` spec.
    """

    def __init__(self):
        self._specs_lists = []

    def verify(self, Implementation):
        """
        Verify that the `Implementation` satisfies all the tests in the
        spec list.
        """
        succeeded = 0
        failed = 0
        run = 0
        for spec_list in self._specs_lists:
            result = spec_list.verify(Implementation)
            run += result.testsRun
            failed += len(result.failures)
            succeeded += run - failed
        print('\n\nTEST RESULTS:', file=stderr)
        print(succeeded, 'succeeded', file=stderr)
        print(failed, 'failed', file=stderr)

    def add_spec_list(self, init_spec, specs):
        spec_list = SpecList(init_spec, specs)
        self._specs_lists.append(spec_list)


# if __name__ == '__main__':
#     from structpy.language.specification.spec import Spec
#     class MyStruct:
#         def __init__(self, a, b):
#             self.a = a
#             self.b = b
#     def specinit(Struct):
#         return Struct(1, 2)
#     def specfn1(x):
#         assert x.a == 1
#         x.b = 4
#     def specfn2(x):
#         assert x.b == 4
#     sc = Spec(specinit, 'construction')
#     s1 = Spec(specfn1, 'definition')
#     s2 = Spec(specfn2, 'definition')
#     verifier = Verifier()
#     verifier.add_spec(sc)
#     verifier.add_spec(s1)
#     verifier.add_spec(s2)
#     verifier.verify(MyStruct)















