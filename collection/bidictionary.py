
class Bidictionary(dict):

    def __init__(self, kwargs=None):
        if kwargs is None:
            dict.__init__(self)
        else:
            dict.__init__(self, kwargs)
        self.reverse = {}

    def __getitem__(self, item):
        return dict.__getitem__(self, item)

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.reverse[value] = key
