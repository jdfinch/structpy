

from functools import partial

class Pipe(list):

    def __init__(self, *functions):
        list.__init__(self)
        for function in functions:
            if isinstance(function, args):
                self[-1] = partial(self[-1], *function.args, **function.kwargs)
            else:
                self.append(function)

    def __call__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs:
            result = args[0]
        elif len(args) == 0 and not kwargs:
            result = None
        elif not kwargs:
            result = args
        elif not args:
            result = kwargs
        else:
            result = args, kwargs
        for function in self:
            result = function(*args, **kwargs)
            if isinstance(result, tuple):
                args = result
            else:
                args = (result,)
            kwargs = {}
        return result

class args:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

def pipeline(*functions_and_arguments):
    return Pipe(*functions_and_arguments)()


from time import time
class timer:

    def __init__(self, f=None):
        if f is None:
            f = print
        self.f = f
        self.t1 = None

    def __enter__(self):
        self.t1 = time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        t2 = time()
        self.f(t2 - self.t1)


def nested(x):
    if x % 9 != 0:
        if x % 8 != 0:
            if x % 7 != 0:
                if x % 2 != 0:
                    return x
                else:
                    return None
            else:
                return None
        else:
            return None
    else:
        return None



def unnested(x):
    return pipeline(
        check, args(x, m=9),
        check, args(m=8),
        check, args(m=7),
        check, args(m=2)
    )

def check(x, m):
    if x is not None and x % m != 0:
        return x
    else:
        return None


if __name__ == '__main__':
    def show(code):
        result = eval(code)
        print(code + ':', result)
    def heading(text):
        print('\n' + '{:#^20}'.format(' {} '.format(text)))

    with timer(partial(print, 'Time:')):
        heading('Nested')
        show('nested(9)')
        show('nested(16)')
        show('nested(4)')
        show('nested(3)')

    with timer(partial(print, 'Time:')):
        heading('Unnested')
        show('unnested(9)')
        show('unnested(16)')
        show('unnested(4)')
        show('unnested(3)')