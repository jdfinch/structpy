
from time import perf_counter


def foo(x):

    def bar(y):
        a = []
        b = {}
        c = []
        d = [None] * 10 ** 6
        e = ()
        f = []
        g = {}
        h = []
        # print('bar:', locals().keys())
        return x + y

    return locals()


def bat(x):
    a = []
    b = {}
    c = []
    d = [None]
    e = ()
    f = []
    g = {}
    h = []
    # print('bat:', locals().keys())
    return locals()


ti = perf_counter()
for i in range(10**6):
    foo(i)
tf = perf_counter()
print(tf - ti)

ti = perf_counter()
for i in range(10**6):
    bat(i)
tf = perf_counter()
print(tf - ti)