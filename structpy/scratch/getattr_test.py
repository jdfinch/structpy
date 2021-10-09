
from inspect import getmembers, isfunction

def callall(f):
    f()
    lineno = lambda x: x[1].__code__.co_firstlineno
    members = getmembers(f, isfunction)
    print(f'members: {members}')
    subfunctions = sorted(members, key=lineno)
    for subf in subfunctions:
        print(f'calling {subf.__name__}')
        subf()


callall(foo)