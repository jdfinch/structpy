from structpy import implementation
from structpy.collection.attributes_spec import AttributesSpec

@implementation(AttributesSpec)
class Attributes:

    def __init__(self, **kwargs):
        self.__dict__.update(__dictionary__=kwargs, __specification__=None)

    def __getitem__(self, item):
        return self.__dictionary__.__getitem__(item)

    def __setitem__(self, key, value):
        return self.__dictionary__.__setitem__(key, value)

    def __getattr__(self, item):
        return self.__dictionary__[item]

    def __setattr__(self, key, value):
        return self.__dictionary__.__setitem__(key, value)

    def __call__(self):
        return self.__dictionary__

    def __contains__(self, item):
        return item in self.__dictionary__

    def __str__(self):
        return 'Attributes({})'.format(self.__dictionary__)

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    print(AttributesSpec.verify(Attributes))