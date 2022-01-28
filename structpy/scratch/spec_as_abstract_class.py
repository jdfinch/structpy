

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


Decorator @spec returns a Spec object, where the Spec class has a metaclass that alters inheritance to function like an ABC.

Protocol structural static type checking seems to fall through the decorator, so the class decorated with @spec should still be usable as a Protocol for type annotation.
"""


def spec(f):
    class Spec:
        def run_tests(self):
            pass
    return Spec()


############# spec file #############

thing: ...
other: ...


@spec
class Foo(Protocol):

    def bar(thing, x: str) -> list:
        y = thing.hello
        other = y.get_other()
        return ...


############# imp  file #############


class MyFooImp:

    def bar(self, x: str):
        return ['hello', 'there']


blah: Foo = MyFooImp()


############# obj  test #############

"""
To make a spec of just an object, just use the object var name instead of "self".
"""


@spec
class MyObject(Protocol):

    def do_something(MyObject, x, y):
        assert MyObject.do_something('hello', 'world')



#############  static   #############

"""
Class methods can use @classmethod with class as first arg.

Raw references to `MyStaticClass` will still treat it as a Spec.
"""


@spec
class MyStaticCls(Protocol):

    @classmethod
    def do_something_static(MyStaticCls, x):
        assert MyStaticCls.do_something_static(4)


MyStaticCls.run_tests()

