import sys
from time import perf_counter
from traceback import format_exc
from inspect import signature, Parameter
from functools import partial

from structpy.system.printer import Printer, capture_stdout, capture_stderr
from structpy.system.dclass import Dclass


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

    def __init__(self, f):
        self.function = f if not isinstance(f, UnitTest) else f.function
        self._bound_functions = [partial(self.function)]

    @property
    def bound_function(self):
        return self._bound_functions[-1]

    def run(self, output=False):
        stdout_cap = capture_stdout(silence=not output)
        stderr_cap = capture_stderr(file=Printer('red', file=stdout_cap.stdout))
        with stdout_cap, stderr_cap:
            error = None
            traceback = None
            bound_args = []
            bound_kwargs = {}
            result = None
            ti = perf_counter()
            try:
                bound_args = self.bound_function.args
                bound_kwargs = self.bound_function.keywords
                ti = perf_counter()
                result = self.bound_function()
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
        return self._bind(partial(self.function, *args, **kwargs))

    def unbind(self, all=False):
        if all:
            self._bound_functions = self._bound_functions[:1]
        elif len(self._bound_functions) > 1:
            self._bound_functions.pop()

    def _bind(self, bound_function):
        self._bound_functions.append(bound_function)
        return self

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

    @property
    def name(self):
        return self.function.__name__

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unbind()


if __name__ == '__main__':

    import pprint

    def my_test(c, e, z, blah=4):
        x = c(e)
        print('Running my test!', 'Result:', x, ', and z is', z)
        for y in e:
            assert y in x
        assert False

    my_unit_test = UnitTest(my_test)
    my_unit_test = my_unit_test.try_bind_default(list, {1, 2, 3}, x=2)
    my_result = my_unit_test.run(output=True)
    # print(my_unit_test)
    # pprint.pprint(my_result())
    print('done')

