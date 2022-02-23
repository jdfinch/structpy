
class Foo:

    def add(self, other):
        return other

    __add__ = add


f = Foo()
print(f + 3)