
from structpy import specxxx
from structpy.system.specification.spec_example import foo_spec


@specxxx.implements(foo_spec)
class Foo:

    def method(self):
        return True

    def test(self):
        return True


if __name__ == '__main__':

    # Verify all specs of implementation
    specxxx.verify(Foo)

    # Verify implementation against a specification
    specxxx.verify(Foo, spec=foo_spec)