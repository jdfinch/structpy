
from structpy import specification


@specification
class HidictSpec:
    """
    Hierarchical dictionary.

    For an order-N hidict, N+1 ordered keys are mapped to a value in each
    hidict entry.

    Hidict supports access patterns where only part of the key sequence
    is specified, allowing flexibility in lookup patterns where multiple
    keys are associated with a value.
    """

    @specification.init
    def HIDICT_SPEC(Hidict, order, dict_like=None):
        """
        Create a hierarchical dictionary from the dictionary structure
        passed in to `other`.

        `order` represents the number of intermediate keys to look up a
        value, e.g. an order-2 `Hidict` would have items of the form
        `(key1, key2, key3, value)`. An order-0 Hidict is equivalent to
        a python `dict`.
        """
        hidict = Hidict(2, {
            'Mary': {
                'likes': {'lot': 'Bob', 'little': 'Sue'},
                'dislikes': {'lot': 'Randy'}
            },
            'Bob': {
                'likes': {'lot': 'Mary'},
                'dislikes': {'lot': 'Sue', 'medium': 'Joe'}
            }
        })
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
        hidict['Bob', 'dislikes', 'lot'] = 'Sam'
        assert hidict['Bob', 'dislikes', 'lot'] == 'Sam'

        # Can assign a partial key sequence to a dict-like to add/update a subdict
        hidict['Bob', 'loves'] = {'medium': 'George', 'lot': 'Phil'}
        assert hidict['Bob', 'loves', 'medium'] == 'George'

    def delitem(hidict, keys):
        """
        `del hidict[key1, key2, ...]` will delete an entry from hidict.

        If less than `order-1` keys are provided, the specified intermediate dictionary
        will be cleared.
        """
        del hidict['Bob', 'likes', 'little']
        assert ('Bob', 'likes', 'little') not in hidict
        del hidict['Bob', 'dislikes']
        assert ('Bob', 'dislikes') not in hidict
        del hidict['Bob', 'loves']
        assert ('Bob', 'loves') not in hidict

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
        items = list(hidict.items())
        assert ('Mary', 'likes', 'lot', 'Bob') in items
        assert ('Mary', 'likes', 'little', 'Sue') in items
        assert ('Bob', 'likes', 'lot', 'Mary') in items
        assert not ('Bob', 'likes', 'little', 'Joe') in items
