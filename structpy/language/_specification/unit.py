
from inspect import signature
import sys, traceback, time
from structpy.language._specification.result import Result, ResultList


class unit:
    """
    Decorator taking a class method as input and producing a Unit object
    """

    def __init__(self, *tags, time_requirement=None):
        self.time_requirement = time_requirement
        self.tags = tags

    def __call__(self, method):
        return Unit(method, *self.tags, time_requirement=self.time_requirement)


class Unit:
    """
    Unit test, which is the result of decoration of a unit test method:

    ```
    @unit
    def my_unit_test(struct):
        ...
    ```
    """

    def __init__(self, method, *tags, time_requirement=None):
        self.method = method
        self.should_pass = True
        self.time_requirement = time_requirement
        self.tags = tags

    def test(self, *args):
        """
        Run the unit test.

        `*args` will be passed to the test method.
        """
        sig = signature(self.method)
        nargs = len(sig.parameters)
        result = Result()
        obj = None
        t0 = time.time()
        try:
            if nargs > 0:
                argv = [*args] + [None] * (nargs - len(args))
            else:
                argv = []
            t0 = time.time()
            obj = self.method(*argv)
            t1 = time.time()
            traceback_message = None
        except Exception:
            t1 = time.time()
            exc_type, exc_value, exc_tb = sys.exc_info()
            tbe = traceback.TracebackException(exc_type, exc_value, exc_tb)
            traceback_message = ''.join(tbe.format())
        time_elapsed = t1 - t0
        result.unit = self
        result.traceback = traceback_message
        result.time_requirement = self.time_requirement
        result.time_elapsed = time_elapsed
        result.time_passed = result.time_requirement is None or result.time_elapsed <= result.time_requirement
        result.passed = result.traceback is None
        result.obj = obj
        return result

















