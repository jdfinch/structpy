from collections import defaultdict
from structpy.language.specification.verifier import Verifier
from structpy.language.specification.spec import Spec
from inspect import getmro, getmembers, isfunction


class implements:
    def __init__(self, specification):
        self.__specification__ = specification
    def __call__(self, implementation):
        class Implementation(implementation):
            __specification__ = self.__specification__
            __implementation__ = implementation
            @classmethod
            def __verify__(cls):
                Implementation.__specification__.__verify__(cls)
        self.__specification__.add_implementation(Implementation)
        return Implementation

class _Specification:

    def __init__(self):
        self._order = 0

    def __call__(self, specification):
        def _add_implementation(Implementation):
            if not hasattr(specification, 'implementations'):
                specification.implementations = []
            specification.implementations.append(Implementation)
        specification.add_implementation = _add_implementation
        def _verify(implementation='all'):
            if implementation == 'all':
                for imp in specification.implementations:
                    specification.__verifier__.verify(imp)
            else:
                specification.__verifier__.verify(implementation)
        specification.verify = _verify
        specification.__verifier__ = Verifier()
        for parent in getmro(specification):
            if hasattr(parent, '__verifier__'):
                specification.__verifier__.add_from(parent.__verifier__)
        specs = sorted([spec for _, spec in getmembers(specification,
                predicate=lambda x: hasattr(x, '__test_type__'))],
                key=lambda x: x._order)
        for spec in specs:
            spec = Spec(spec, spec.__test_type__)
            specification.__verifier__.add_spec(spec)
        return specification

    def construction(self, test):
        test.__test_type__ = 'construction'
        test._order = self._order
        self._order += 1
        return test

    def definition(self, test):
        test.__test_type__ = 'definition'
        test._order = self._order
        self._order += 1
        return test

Specification = _Specification()


if __name__ == '__main__':

    @Specification
    class MyStruct:

        @Specification.construction
        def mock_constructor(Struct):
            s = Struct()
            return s

        @Specification.definition
        def mock_test_1(struct):
            assert struct.x == 1
            struct.y = 3

        @Specification.definition
        def mock_test_2(struct):
            assert struct.y == 3


        @Specification.construction
        def mock_init(Struct):
            s = Struct()
            s.x = 6
            s.y = 7
            return s

        @Specification.definition
        def mock_test_alt(struct):
            assert struct.x == 6
            assert struct.y == 7


    @implements(MyStruct)
    class MyStructImplementation:

        def __init__(self):
            self.x = 1
            self.y = 2

    MyStruct.verify(MyStructImplementation)