
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

        `add_function(added)` is a function that is called whenever a new
        key:value pair is added, and it should expect `added` to be a `iterable<tuple<key, value>>`
        as an argument.

        `remove_function(removed)` is a function that is called whenever a key:value pair
        is removed  (including those overwritten by new value), and it should expect `removed` to be
        `iterable<tuple<key:value>>` as an argument.
        """
        class LetterCount:
            def __init__(self):
                self.value = 0
            def add_function(self, items):
                for _, value in items:
                    self.value += len(value)
            def remove_function(self, items):
                for _, value in items:
                    self.value -= len(value)

        global other
        other = LetterCount()

        hidict = EnforcerHidict(
            {
                'duck': {'has': 'bill', 'is': 'bird'},
                'robin': {'has': 'wings', 'is': 'bird'},
                'plane': {'has': 'wings', 'is': 'vehicle'}
            },
            add_function=other.add_function,
            remove_function=other.remove_function,
            order=1
        )
        return hidict

    def add(hidict, key, value):
        hidict['duck', 'sound'] = 'quack'
        assert hidict['duck', 'sound'] == 'quack'
        assert hidict['duck'] == {'has': 'bill', 'is': 'bird', 'sound': 'quack'}
        assert other.value == 34

        hidict.update({
            'robin': {'sound': 'chirp', 'color': 'red'},
            'eagle': {'quality': 'magnificent'}
        })
        assert hidict['eagle']['quality'] == 'magnificent'
        assert 'sound' in hidict['robin']

    def remove(hidict, key, value):
        del hidict['robin']
        del hidict['eagle']
        assert 'robin' not in hidict
        assert 'eagle' not in hidict
        assert other.value == 25

        hidict['duck', 'has'] == 'webbing'
        assert hidict['duck', 'has'] == 'webbing'
        other.value == 28

        hidict['duck'].clear()
        assert other.value == 12
        assert 'duck' in hidict
        assert 'has' not in hidict['duck']

        hidict.clear()
        assert other.value == 0
        assert len(hidict) == 0



























