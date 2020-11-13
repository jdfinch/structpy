
from structpy import specification


other = None

@specification
class EnforcerHidictSpec:
    """
    Hierarchical dictionary.

    An extension of python `dict` allowing N hierarchically-ordered key types
    to be used to organize and access a set of values. Contains enforcement
    hooks that call functions whenever items are added/overwritten/removed.
    """

    @specification.init
    def ENFORCER_HIDICT(EnforcerHidict, dict_like=None, add_function=None, remove_function=None, order=0):
        """
        Build a hierarchical dictionary.

        `add_function(added)` is a function that is called whenever a new (or replacement)
        key:value pair is added, and it should expect `added` to be a `iterable<tuple<key1, key2, ..., value>>`
        as an argument. The return of `add_function(added)` should be an `iterable<tuple<key1, key2, ..., value>>`,
        which represent the entries that will actually be added to the `enforcer_dict` object.

        `remove_function(removed)` is a function that is called whenever a key:value pair
        is removed  (including those overwritten by new value), and it should expect `removed` to be
        `iterable<tuple<key1, key2, ..., value>>` as an argument. The return of `remove_function(removed)`
        should be an `iterable<tuple<key1, key2, ..., value>>` which represents the entries that will
        actually be removed from the `enforcer_dict` object.
        """
        class EntryCount:
            def __init__(self):
                self.value = 0
            def add_function(self, items):
                items = list(items)
                for _ in items:
                    self.value += 1
                return items
            def remove_function(self, items):
                items = list(items)
                for _ in items:
                    self.value -= 1
                return items

        global other
        other = EntryCount()

        hidict = EnforcerHidict(2,
            {
                'Mary': {
                    'likes': {'lot': 'Bob', 'little': 'Sue'},
                    'dislikes': {'lot': 'Randy'}
                },
                'Bob': {
                    'likes': {'lot': 'Mary'},
                    'dislikes': {'lot': 'Sue', 'medium': 'Joe'}
                }
            },
            add_function=other.add_function,
            remove_function=other.remove_function
        )
        assert other.value == 6
        return hidict

    def getitem(hidict, keys):
        """
        Use `hidict[key1, key2, ...]` to access hidict entries.

        Providing less than `order+1` keys will return a subdictionary object.
        """
        assert hidict['Mary', 'likes', 'lot'] == 'Bob'
        keys = ('Mary', 'likes', 'little')
        assert hidict[keys] == 'Sue'
        assert hidict['Mary', 'dislikes'] == {'lot': 'Randy'}

    def setitem(hidict, keys, value):
        """
        Use `hidict[key1, key2, ...] = value` to reassign or add entries to the hidict.

        `keys` should be a tuple of keys with length `order+1`.
        """
        hidict['Bob', 'likes', 'little'] = 'George'
        assert hidict['Bob', 'likes', 'little'] == 'George'
        hidict['Bob', 'dislikes']['lot'] = 'Sam'
        assert hidict['Bob', 'dislikes', 'lot'] == 'Sam'
        assert other.value == 7

    def delitem(hidict, keys):
        """
        `del hidict[key1, key2, ...]` will delete an entry from hidict.

        If less than `order-1` keys are provided, the specified intermediate dictionary
        will be cleared.
        """
        del hidict['Bob', 'likes', 'little']
        assert 'little' not in hidict['Bob', 'likes']
        del hidict['Bob', 'dislikes']
        assert 'dislikes' not in hidict['Bob']
        assert other.value == 4

    def contains(hidict, keys):
        """
        `(key1, key2, ...) in hidict` will return whether the provided keys are found in
        the hidict.

        Checking the membership of a key sequence of length less than `order+1` is valid.

        Additionally, membership check `(key1, key2, ..., value) in hidict` can be used
        to check for a specific key sequence and value pairing.
        """
        assert 'Mary' in hidict
        assert ('Mary', 'likes', 'lot') in hidict
        assert ('Mary', 'likes') in hidict
        assert ('Marvin', 'likes') not in hidict
        assert ('Mary', 'likes', 'lot', 'Bob') in hidict

    def items(hidict):
        """
        Gets a list of `(key1, key2, ..., keyN, value)` tuple entries in the hidict.

        Length of the tuples is `order+2`.
        """
        items = set(hidict.items())
        assert ('Mary', 'likes', 'lot', 'Bob') in items
        assert ('Mary', 'likes', 'little', 'Sue') in items
        assert ('Bob', 'likes', 'lot', 'Mary') in items
        assert not ('Bob', 'likes', 'little', 'Joe') in items



























