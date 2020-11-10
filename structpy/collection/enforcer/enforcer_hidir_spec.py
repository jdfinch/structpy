
from structpy import specification


other = None

@specification
class EnforcerHidirSpec:
    """
    Hierarchical directory.

    An extension of python `dict` allowing N hierarchically-ordered key types
    to be used to organize and access a set of values. Contains enforcement
    hooks that call functions whenever items are added/overwritten/removed.
    """

    @specification.init
    def ENFORCER_HIDIR(EnforcerHidir, dict_like=None, add_function=None, remove_function=None, order=0):
        """
        Build a hierarchical directory.

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

        hidir = EnforcerHidir(2,
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
        return hidir

    def getitem(hidir, keys):
        """
        Use `hidir[key1, key2, ...]` to access hidir entries.

        Providing less than `order+1` keys will return a subdirectory object.
        """
        assert hidir['Mary', 'likes', 'lot'] == 'Bob'
        keys = ('Mary', 'likes', 'little')
        assert hidir[keys] == 'Sue'
        assert hidir['Mary', 'dislikes'] == {'lot': 'Randy'}

    def setitem(hidir, keys, value):
        """
        Use `hidir[key1, key2, ...] = value` to reassign or add entries to the hidir.

        `keys` should be a tuple of keys with length `order+1`.
        """
        hidir['Bob', 'likes', 'little'] = 'George'
        assert hidir['Bob', 'likes', 'little'] == 'George'
        hidir['Bob', 'dislikes']['lot'] = 'Sam'
        assert hidir['Bob', 'dislikes', 'lot'] == 'Sam'
        assert other.value == 7

    def delitem(hidir, keys):
        """
        `del hidir[key1, key2, ...]` will delete an entry from hidir.

        If less than `order-1` keys are provided, the specified intermediate directory
        will be cleared.
        """
        del hidir['Bob', 'likes', 'little']
        assert 'little' not in hidir['Bob', 'likes']
        del hidir['Bob', 'dislikes']
        assert 'dislikes' not in hidir['Bob']
        assert other.value == 4

    def contains(hidir, keys):
        """
        `(key1, key2, ...) in hidir` will return whether the provided keys are found in
        the hidir.

        Checking the membership of a key sequence of length less than `order+1` is valid.

        Additionally, membership check `(key1, key2, ..., value) in hidir` can be used
        to check for a specific key sequence and value pairing.
        """
        assert 'Mary' in hidir
        assert ('Mary', 'likes', 'lot') in hidir
        assert ('Mary', 'likes') in hidir
        assert ('Marvin', 'likes') not in hidir
        assert ('Mary', 'likes', 'lot', 'Bob') in hidir

    def items(hidir):
        """
        Gets a list of `(key1, key2, ..., keyN, value)` tuple entries in the hidir.

        Length of the tuples is `order+2`.
        """
        items = set(hidir.items())
        assert ('Mary', 'likes', 'lot', 'Bob') in items
        assert ('Mary', 'likes', 'little', 'Sue') in items
        assert ('Bob', 'likes', 'lot', 'Mary') in items
        assert not ('Bob', 'likes', 'little', 'Joe') in items



























