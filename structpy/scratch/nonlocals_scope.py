
x = 1

def foo():

    y = 1

    def bar():

        z = 2
        # nonlocal y
        y = 2

        print(x, y, z)
        print(locals())
        print(globals())

    bar()

    print(x, y)

foo()