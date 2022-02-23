
def foo(bar=None, **kwargs):
    print('bar:', bar)
    print(kwargs)

foo(bar=4)  # 1st param bar steals kwarg