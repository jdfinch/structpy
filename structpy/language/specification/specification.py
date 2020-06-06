
from structpy.language.specification.verifier import Verifier
from structpy.language.specification.spec import Spec
from inspect import getmembers


def __verify__(cls):
    cls.__specification__.__verify__(cls)


class Implementation:
    def __init__(self, specification):
        self.__specification__ = specification
    def __call__(self, implementation):
        implementation.__specification__ = self.__specification__
        implementation.__verify__ = classmethod(__verify__)
        self.__specification__.__add_implementation__(implementation)
        if hasattr(implementation, '__kwargs__'):
            tmp = implementation.__kwargs__
        else:
            tmp = {}
        if hasattr(implementation.__specification__, '__kwargs__'):
            implementation.__kwargs__ = implementation.__specification__.__kwargs__
        else:
            implementation.__kwargs__ = {}
        implementation.__kwargs__.update(tmp)
        return implementation


class _Specification:
    """
    spec decorator
    """

    def __init__(self):
        self._order = 0

    def __call__(self, specification_class):
        """
        spec decorate function, as in

        ```
        @spec(specification)
        class ...
        ```

        specification: the class that is loaded as a specification
        """

        def _add_implementation(Implementation_):
            """
            function to be added to the `specification_class`

            allows adding an implementation to the `specification_class`
            """
            if not hasattr(specification_class, '__implementations__'):
                specification_class.__implementations__ = []
            specification_class.__implementations__.append(Implementation_)

        def _verify(implementation='all'):
            """
            function to be added to the `specification class`

            verifies a provided impementation, or all implementations defined
            in the `__implementations__` list
            """
            if implementation == 'all':
                for imp in specification_class.__implementations__:
                    specification_class.__verifier__.verify(imp)
            else:
                specification_class.__verifier__.verify(implementation)

        def _implementation():
            """
            function to be added to the `specification_class`

            gets the default implementation of the specification
            """
            return specification_class.__implementations__[0] \
                    if hasattr(specification_class, '__implementations__') \
                       and specification_class.__implementations__ else None

        # add the functions to the `specification_class`
        specification_class.__add_implementation__ = _add_implementation
        specification_class.__verify__ = _verify
        specification_class.__verifier__ = Verifier()
        specification_class.__implementation__ = _implementation()

        # sort the tests defined in the `specification_class` by order of appearance
        specs = sorted(
            [spec for _, spec in getmembers(specification_class,
                predicate=lambda x: hasattr(x, '__test_type__'))],
            key=lambda x: x._order
        )
        for spec in specs:
            spec = Spec(spec, spec.__test_type__)
            specification_class.__verifier__.add_spec(spec)
        return specification_class

    def init(self, test):
        """
        spec.init decorate function, as in

        ```
        @spec.init
        def ...
        ```

        Marks the start of a test list,
        where an object is constructed and returned.
        """
        test.__test_type__ = 'construction'
        test._order = self._order
        self._order += 1
        return test

    def prop(self, test):
        """
        spec.prop decorate function, as in

        ```
        @spec.prop
        def ...
        ```

        Marks a specification test that represents
        a method in the eventual implementation class.
        """
        test.__test_type__ = 'definition'
        test._order = self._order
        self._order += 1
        return test

    def test(self, test):
        """
        spec.test decorate function, as in

        ```
        @spec.test
        def ...
        ```

        Marks a specification test that addresses some
        behavior of the eventual implementation, but does
        not necessarily correspond to a implementation
        method.
        """
        test.__test_type__ = 'test'
        test._order = self._order
        self._order += 1
        return test

spec = _Specification()


if __name__ == '__main__':

    @spec
    class MyStruct:

        @spec.init
        def mock_constructor(Struct):
            s = Struct()
            return s

        @spec.prop
        def mock_test_1(struct):
            assert struct.x == 1
            struct.y = 3

        @spec.prop
        def mock_test_2(struct):
            assert struct.y == 3


        @spec.init
        def mock_init(Struct):
            s = Struct()
            s.x = 6
            s.y = 7
            return s

        @spec.prop
        def mock_test_alt(struct):
            assert struct.x == 6
            assert struct.y == 7

        @spec.test
        def mock_test(struct):
            assert struct.x == 5
            assert True


    @Implementation(MyStruct)
    class MyStructImplementation:

        def __init__(self):
            self.x = 1
            self.y = 2

    MyStruct.__verify__(MyStructImplementation)