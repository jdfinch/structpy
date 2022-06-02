

from time import perf_counter_ns


n = 10 ** 6
l = list(range(n))
d = dict(zip(l, l))

ti = perf_counter_ns()
print(next(iter(d)))
tf = perf_counter_ns()
print('Forward:', tf - ti)

ti = perf_counter_ns()
print(next(iter(d)))
tf = perf_counter_ns()
print('Forward:', tf - ti)

ti = perf_counter_ns()
print(next(reversed(d)))
tf = perf_counter_ns()
print('Reverse:', tf - ti)

ti = perf_counter_ns()
print(next(reversed(d.items())))
tf = perf_counter_ns()
print('Reversed items:', tf - ti)