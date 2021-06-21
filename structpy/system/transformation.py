

class Transformation:

    _transformed = {}

    def __new__(cls, obj, *args, **kwargs):
        if obj in cls._transformed:
            return cls._transformed[obj]
        else:
            new_obj = object.__new__(cls)
            cls._transformed[obj] = new_obj
            return new_obj


if __name__ == '__main__':

    from structpy.system.defaulted import Defaulted

    class MySingleton(Transformation, Defaulted):

        defaults = {'bar': 1, 'bat': 2}

        def __init__(self, foo, bar=None, bat=None):
            self.foo = foo
            self.bar = bar
            self.bat = bat

        def __str__(self):
            return f'{self.foo}-{self.bar}-{self.bat}-{id(self)}'

    s1 = MySingleton('x')
    print(s1)
    s1.bar = 'y'
    print(s1)
    s2 = MySingleton('x', bat='z')
    print(s2)

