

call = lambda f: f()


def foo(x):
    x.append(2)
    @call
    def append_and_reverse(x=x, v=3):
        x.append(v)
        x.reverse()
        return x + [0]
    y = append_and_reverse + [0]
    return y

def foo(x):
    x.append(2)
    def append_and_reverse(x=x, v=3):
        x.append(v)
        x.reverse()
        return x + [0]
    a = append_and_reverse()
    y = a + [0]
    return y

if __name__ == '__main__':
    print(foo([1]))