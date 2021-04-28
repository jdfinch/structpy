
from functools import reduce


default = object()


class Map:

    def __init__(self, mapping=default, _reverse=default):
        self._mapping = {}
        if _reverse is not default:
            self.reverse = _reverse
        else:
            self.reverse = Rmap(self)
        if mapping is not default:
            self.map(mapping)

    def __contains__(self, key):
        return key in self._mapping

    def has(self, key=default, value=default):
        if key is default:
            return value in self.values()
        if value is default:
            return key in self._mapping
        return key in self._mapping and value in self._mapping[key]

    def __getitem__(self, key):
        return set(self._mapping[key])

    def get(self, key):
        if key in self:
            return self[key]
        else:
            return set()

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self):
        return len(self._mapping)

    def len_keys(self):
        return len(self._mapping)

    def len_values(self):
        return len(reduce(set.union, self._mapping.values()))

    def len_items(self):
        return len(self.items())

    def keys(self, value=default):
        if value is default:
            return self._mapping.keys()
        else:
            return {key for key in self._mapping if value in self._mapping[key]}

    def values(self, key=default):
        if key is default:
            return reduce(set.union, self._mapping.values())
        else:
            return self._mapping[key]

    def items(self):
        items = set()
        for key, values in self._mapping.items():
            items.update([(key, value) for value in values])
        return items

    def add(self, key, value):
        self._mapping.setdefault(key, set()).add(value)

    def update(self, key, values):
        for value in values:
            self.add(key, value)

    def map(self, mapping):
        for key in mapping:
            self.update(key, mapping[key])

    def remove(self, key=default, value=default):
        if key is not default and value is not default:
            values = self._mapping[key]
            values.remove(value)
            if not values:
                del self._mapping[key]
        elif key is not default:
            del self._mapping[key]
        elif value is not default:
            err = True
            for key, values in self._mapping.items():
                if value in values:
                    values.remove(value)
                    err = False
            if err:
                raise ValueError(f'{value} not in Map {self}')

    def discard(self, key=default, value=default):
        if key is not default:
            if key in self._mapping:
                if value is default:
                    del self._mapping[key]
                else:
                    values = self._mapping[key]
                    values.discard(value)
                    if not values:
                        del self._mapping[key]
        elif value is not default:
            for key, values in self._mapping.items():
                values.discard(value)

    def __delitem__(self, key):
        self.remove(key)

    def pop(self, key=default):
        if key is default:
            key = next(iter(self._mapping))
        value = next(iter(self._mapping[key]))
        self.remove(key, value)
        return key, value


class Rmap:

    def __init__(self, reverse):
        self.reverse = reverse

    def __contains__(self, key):
        return self.reverse.has(value=key)

    def has(self, key=default, value=default):
        return self.reverse.has(value, key)

    def __getitem__(self, key):
        return self.reverse.keys(key)

    def get(self, key):
        return self.reverse.keys(key)

    def __iter__(self):
        return iter(self.reverse.values())

    def __len__(self):
        return len(self.reverse.values())

    def len_keys(self):
        return len(set(self.reverse.values()))

    def len_values(self):
        return len(self.reverse.keys())

    def len_items(self):
        return len(self.reverse.items())

    def keys(self, value=default):
        return set(self.reverse.values(value))

    def values(self, key=default):
        return self.reverse.keys(key)

    def items(self):
        return {(v, k) for k, v in self.reverse.items()}

    def add(self, key, value):
        self.reverse.add(value, key)

    def update(self, key, values):
        for value in values:
            self.reverse.add(value, key)

    def map(self, mapping):
        for key in mapping:
            self.update(key, mapping[key])

    def remove(self, key=default, value=default):
        try:
            self.reverse.remove(value, key)
        except KeyError:
            raise ValueError(f'{value} not found in Map {self}')
        except ValueError:
            raise KeyError(f'{key} not found in Map {self}')

    def discard(self, key=default, value=default):
        self.reverse.discard(value, key)

    def __delitem__(self, key):
        self.remove(key)

    def pop(self, key=default):
        if key is default:
            key = next(iter(self))
        value = next(iter(self[key]))
        self.remove(key, value)
        return key, value



