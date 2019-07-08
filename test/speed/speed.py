
import time
import math

f = open('speed.txt', 'w')

def t(func):
    def inner(*args, **kwargs):
        times = []
        for n in range(5):
            begin = time.time()
            func(*args, **kwargs)
            end = time.time()
            times.append(end - begin)
        avg = sum(times) / len(times)
        arg_strs = [str(x) for x in args]
        for i in range(len(arg_strs)):
            s = arg_strs[i]
            if len(s) > 10:
                arg_strs[i] = s[:10] + '...'
        kwarg_strs = [str(k) + '=' + str(v)[:10] for k, v in kwargs.items()]
        return func.__name__ + '(' + ', '.join(arg_strs) \
            + ', '.join(kwarg_strs) + '): ' + str(avg)
    return inner

def h(text):
    print()
    print(text)

def r(text):
    print(text)
    print()

def p(*args, sep=' ', end='\n'):
    print(*args, sep=sep, end=end)
    f.write(' '.join([str(a) for a in args]) + '\n')
