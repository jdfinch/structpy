
from unittest import TestCase, TestSuite, TextTestRunner


def _class_to_string(cls):
    string = str(cls)
    return string[string.rfind('.') + 1:-2]

class _Verifier:

    def __init__(self):
        self._examples = []
        self._definitions = []
        self._benchmarks = []
        self._scales = []
        self._evaluations = []
        self._checks = []

    def verify(self, struct):
        suite = TestSuite()
        suite.addTests([Example(struct) for Example in self._examples])
        TextTestRunner().run(suite)

    def add_example(self, test):
        class Example(TestCase):
            def __init__(self, struct):
                self.struct = struct
                self.test = test
                TestCase.__init__(self)
            def runTest(self):
                self.test(None, self.struct)
            def __str__(self):
                spec_string = _class_to_string(self.struct.__specification__)
                struct_string = _class_to_string(self.struct.__implementation__)
                test_string = test.test.__name__
                return '{}.{} example "{}"'.format(spec_string, struct_string, test_string)
            def __repr__(self):
                return str(self)
        self._examples.append(Example)

    def add_definition(self, test):
        class Definition(TestCase):
            def __init__(self, struct):
                self.struct = struct
                self.test = test
                TestCase.__init__(self)
            def runTest(self):
                self.test(None, self.struct)
            def __str__(self):
                spec_string = _class_to_string(self.struct.__specification__)
                struct_string = _class_to_string(self.struct.__implementation__)
                test_string = test.test.__name__
                return '{}.{} definition "{}"'.format(spec_string, struct_string, test_string)
            def __repr__(self):
                return str(self)
        self._definitions.append(Definition)

    def add_check(self, test):
        class Check(TestCase):
            def __init__(self, struct):
                self.struct = struct
                self.test = test
                TestCase.__init__(self)
            def runTest(self):
                self.test(None, self.struct)
            def __str__(self):
                spec_string = _class_to_string(self.struct.__specification__)
                struct_string = _class_to_string(self.struct.__implementation__)
                test_string = test.test.__name__
                return '{}.{} check "{}"'.format(spec_string, struct_string, test_string)
            def __repr__(self):
                return str(self)
        self._checks.append(Check)

class implements:
    def __init__(self, specification):
        self.spec = specification
    def __call__(self, implementation):
        class Implementation(implementation):
            __specification__ = self.spec
            __implementation__ = implementation
            @classmethod
            def verify_specification(cls):
                Implementation.__specification__.verify(cls)
        return Implementation

class Specification:

    verifier = _Verifier()

    class Test:
        def __init__(self, t, type):
            self.test = t
            self.type = type

        def __call__(self, *args, **kwargs):
            self.test(*args, **kwargs)

    @classmethod
    def example(cls, test):
        return Specification.Test(test, 'example')

    @classmethod
    def definition(cls, test):
        return Specification.Test(test, 'definition')

    @classmethod
    def check(cls, test):
        return Specification.Test(test, 'check')

    @classmethod
    def verify(cls, implementation):
        for _, test in cls.__dict__.items():
            if isinstance(test, Specification.Test):
                if test.type == 'example':
                    cls.verifier.add_example(test)
                elif test.type == 'definition':
                    cls.verifier.add_definition(test)
                elif test.type == 'check':
                    cls.verifier.add_check(test)
        cls.verifier.verify(implementation)






if __name__ == '__main__':


    class MyStruct(Specification):

        @Specification.example
        def mock_test_1(self, Struct):
            s = Struct()
            assert s.x == 1

        @Specification.example
        def mock_test_2(self, Struct):
            s = Struct()
            assert s.y == 2


    @implements(MyStruct)
    class MyStructImplementation:

        def __init__(self):
            self.x = 1
            self.y = 2

    MyStruct.Implementation = MyStructImplementation


    MyStruct.Implementation.verify_specification()
