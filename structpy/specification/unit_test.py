import sys
from time import perf_counter
from traceback import format_exc
import typing

from structpy.system.printer import Printer, capture_stdout, capture_stderr
from structpy.system.dclass import Dclass
from structpy.specification.default_binder import DefaultBinder


class UnitTest:
    """
    Wrapper for a test function designed to evaluate the correctness
    of some implementation code.
    """

    class Result(Dclass):

        def __init__(self, **attrs):
            self.unit = None
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

    def __init__(self, f: typing.Union[typing.Callable, 'UnitTest']):
        self.function = ...
        self.function = f.function if isinstance(f, UnitTest) else f
        self._binder = DefaultBinder(self.function, force_namespace=True)
        self._binding = self._binder.arguments()

    def run(self, output=False):
        stdout_cap = capture_stdout(silence=not output)
        stderr_cap = capture_stderr(file=Printer('red', file=stdout_cap.stdout))
        with stdout_cap, stderr_cap:
            error = None
            traceback = None
            bound_args, bound_kwargs = self._binding
            result = None
            ti = perf_counter()
            try:
                ti = perf_counter()
                result = self.function(*bound_args, **bound_kwargs)
                timedelta = perf_counter() - ti
            except Exception as e:
                timedelta = perf_counter() - ti
                error = e
                traceback = format_exc()
                print(traceback, file=sys.stderr)
        results = UnitTest.Result(
            unit=self,
            args=bound_args,
            kwargs=bound_kwargs,
            timedelta=timedelta,
            error=error,
            traceback=traceback,
            stdout=stdout_cap.record,
            stderr=stderr_cap.record,
            result=result
        )
        return results

    def bind(self, *args, **kwargs):
        self._binding = self._binder.arguments(*args, **kwargs)

    @property
    def name(self):
        return self.function.__name__

    def __str__(self):
        return f'<UnitTest {self.function.__module__+"." if hasattr(self.function, "__module__") else ""}{self.function.__name__}>'

    def __repr__(self):
        return str(self)


if __name__ == '__main__':

    import pprint

    def my_test(c, e, z, blah=4):
        x = c(e)
        print('Running my test!', 'Result:', x, ', and z is', z)
        for y in e:
            assert y in x
        assert False

    my_unit_test = UnitTest(my_test)
    my_unit_test.bind(list, {1, 2, 3}, x=2)
    my_result = my_unit_test.run(output=True)
    print(my_unit_test)
    pprint.pprint(my_result())
    print('done')

