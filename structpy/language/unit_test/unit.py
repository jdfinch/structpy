
from inspect import signature, Parameter
import sys, traceback, time
from structpy.language.unit_test.result import Result


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

    def __init__(self, method, *tags, args=None, kwargs=None, time_requirement=None):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        self.method = method
        self.should_pass = True
        self.args = args
        self.kwargs = kwargs
        self.time_requirement = time_requirement
        self.tags = tags


    def set_args(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


    def test(self, *args, **kwargs):
        """
        Run the unit test.

        `*args` and `**kwargs` will be passed to the test method.
        """
        if args:
            self.args = args
        if kwargs:
            self.kwargs = kwargs
        args, kwargs = self.args, self.kwargs
        sig = signature(self.method)
        args = list(reversed(args)) if args else None
        arguments = {}
        for parameter in sig.parameters:
            if args:
                arguments[parameter] = args.pop()
            elif kwargs and parameter in kwargs:
                arguments[parameter] = kwargs[parameter]
        result = Result()
        obj = None
        t0 = time.time()
        try:
            t0 = time.time()
            obj = self.method(**arguments)
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
        result.time_passed = result.time_requirement is None \
                             or result.time_elapsed <= result.time_requirement
        result.passed = result.traceback is None
        result.obj = obj
        return result
















