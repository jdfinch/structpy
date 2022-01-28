
from copy import deepcopy

def test_deepcopy_class():

    class Foo:
        l = []

    f = Foo()

    fc = deepcopy(f)

    FooCopy = deepcopy(Foo)

    print(f is fc)              # False
    print(Foo is FooCopy)       # True
    print(Foo.l is FooCopy.l)   # True


def copy_by_dynamic_type_creation():

    class Foo:
        l = []

    FooCopy = type('FooCopy', deepcopy(Foo.__bases__), deepcopy(Foo.__dict__))
    """
    Traceback (most recent call last):
      File "/home/james/Structpy/structpy/structpy/scratch/copy_tests.py", line 31, in <module>
        test_copy_class()
      File "/home/james/Structpy/structpy/structpy/scratch/copy_tests.py", line 25, in test_copy_class
        FooCopy = type('FooCopy', deepcopy(Foo.__bases__), deepcopy(Foo.__dict__))
      File "/home/james/anaconda3/envs/Structpy/lib/python3.7/copy.py", line 169, in deepcopy
        rv = reductor(4)
    TypeError: can't pickle mappingproxy objects
    """

    print(Foo is FooCopy)
    print(Foo.l is FooCopy.l)


def copy_by_inheritance():

    class Foo:
        l = []

    class FooCopy:
        pass

    print(Foo is FooCopy)
    print(Foo.l is FooCopy.l)
    """
    Traceback (most recent call last):
      File "/home/james/Structpy/structpy/structpy/scratch/copy_tests.py", line 53, in <module>
        copy_by_inheritance()
      File "/home/james/Structpy/structpy/structpy/scratch/copy_tests.py", line 50, in copy_by_inheritance
        print(Foo.l is FooCopy.l)
    AttributeError: type object 'FooCopy' has no attribute 'l'
    """


copy_by_inheritance()