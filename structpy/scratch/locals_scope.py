

def foo():
    x = 1

    def bar():
        nonlocal x
        y = x + 1
        x = 3

        print(x, y)

    bar()
    print(x)


if __name__ == '__main__':
    foo()