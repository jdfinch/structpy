
from structpy.specification.recompile import RecompiledFunction


class VarLink:

    def __init__(self):
        self.globals = {}
        self.locals = {}

    def __call__(self, globals, locals):
        self.globals = globals
        self.locals = locals

__varlink__ = VarLink()


class RecompiledUnitFunction(RecompiledFunction):

    def __init__(self, f, globals=None, locals=None, keep_code=False):
        self.vars = VarLink()
        if globals is None:
            globals = dict(__varlink__=self.vars)
        else:
            globals.update(dict(__varlink__=self.vars))
        RecompiledFunction.__init__(self, f, globals, locals, keep_code)

    def before(self):
        __varlink__(globals(), locals())

    def after(self):
        ...


if __name__ == '__main__':

    a = 1

    def foo(x, y):
        z = a + x + y
        return z

    foo = RecompiledUnitFunction(foo, globals(), keep_code=True)
    print(foo.code)

    result = foo(3, 4)
    print(result)
    print(foo.vars.globals)
    print(foo.vars.locals)
