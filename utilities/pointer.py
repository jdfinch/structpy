
class PointerBase:
    def __init__(self, v):
        self.v = v

class Pointer(PointerBase):

    def __init__(self, v=None):
        PointerBase.__init__(self, v)

    def __imul__(self, v):
        PointerBase.__setattr__(self, 'v', v)
        return self

    def __getattribute__(self, item):
        return PointerBase.__getattribute__(self, 'v').__getattribute__(item)

    def __call__(self):
        return PointerBase.__getattribute__(self, 'v')

    def __pos__(self):
        return PointerBase.__getattribute__(self, 'v')