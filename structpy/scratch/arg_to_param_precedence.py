

def foo(a, b, *args, **kwargs):
    print(a)
    print(b)
    print(args)
    print(kwargs)


foo(1, 2, 3, b=4) # TypeError: got multiple values for argument