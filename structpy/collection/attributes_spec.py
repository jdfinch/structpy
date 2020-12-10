
from structpy import specification


@specification
class AttributesSpec:
    """
    A dictionary allowing `.` operator to get and set
    key value pairs.

    Keys are expected to be strings if `.` notation is used.
    """

    @specification.init
    def ATTRIBUTES(Attributes, **kwargs):
        """
        Create an `Attributes` collection from keyword args.
        """
        attributes = Attributes(a=1, b=2, c=3)
        return attributes

    def getitem(attributes, key):
        """
        Get a value from the set of attributes, either with
        `__getitem__` or `__getattr__` notation.
        """
        assert attributes.a == 1
        assert attributes['b'] == 2

    def contains(attributes, item):
        """
        Check if an attribute key is in the attributes collection.
        """
        assert 'a' in attributes
        assert 'z' not in attributes

    def setitem(attributes, key, value):
        """
        Set a value using either `__setitem__` or `__setattr__`
        notation.
        """
        attributes.d = 4
        attributes['e'] = 5
        assert attributes['d'] == 4
        assert attributes.e == 5

        # Can also overwrite
        attributes.d = 0
        assert attributes.d == 0

    def call(attributes):
        """
        Use `()` notation to get the underlying dictionary
        and access any dictionary function.
        """
        attributes().clear()
        assert 'a' not in attributes
