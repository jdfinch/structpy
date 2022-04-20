

class Dclass:

    def __init__(self, *args, **kwargs):
        self(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        kws = iter(self.__dict__)
        for arg in args:
            kw = next(kws)
            setattr(self, kw, arg)
        for kw, arg in kwargs.items():
            setattr(self, kw, arg)
        return self.__dict__

    def __getattribute__(self, item):
        return object.__getattribute__(self, item)

    def __getattr__(self, item):
        return None

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __iter__(self):
        return iter(self.__dict__.values())

    def __contains__(self, item):
        return item in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __or__(self, other):
        return Dclass(**self.__dict__).__ior__(other)

    def __ior__(self, other):
        self(**other.__dict__)
        return self

    @property
    def __name__(self):
        return self.__class__.__name__

    def __str__(self):
        name = self.__name__
        itemstring = ', '.join((
            f'{k}={v}' for k, v in self.__dict__.items()
            if not k.startswith('_')
        ))
        return f'{name}({itemstring})'

    def __repr__(self):
        return str(self)


def dclass(name):
    def dclass_factory(*args, **kwargs):
        obj = Dclass(__name__=name)
        obj(*args, **kwargs)
        return obj
    return dclass_factory


if __name__ == '__main__':

    class Foo(Dclass):

        def __init__(self, d, *args, **kwargs):
            self.a = -1
            self.b = -2
            self.c = -3
            self.d = d
            Dclass.__init__(self, *args, **kwargs)


    f = Foo(4, 1, c=3, e=5)
    f.f = f.e + 1
    print(f)
    g = Foo(**f())
    x = g().setdefault('x', 99)
    y = g().setdefault('x', 100)
    g().update(x=101, y=102)
    g(a=9, b=8, c=7)
    print(y)
    print(g)
    f |= g
    print(f)
    for v in f:
        print(v)
