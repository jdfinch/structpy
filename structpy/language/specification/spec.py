
from unittest import TestCase, TestSuite, TextTestRunner
from inspect import signature


class Spec(TestCase):
    """
    Run a test function.

    By default, the test function will be passed None for each expected argument.

    If an object is specified, the object will be passed as the functions first arg.
    """

    def __init__(self, test, type=None, object=None):
        if type is None:
            type = 'test'
        self._object = object
        self._test_fn = test
        self._type = type
        TestCase.__init__(self)

    def type(self):
        return self._type

    def object(self):
        return self._object

    def set_object(self, object):
        self._object = object

    def run_test(self):
        return self.runTest()

    def runTest(self):
        sig = signature(self._test_fn)
        nargs = len(sig.parameters)
        if self._object is not None:
            return self._test_fn(self._object, *([None] * (nargs - 1)))
        else:
            return self._test_fn(*([None] * nargs))

    def __str__(self):
        type_string = str(self._type)
        test_string = self._test_fn.__name__
        if self._object:
            def _class_to_string(cls):
                string = str(cls)
                return string[string.rfind('.') + 1:-2]
            if hasattr(self._object, '__specification__'):
                spec_string = _class_to_string(self._object.__specification__)
                object_string = _class_to_string(self._object.__implementation__)
                return '{}.{} {} "{}"'.format(spec_string, object_string, type_string, test_string)
            else:
                return '{} {} "{}"'.format(str(self._object), type_string, test_string)
        else:
            return '{} "{}"'.format(type_string, test_string)

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    o = (lambda:None)
    o.a = 1
    o.b = 2

    def test_fn(x, y):
        assert x.a == 1
        assert x.b == 2
        assert y is None

    test = Spec(test_fn)
    test.set_object(o)

    test_suite = TestSuite()
    test_suite.addTest(test)
    TextTestRunner().run(test_suite)