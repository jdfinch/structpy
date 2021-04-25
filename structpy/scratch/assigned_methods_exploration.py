
class Foo:

    def bar(self, x):
        return x


class Bar:

    bat = Foo.bar


b = Bar()
print(b.bat(2))
