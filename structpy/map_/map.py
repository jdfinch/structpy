

default = object()


class Map:

    def __init__(self, mapping):
        self._mapping = {}



    def add(self, *chain):
        assert len(chain) > 1
        d = self._mapping
        for key in chain[:-2]:
            d = d.setdefault(key, {})
        s = d.setdefault(chain[-2], set())
        s.add(chain[-1])

    def add_item(self, key, value, *keys):
        pass

    def map(self, keys, values):
        if type(keys) is not list:
            keys = [keys]
