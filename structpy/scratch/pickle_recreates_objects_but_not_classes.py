
import pickle

class Sym:
    pass

class Foo:
    bar=Sym

    def __init__(self):
        self.bat = Sym

    def save(self, file):
        with open(file, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, file):
        with open(file, 'rb') as f:
            return pickle.load(f)

from sys import getsizeof

file = 'test.pkl'
x = Foo()
x.save(file)
y = Foo.load(file)
print(x)
print(y)
print(x is y)
print(type(x) is type(y))
print(x.bar is y.bar)
print(x.bat is y.bat)


