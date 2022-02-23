
from typing import KeysView, ValuesView

d = {'a': 1, 'b': 2, 'c': 3}
k = d.keys()
print(k)
ik = iter(k)
d['d'] = 4
del d['b']
print(k)
for e in ik:
    print(e, end=', ')
print('\n')
for e in d.keys():
    d['e'] = 5
    print(e, end=', ')