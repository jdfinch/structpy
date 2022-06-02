
def spec(f=None, /, **kwargs): return f
spec.set = lambda **kwargs: ...


@spec
def MyClassSpec(
        MyClass,
        my_obj = 'complicated' + 'thing'
):

    def __init__():
        nonlocal my_obj
        my_obj = ['hello']
        print('__init__', my_obj)

    def foo():
        print('foo:', my_obj)
        return my_obj

    def bar():
        ...

    def bat():
        ...

    def baz():
        ...

    return locals()


results = []
units = MyClassSpec(None)
print(units)
for name, test in units.items():
    if callable(test):
        test()
        print('fd')
print(units)