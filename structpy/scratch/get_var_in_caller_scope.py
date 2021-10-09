
from inspect import currentframe


class Ctx:

    def __init__(self):
        self.inital_locals = None

    def __enter__(self):
        self.inital_locals = dict(currentframe().f_back.f_locals)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        final_locals = {k: v for k, v in currentframe().f_back.f_locals.items() if k not in self.inital_locals}
        print(final_locals)


def mything():
    a = 1
    b = 1
    with Ctx():
        c = 3
        d = 4

mything()