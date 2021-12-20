
from structpy.system.specification import spec
from structpy.system.specification.spec_example import foo_spec


@spec.imp(foo_spec)
class Foo(list):

    def method(self):
        return True

    def test(self):
        return True


if __name__ == '__main__':

    # Verify all specs of implementation
    spec.verify(foo_spec)