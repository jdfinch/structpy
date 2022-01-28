

def my_decorator(cls):

    class AlternateClass:

        defined_class = cls

        def alternate_method(self, x):
            return x + 1

    return AlternateClass()


@my_decorator
class MyClass:

    @classmethod
    def my_class_method(cls, x):
        return cls


print(MyClass)
print(MyClass.alternate_method(3))
print(MyClass.defined_class)
print(MyClass.defined_class.my_class_method(9))  # didn't get type hinting on defined_class.???

"""
<__main__.my_decorator.<locals>.AlternateClass object at 0x7f6a6c86bdc0>
4
<class '__main__.MyClass'>
<class '__main__.MyClass'>
"""

