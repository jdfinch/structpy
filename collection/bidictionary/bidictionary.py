
class Bidictionary(dict):

    def __init__(self, other=None):
        if other is not None:
            dict.__init__(self, other)
        else:
            dict.__init__(self)
        self._reverse = {}

    def reverse(self):
        return self._reverse

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self._reverse.__setitem__(value, key)

    def __delitem__(self, key):
        self._reverse.__delitem__(self[key])
        dict.__delitem__(self, key)

