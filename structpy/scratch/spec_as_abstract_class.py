

from typing import Any, Iterator, Protocol, Type

"""

Need to specify:

* Order of tests
* Method object (for dot notation in docs)
* Test parameters/fixtures
* Method/Function parameters with annotation
* Modification of test parameters
* References to other specs, with test args
* Modularization of spec
* Subtests
* Undocumented/nested tests
* Fields/properties with annotation

Importing the spec module registers an import hook to create Specification objects from Spec inheritors discovered in imported modules.

Spec is a special class that, when inherited, marks a class as a set of specifications for spec testing. (May also define a metaclass in order to prevent instantiation and raise NotImplementedError when inheritors call the Spec's methods).

Callable spec.spec transforms and memoizes a Spec to a Specification object, which is a parameterized set of tests, by parsing and reading data from the AST of the Spec's code (helpful to parameterize test appropriately with global parameters, discover nested functions as subtests, and rewrite assert statements). Specification objects can be iteratively bound to new sets and combinations of test arguments.

Specification objects have a .run method that runs each test defined in the Spec it was generated from (and any tests imported from other Specifications via decoration; see below), in order. Tests are run with access to test parameters (defined as global variables in Spec with the value spec.param, as well as two special variables representing a class and instance). Assigning local variables within a test (at top-level, no walrus-ing) with the same names as global variables with value spec.param will create a fixturization of the parameter with respect to that test. Future tests in the sequence that reference a fixturized parameter will re-run the tests that created the fixturization, with recursion, to reconstruct fixturized parameters to the original state defined by the fixturization. 

Using spec.param as a decorator of a function will create a fixturized parameter with the name of the decorated function. The test chain that references the function name as a test parameter will call the function to reconstruct the parameter value in each test that references it. 

Specification objects can be looked up by their original Spec definitions using spec.spec[MySpec]. Similarly, creating new specs as slices, combinations, etc. of existing specs can be done like spec.spec[SpecOne.method_a, SpecTwo.method_b:SpecTwo.method_c, SpecThree.method_d].

Specification objects can decorate methods to "copy-paste" their tests after the decorated method in a new Spec definition. The decorated method is treated as setup for the copied tests, where locals is checked after running setup to assign parameters to the copied tests. In general, doing this should be accompanied by defining the source Spec as a superclass of the target Spec, so type hints and checking are still set up correctly, but it is not strictly required.

Class spec.Test holds a collection of Specification objects (test arguments are managed by each Specification object, but can be bound in batch by the Test). It has a .run method to run tests across all Specifications.

Function spec.implements/spec.imps matches a Spec with an implementation argument (to be assigned with the parameter represented by the Spec name). The Spec passed to spec.implements can either be an existing Specification object, or a raw Spec class. The implementation object matched to the Specification will add the specification to a special __specification__ attribute. Function spec.implements can be used as a decorator and returns the implementation.

Function spec.run creates and runs Test objects. It can be passed Specification objects, implementations that have a valid __specification__ attribute defining their specifications, or entire packages/modules, in which case the package is recursively searched for module-level Specifications and implementations.
"""


def spec(f):
    class Spec:
        def run_tests(self):
            pass
        spec = f
    result = Spec()
    result.spec = f
    return result

def nothing(f):
    return None


############# spec file #############

class Foo(Protocol):

    def bar(thing, x: str) -> list:
        y = thing.bar
        other = y('hello')

        def subtest():
            """ Treated as yet another test, but passed locals of bar (AFTER any REGENERATIONS)"""
            assert other.reverse()

        return ...


############# imp  file #############


class MyFooImp:

    def __init__(self):
        pass

    def bar(self, x: str):
        return ['hello', 'there']


blah: Foo = MyFooImp()


############# obj  test #############

"""
To make a spec of just an object, just use the object var name instead of "self".
"""


class MyObject(Protocol):

    def do_something(MyObject, x, y):
        assert MyObject.do_something('hello', 'world')



#############  static   #############

"""
Class methods can use @classmethod with class as first arg.

Raw references to `MyStaticClass` will still treat it as a Spec.
"""

class MyStaticCls(Protocol):

    @classmethod
    def do_something_static(MyStaticCls, x):
        assert MyStaticCls.do_something_static(4)



#############   refer   #############

class Bar(Foo, Protocol):


    def bat(self) -> None: ...


def setup_1():
    ...


class BarImp:

    def bar(self, x):
        return []

    def bat(self): ...

bar: Bar = BarImp()



