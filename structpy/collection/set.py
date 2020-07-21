
from structpy import implementation
from structpy.collection.set_spec import SetSpec


@implementation(SetSpec)
class Set(set):
    """
    Simple implementation of FiniteSet by overriding python Set `__hash__` and `__eq__`
    """

    def __eq__(self, other):
        return set.__eq__(self, other)

    def __hash__(self):
        return hash(frozenset(self))

if __name__ == '__main__':
    print(SetSpec.verify(Set))