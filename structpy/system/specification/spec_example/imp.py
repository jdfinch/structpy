
from structpy import spec
from structpy.system.specification.spec_example import spec as my_spec

@spec.implements(my_spec)
class Implementation:

    def method(self):
        return True

    def test(self):
        return True

if __name__ == '__main__':
    spec.verify(Implementation)