import sys
sys.path.append(sys.path[0][:sys.path[0].find('structpy')])

from speed import print_text_after_newline, run_time_tests, print_text_before_newline, write_args_to_file
from structpy.collections import PriorityQueue

def set_n(n):
    return set(range(n))

def even_set_n(n):
    return set([i*2 for i in range(n)])

def list_n(n):
    return list(range(n))

def dict_n(n):
    return {i:i for i in range(n)}

def priority_queue_n(n):
    return PriorityQueue([i*2 for i in range(n)])
"""
@run_time_tests
def iteration(s, n):
    x = 0
    for i in range(n):
        for e in s:
            x += e

print_text_after_newline('Iteration tests:')
write_args_to_file('set length 10:', iteration(set_n(10), 1000000))
write_args_to_file('set length 1000:', iteration(set_n(1000), 10000))
write_args_to_file('list length 10:', iteration(list_n(10), 1000000))
write_args_to_file('list length 1000:', iteration(list_n(1000), 10000))

@run_time_tests
def membership(s, n):
    x = 0
    for i in range(n):
        for e in s:
            if e in s:
                x += 1

print_text_after_newline('Membership tests:')
write_args_to_file('set length 3:', membership(set_n(3), 1000000))
write_args_to_file('set length 10:', membership(set_n(10), 1000000))
write_args_to_file('set length 100:', membership(set_n(100), 100000))
write_args_to_file('list length 3:', membership(list_n(3), 1000000))
write_args_to_file('list length 10:', membership(list_n(10), 1000000))
write_args_to_file('list length 100:', membership(list_n(100), 100000))

class obj:
    def __init__(self, d):
        self.d = d
    def dictionary(self):
        return self.d
    def val(self, key):
        return self.d[key]
    def safeval(self, key):
        if key in self.d:
            return self.d[key]

@run_time_tests
def access(d, n):
    x = 0
    for i in range(n):
        for k in d:
            x += d[k]

@run_time_tests
def access_safe(d, n):
    x = 0
    for i in range(n):
        for k in d:
            if k in d:
                x += d[k]

@run_time_tests
def access_obj(o, n):
    x = 0
    for i in range(n):
        for k in o.d:
            x += o.d[k]

@run_time_tests
def access_obj_fun(o, n):
    x = 0
    for i in range(n):
        for k in o.dictionary():
            x += o.val(k)

@run_time_tests
def access_obj_safe(o, n):
    x = 0
    for i in range(n):
        for k in o.dictionary():
            x += o.safeval(k)

print_text_after_newline('Dict access tests:')
write_args_to_file('10 items --')
d = dict_n(10)
o = obj(d)
write_args_to_file(access(d, 1000000))
write_args_to_file(access_safe(d, 1000000))
write_args_to_file(access_obj(o, 1000000))
write_args_to_file(access_obj_fun(o, 1000000))
write_args_to_file(access_obj_safe(o, 1000000))
"""

"""
NOTE: The s argument gets modified after the first iteration and then the iterations afterwards are doing less work
since the task was already accomplished
"""
@run_time_tests
def insertion(s, n):
    for i in range(n):
        s.add((i*2)+1)

print_text_after_newline('Insertion tests:')
write_args_to_file('set length 10:', insertion(even_set_n(10), 10000))
write_args_to_file('set length 10000:', insertion(even_set_n(10000), 10000))
write_args_to_file('priority queue 10:', insertion(even_set_n(10), 10000))
write_args_to_file('priority queue 10000:', insertion(even_set_n(10000), 10000))
