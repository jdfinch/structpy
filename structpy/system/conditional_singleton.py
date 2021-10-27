

class ConditionalSingleton:
    """
    Superclass that creates conditional-singletons.

    Instantiating a ConditionalSingleton will return a pre-existing object
    if the first argument passed to the constructor is not None and
    the constructor has already been invoked with that first arg.

    This allows inheritors to guarantee a one-to-one relationship
    between instantiated objects and objects passed into the constructor.
    """

    _transformed = {}

    def __new__(cls, singleton=None, *args, **kwargs):
        if singleton in ConditionalSingleton._transformed.setdefault(cls, {}):
            result = ConditionalSingleton._transformed[cls][singleton]
        elif singleton is not None:
            result = object.__new__(cls)
            ConditionalSingleton._transformed.setdefault(cls, {})[singleton] = result
            result.__init__(singleton, *args, **kwargs)
        else:
            result = object.__new__(cls)
            result.__init__(singleton, *args, **kwargs)
        return result


if __name__ == '__main__':

    from structpy.system.dclass import dclass

    class MySingleton(ConditionalSingleton, dclass):

        def __init__(self, *args, **kwargs):
            self.foo = 1
            self.bar = 2
            self.bat = 3
            dclass.__init__(self, *args, **kwargs)


        def __str__(self):
            return f'{self.foo}-{self.bar}-{self.bat}-{id(self)}'


    s1 = MySingleton('x')
    print(s1)
    s1.bar = 'y'
    print(s1)
    s2 = MySingleton('x', bat='z')
    print(s2)
    s3 = MySingleton(None, 'x', 'y')
    print(s3)
    print(MySingleton._transformed)

