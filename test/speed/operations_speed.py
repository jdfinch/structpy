from speed import h, t, r, p

def set_n(n):
    return set(range(n))

def list_n(n):
    return list(range(n))

def dict_n(n):
    return {i:i for i in range(n)}

@t
def iteration(s, n):
    x = 0
    for i in range(n):
        for e in s:
            x += e

h('Iteration tests:')
p('set length 10:', iteration(set_n(10), 1000000))
p('set length 1000:', iteration(set_n(1000), 10000))
p('list length 10:', iteration(list_n(10), 1000000))
p('list length 1000:', iteration(list_n(1000), 10000))

@t
def membership(s, n):
    x = 0
    for i in range(n):
        for e in s:
            if e in s:
                x += 1

h('Membership tests:')
p('set length 10:', membership(set_n(10), 1000000))
p('set length 100:', membership(set_n(100), 100000))
p('list length 10:', membership(list_n(10), 1000000))
p('list length 100:', membership(list_n(100), 100000))

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

@t
def access(d, n):
    x = 0
    for i in range(n):
        for k in d:
            x += d[k]

@t
def access_safe(d, n):
    x = 0
    for i in range(n):
        for k in d:
            if k in d:
                x += d[k]

@t
def access_obj(o, n):
    x = 0
    for i in range(n):
        for k in o.d:
            x += o.d[k]

@t
def access_obj_fun(o, n):
    x = 0
    for i in range(n):
        for k in o.dictionary():
            x += o.val(k)

@t
def access_obj_safe(o, n):
    x = 0
    for i in range(n):
        for k in o.dictionary():
            x += o.safeval(k)

h('Dict access tests:')
p('10 items --')
d = dict_n(10)
o = obj(d)
p(access(d, 1000000))
p(access_safe(d, 1000000))
p(access_obj(o, 1000000))
p(access_obj_fun(o, 1000000))
p(access_obj_safe(o, 1000000))
