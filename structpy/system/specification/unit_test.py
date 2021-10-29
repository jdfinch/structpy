
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
        if isinstance(f, UnitTest):
            self.function = f.function
            Dclass.__init__(self, **f())
        else:
            self.function = f
        self.bound_function = partial(self.function)
        Dclass.__init__(self, **attrs)

    def bind(self, *args, **kwargs):
        return self._bind(partial(self.function, *args, **kwargs))

    def _bind(self, bound_function):
        context = BoundUnitTestContext(self, bound_function)
        self.bound_function = bound_function
        return context

    def try_bind_default(self, *args, **kwargs):
        f = self._try_bind(self.function, *args, **kwargs)
        return self._bind(self._bind_default(f))

    def try_bind(self, *args, **kwargs):
        return self._bind(self._try_bind(self.function, *args, **kwargs))

    def _try_bind(self, f, *args, **kwargs):
        params = signature(f).parameters
        has_varg = any((param.kind is Parameter.VAR_POSITIONAL for param in params.values()))
        has_vkwarg = any((param.kind is Parameter.VAR_KEYWORD for param in params.values()))
        bound_kwargs = {
            kw: kwargs[kw] for kw in kwargs
            if has_vkwarg or (kw in params and params[kw].kind not in
            {Parameter.POSITIONAL_ONLY, Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD})
        }
        bound_args = []
        for i, (param_name, param) in enumerate(params.items()):
            if param.kind in {Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD}:
                if has_varg or len(args) > i:
                    if param_name in bound_kwargs:
                        bound_args.append(bound_kwargs[param_name])
                        del bound_kwargs[param_name]
                    else:
                        bound_args.append(args[i])

        bound_f = partial(f, *bound_args, **bound_kwargs)
        return bound_f

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
            bound_args = []
            bound_kwargs = {}
            result = None
            ti = time()
            try:
                f = partial(self.bound_function, *args, **kwargs)
                bound_args = f.args
                bound_kwargs = f.keywords
                ti = time()
                result = f()
                timedelta = time() - ti
            except Exception as e:
                timedelta = time() - ti
                error = e
                traceback = format_exc()
        results = Result(
            function=self.function,
            args=bound_args,
            kwargs=bound_kwargs,
            timedelta=timedelta,
            error=error,
            traceback=traceback,
            stdout=''.join(stdout_captured),
            stderr=''.join(stderr_captured),
            result=result
        )
        return results

    @property
    def name(self):
        return self.function.__name__


class BoundUnitTestContext(UnitTest):

    def __init__(self, unit, bound_function):
        UnitTest.__init__(self, unit)
        self._unit = unit
        self._old_bound_function = unit.bound_function
        self.bound_function = bound_function

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._unit.bound_function = self._old_bound_function
        self.bound_function = self._old_bound_function


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
    my_unit_test = my_unit_test.try_bind_default(list, {1, 2, 3}, x=2)
    my_result = my_unit_test.run()
    print(my_unit_test)
    pprint.pprint(my_result())

