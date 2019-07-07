
import time
import math

f = open('speed.txt', 'w')

def run_time_tests(func):
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

def print_text_after_newline(text):
    print()
    print(text)

def print_text_before_newline(text):
    print(text)
    print()

def write_args_to_file(*args, sep=' ', end='\n'):
    print(*args, sep=sep, end=end)
    f.write(' '.join([str(a) for a in args]) + '\n')
