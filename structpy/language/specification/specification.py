
from structpy.language.specification.verifier import Verifier
from structpy.language.specification.spec import Spec
from inspect import getmembers
import types
from sys import stderr

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
        self._constructor = None

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
            [v for k, v in specification_class.__dict__.items() if hasattr(v, '__test_type__')],
            key=lambda x: x._order
        )
        print('\n'.join([str(x) for x in specs]), file=stderr)
        initial_construction = Spec(lambda: None)
        construction = initial_construction
        ls = []
        for s in specs:
            s = Spec(s, s.__test_type__)
            if s.type() == 'construction':
                if construction != initial_construction or ls:
                    specification_class.__verifier__.add_spec_list(construction, ls)
                    ls = []
                construction = s
            else:
                ls.append(s)
        if ls:
            specification_class.__verifier__.add_spec_list(construction, ls)
        return specification_class

    def init(self, test):
        """
        spec.init decorate function, as in

        ```
        @spec.init
        def ...
        ```

        Marks the start of a unit list,
        where an object is constructed and returned.
        """
        test.__test_type__ = 'construction'
        test._sequence = []
        test._order = self._order
        self._order += 1
        self._constructor = test
        return test

    def prop(self, test):
        """
        spec.prop decorate function, as in

        ```
        @spec.prop
        def ...
        ```

        Marks a specification unit that represents
        a method in the eventual implementation class.
        """
        test.__test_type__ = 'definition'
        test._order = self._order
        self._order += 1
        if self._constructor:
            self._constructor._sequence.append(test)
        return test

    class _sats:

        def __init__(self, specification, reference):
            self.specification = specification
            self.reference = reference

        def __call__(self, test):
            test.__test_type__ = 'construction'
            test._order = self.specification._order
            test._sequence = list(self.reference._sequence)
            for t in test._sequence:
                setattr(self.specification, 'placeholder', t)
            self.specification._order += 1
            self.specification._constructor = test
            return test

    def sats(self, reference):
        return _Specification._sats(self, reference)


spec = _Specification()


if __name__ == '__main__':

    @spec
    class ToImport:

        @spec.init
        def not_imported(Struct):
            s = Struct()
            s.x = 999

        @spec.prop
        def imported(struct):
            assert struct.x == 999

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

        @spec.sats(ToImport.not_imported)
        def construct_to_satisfy(Struct):
            s = Struct()
            s.x = 0
            s.x += 999
            s.y = 8

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

        @spec.prop
        def mock_test(struct):
            assert struct.x == 5
            assert True


    @Implementation(MyStruct)
    class MyStructImplementation:

        def __init__(self):
            self.x = 1
            self.y = 2

    MyStruct.__verify__(MyStructImplementation)