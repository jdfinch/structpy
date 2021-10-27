
from time import time
from traceback import format_exc
from inspect import signature, Parameter
from functools import partial

from structpy.system.printer import Printer
from structpy.system.dclass import Dclass


class UnitTest(Dclass):
    """
    Wrapper for a test function designed to evaluate the correctness
    of some implementation code.
    """

    def __init__(self, f, **attrs):
        self.function = f
        self.bound_function = partial(self.function)
        Dclass.__init__(self, **attrs)

    def bind(self, *args, **kwargs):
        self.bound_function = partial(self.function, *args, **kwargs)
        return self

    def _bind_default(self, f):
        params = signature(f).parameters.values()
        args = [
            {Parameter.empty: None}.get(param.default, param.default)
            for param in params
            if param.kind is Parameter.POSITIONAL_ONLY
        ]
        kwargs = {
            param.name: {Parameter.empty: None}.get(param.default, param.default)
            for param in params
            if param.kind not in
            {Parameter.POSITIONAL_ONLY, Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD}
        }
        return partial(f, *args, **kwargs)

    def run(self, *args, **kwargs):
        stdout_captured = []
        stderr_captured = []
        stdout_capture = Printer(file=stdout_captured)
        stderr_capture = Printer(file=stderr_captured)
        stdout = stdout_capture.capturing()
        stderr = stderr_capture.capturing(stdout=False, stderr=True)
        with stdout, stderr:
            error = None
            traceback = None
            f = partial(self.bound_function, *args, **kwargs)
            args = f.args
            kwargs = f.keywords
            f = self._bind_default(f)
            try:
                ti = time()
                result = f()
                timedelta = time() - ti
            except Exception as e:
                timedelta = time() - ti
                error = e
                traceback = format_exc()
                result = None
        results = Result(
            function=self.function,
            args=args,
            kwargs=kwargs,
            timedelta=timedelta,
            error=error,
            traceback=traceback,
            stdout=''.join(stdout_captured),
            stderr=''.join(stderr_captured),
            result=result
        )
        return results


class Result(Dclass):

    def __init__(self, **attrs):
        self.function = None
        self.args = None
        self.kwargs = None
        self.timedelta = None
        self.error = None
        self.stdout = None
        self.stderr = None
        self.traceback = None
        self.result = None
        Dclass.__init__(self, **attrs)

    @property
    def success(self):
        return self.error is None


if __name__ == '__main__':

    import pprint

    def my_test(c, e, z, blah=4):
        x = c(e)
        print('Running my test!', 'Result:', x, ', and z is', z, end='')
        for y in e:
            assert y in x
        assert len(x) == len(e)

    my_unit_test = UnitTest(my_test)
    my_result = my_unit_test.run(list, {1, 2, 3})
    pprint.pprint(my_result())

