
g = 4

class Foo:

    def foo(self):
        global Foo
        Foo = Foo
        global g
        return locals(), globals()


f = Foo()
print(*f.foo(), sep='\n')