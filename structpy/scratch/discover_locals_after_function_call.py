
import sys
import inspect


def foo(x, y):
    a = 2
    b = 3
    c = [x, y]
    return c


class GettingLocalsContext:

    def __init__(self, f):
        self.f = f
        self.locals = None
        self._old_profile = sys.getprofile()

    def __enter__(self):
        def tracer(frame, event, arg):
            frameinfo = inspect.getframeinfo(frame)
            print('frame', frame)
            print('event', event)
            print('arg', arg)
            print('frameinfo', frameinfo)
            print()
            if event == 'call' and frameinfo.function == self.f.__name__:
                print('!!!')
                self.locals = frame.f_locals
        sys.setprofile(tracer)  # !!! Replaces debugger or profiler! :(
        return self.locals

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.setprofile(self._old_profile)


def get_locals(f):
    return GettingLocalsContext(f)


if __name__ == '__main__':
    with get_locals(foo) as got:
        foo(3, 4)
        print('GOT', got)