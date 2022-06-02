
import inspect
import importlib


class Spec:
    def __init__(self, g=None, **kwargs):
        self.fns = {}
    def __getattr__(self, item):
        ...
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        ctxt = inspect.currentframe().f_back.f_globals
        for n, f in list(ctxt.items()):
            if inspect.isfunction(f):
                self.fns[n] = f


with Spec(
    doc="""
    My documentation for myspec.
    
    Does nothing. Is just a mock.
    """
) as myspec:

    with myspec.params:
        MyClass = (1, 2, 3)
        my_obj = None

    def __init__():
        global my_obj
        my_obj = list(MyClass)
        return my_obj

    def foo():
        return my_obj

    def bar():
        return my_obj



results = []
for name, fn in myspec.fns.items():
    results.append(fn())
    print(name, results[-1])

print('identity', results[0] is results[1])

foo()

print('globals module', importlib.import_module(__name__))
print(globals())

