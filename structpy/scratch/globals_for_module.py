
x = 1
y = 2


def foo():
    print(globals())
    global x
    z = x + y
    x = 3
    print(locals())
    print(globals())




if __name__ == '__main__':
    foo()