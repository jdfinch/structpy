
from structpy import specification


@specification
class HidirSpec:
    """
    Hierarchical directory.

    For an order-N hidir, N+1 ordered keys are mapped to a set of values
    in each hidir entry.

    Hidir supports access patterns where only part of the key sequence
    is specified, allowing flexibility in lookup patterns where multiple
    keys are associated with a value set.
    """

    @specification.init
    def HIDIR_SPEC(Hidir, order, dict_like=None):
        """
        Create a hierarchical directory from the directory structure
        passed in to `other`.

        `order` represents the number of intermediate keys to look up a
        value set, e.g. an order-2 `Hidir` would have items of the form
        `(key1, key2, key3, values)`. An order-0 Hidir is similar to
        a python `dict` with `set`s as values.
        """
        hidir = Hidir(2, {
            'Mary': {
                'likes': {
                    'lot': {'Bob', 'Joe'},
                    'little': {'Sue'}
                },
                'dislikes': {
                    'lot': {'Randy', 'Phil'}
                }
            },
            'Bob': {
                'likes': {
                    'lot': {'Mary'}
                },
                'dislikes': {
                    'lot': {'Sue'},
                    'medium': {'Joe'}
                }
            }
        })
        return hidir

    def getitem(hidir, keys):
        """
        Use `hidir[key1, key2, ...]` to access hidir entries.

        Providing less than `order+1` keys will return a subdictionary object.
        """
        assert hidir['Mary', 'likes', 'lot'] == {'Bob', 'Joe'}
        keys = ('Mary', 'likes', 'little')
        assert hidir[keys] == {'Sue'}
        assert hidir['Mary', 'dislikes'] == {'lot': {'Randy', 'Phil'}}

    def setitem(hidir, keys, value):
        """
        Use `hidir[key1, key2, ...] = values` to reassign or add entries to the hidir.

        `keys` should be a tuple of keys with length `order+1`.
        """
        hidir['Bob', 'likes', 'little'] = ['George']
        assert hidir['Bob', 'likes', 'little'] == {'George'}
        hidir['Bob', 'dislikes', 'lot'] = ['Sam', 'Phil']
        assert hidir['Bob', 'dislikes', 'lot'] == {'Sam', 'Phil'}

        # can also add items to a Hidir value set
        hidir['Mary', 'likes', 'lot'].add('Rick')
        assert hidir['Mary', 'likes', 'lot'] == {'Bob', 'Joe', 'Rick'}

    def delitem(hidir, keys):
        """
        `del hidir[key1, key2, ...]` will delete an entry from hidir.

        If less than `order-1` keys are provided, the specified intermediate dictionary
        will be cleared.
        """
        del hidir['Bob', 'likes', 'little']
        assert ('Bob', 'likes', 'little') not in hidir
        del hidir['Bob', 'dislikes']
        assert ('Bob', 'dislikes') not in hidir

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
        assert ('Mary', 'likes', 'lot', 'Rick') in hidir

    def items(hidir):
        """
        Gets a list of `(key1, key2, ..., keyN, value)` tuple entries in the hidir.

        Length of the tuples is `order+2`.
        """
        items = list(hidir.items())
        assert ('Mary', 'likes', 'lot', 'Bob') in items
        assert ('Mary', 'likes', 'lot', 'Rick') in items
        assert ('Mary', 'likes', 'little', 'Sue') in items
        assert ('Bob', 'likes', 'lot', 'Mary') in items
        assert ('Bob', 'likes', 'lot', 'Rick') not in items
