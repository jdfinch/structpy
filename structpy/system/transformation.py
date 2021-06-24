

class Transformation:

    _transformed = {}

    def __new__(cls, _object=None, *args, **kwargs):
        if _object in Transformation._transformed.setdefault(cls, {}):
            result = Transformation._transformed[cls][_object]
            result.__init__(*args, **kwargs)
        elif _object is not None:
            result = cls.__new__(cls, _object, *args, **kwargs)
            Transformation._transformed.setdefault(cls, {})[_object] = result
            result.__init__(_object, *args, **kwargs)
        else:
            result = cls.__new__(cls, *args, **kwargs)
            result.__init__(_object, *args, **kwargs)
        return result


if __name__ == '__main__':

    from structpy.system.defaulted import Defaulted

    class MySingleton(Transformation, Defaulted):

        defaults = {'bar': 1, 'bat': 2}

        def __init__(self, foo=None, bar=None, bat=None):
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

