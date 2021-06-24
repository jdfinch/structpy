

class Defaulted:

    defaults = {}
    default = None

    def __setattr__(self, key, value):
        if key in self.defaults:
            defaultvalue = self.defaults[key]
            if value == self.default:
                if not hasattr(self, key):
                    if callable(defaultvalue):
                        self.__dict__[key] = defaultvalue()
                    else:
                        self.__dict__[key] = defaultvalue
            elif callable(defaultvalue):
                self.__dict__[key] = defaultvalue(value)
            else:
                self.__dict__[key] = value
        else:
            self.__dict__[key] = value


if __name__ == '__main__':

    class Foo(Defaulted):

        defaults = {
            'bar': list,
            'bat': dict,
            'baz': 2
        }

        def __init__(self, bar=None, bat=None, baz=None):
            self.update(bar, bat, baz)

        def update(self, bar=None, bat=None, baz=None):
            self.bar = bar
            self.bat = bat
            self.baz = baz

        def __str__(self):
            return f'{self.bar}-{self.bat}-{self.baz}'


    foo = Foo(bar='hello')
    print(foo)
    foo.update([1, 2, 3])
    print(foo)