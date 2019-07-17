import speed

speed.make_sesssion()
speed.toggle_record()

def set_n(n):
    return set(range(n))

def list_n(n):
    return list(range(n))

def dict_n(n):
    return {i:i for i in range(n)}

def iteration(s, n):
    x = 0
    for i in range(n):
        for e in s:
            x += e

speed.header('Iteration tests:')
speed.time('iteration(set_n(10), 1000000)')
speed.time('iteration(set_n(1000), 10000)')
speed.time('iteration(list_n(10), 1000000)')
speed.time('iteration(list_n(1000), 10000)')

def membership(s, n):
    x = 0
    for i in range(n):
        for e in s:
            if e in s:
                x += 1

speed.header('Membership tests:')
speed.time('membership(set_n(3), 1000000)')
speed.time('membership(set_n(10), 1000000)')
speed.time('membership(set_n(100), 100000)')
speed.time('membership(list_n(3), 1000000)')
speed.time('membership(list_n(10), 1000000)')
speed.time('membership(list_n(100), 100000)')

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

def lookup(d, n):
    x = 0
    for i in range(n):
        for k in d:
            x += d[k]

def lookup_with_conditional(d, n):
    x = 0
    for i in range(n):
        for k in d:
            if k in d:
                x += d[k]

def lookup_with_member_var(o, n):
    x = 0
    for i in range(n):
        for k in o.d:
            x += o.d[k]

def lookup_with_getter(o, n):
    x = 0
    for i in range(n):
        for k in o.dictionary():
            x += o.val(k)

def lookup_with_getter_with_conditional(o, n):
    x = 0
    for i in range(n):
        for k in o.dictionary():
            x += o.safeval(k)

speed.header('Dict access tests:')
speed.time('lookup(dict_n(10), 10*6)')
speed.time('lookup_with_conditional(dict_n(10), 10*6)')
speed.time('lookup_with_member_var(obj(dict_n(10)), 10*6)')
speed.time('lookup_with_getter(obj(dict_n(10)), 10*6)')
speed.time('lookup_with_getter_with_conditional(obj(dict_n(10)), 10*6)')
