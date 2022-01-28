

Foo = [9, 8]
Foo.reverse()


class Foo:

    x = 3

    @classmethod
    def z(cls, y):
        print(Foo)
        return Foo.x + y


foo = Foo()
print(foo.z(5))
print(foo)


