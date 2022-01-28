"""
Mapping.
"""

from structpy.spec import *
from structpy.typing import *


@Spec
class Map(Protocol):
    """
    Mapping between domain and codomain.
    """

    def __init__(
            map,
            mapping: Mapping[Hashable, Hashable] | Iterable[tuple[Hashable, Hashable]] = None
    ):
        """
        Constructor for `Map`.

        :param mapping: mapping between domain and codomain elements.
        """

        map = Map([
            ('Mark', 'Geography'),
            ('Mark', 'Algebra'),
            ('Sally', 'Geography'),
            ('Sally', 'Programming')
        ])

    def __from_dict(map):
        """
        `Map` objects can be constructed from a dict-of-sets object.
        """
        assert map == Map({
            'Mark': {'Geography', 'Algebra'},
            'Sally': {'Geography'}
        })

    def __copy_constructor(map):
        """
        Copy a `Map` using the `Map` constructor.
        """
        other = Map([
            ('Mark', 'Geography'),
            ('Mark', 'Algebra'),
            ('Sally', 'Geography'),
            ('Sally', 'Programming')
        ])
        map = Map(other)
        assert map == other
        assert map is not other

    def __getitem__(map, key) -> set:
        """
        Get a set of codomain elements associated with `key`.
        @param key: An element in the `map` domain.
        @return: `set<value>`
        """
        assert map['Mark'] == {'Geography', 'Algebra'}
        assert map['Sally'] == {'Geography'}

    def __getitem_returns_reference(map):
        """
        Result of a `__getitem__` call, `map[x]`, is a reference to the associated codomain set.
        """
        map['Sally'].add('History')
        assert map['Sally'] == {'Geography', 'History'}

    def __getitem_bad_key_raises_keyerror(map):
        """
        Calling `map[key]` where `key not in map` raises `KeyError`.
        """
        with expecting(KeyError):
            v = map['John']

    def __contains__(map, key):
        """
        @param domain_element:
        @return: `bool` whether `key` is an element in the `map` domain.
        """
        assert 'Mark' in map
        assert 'John' not in map

    def __len__(map):
        """
        @return: Number of elements in the `map` domain.
        """
        assert len(map) == 2

    def __iter__(map):
        """
        @return: Iterator over keys of `map`.
        """
        keys = set()
        for key in map:
            keys.add(key)
        assert keys == {'Mark', 'Sally'}

    def keys(map):
        """
        @return: View keys in `map` domain.
        """
        assert map.keys() == {'Mark', 'Sally'}

    def values(map):
        """
        @return: View of values in `map` codomain.
        """
        assert map.values() == {'Geography', 'Algebra'}

    def items(map):
        """
        @return: View of (key, value) pairs in `map`.
        """
        assert set(map.items()) == {
            ('Mark', 'Geography'),
            ('Mark', 'Algebra'),
            ('Sally', 'Geography')
        }

    @property
    def reverse(map):
        """
        @return: View of `map` with domain and codomain inverted.
        """
        assert map.reverse == {
            'Geography': {'Mark', 'Sally'},
            'Algebra': {'Mark'}
        }

    def __reverse_returns_reference(map):
        """
        `map.reverse` is a view of `map` with domain and codomain inverted.

        Any mutations to `map.reverse` will be reflected in `map` and vice versa.
        """
        return Map({
            'Geography': {'Mark', 'Sally'},
            'Algebra': {'Mark'}
        }).reverse

    def __r_alias(map):
        """
        `map.r` is an alias for `map.reverse`
        """
        assert map.r is map.reverse

    def get(map, key, default=None):
        """
        @return: Value associated with `key`, or `default` if `key not in map`.
        """
        assert map.get('Mark') == {'Geography', 'Algebra'}
        assert map.get('John') is None
        dflt = object()
        assert map.get('John', dflt) is dflt

    def __setitem__(map, key, values):
        """
        Assign values from iterable `values` to `key`.

        If `key not in map`, add `key` to map keys.

        @param key: to add to `map` domain.
        @param values: `iterable<value>` to associate with `key` in the `map` codomain.
        """
        map['John'] = {'Calculus', 'English'}
        assert map['John'] == {'Calculus', 'English'}

    def __setitem_overwrites_values(map):
        """
        `map[key] = values` overwrites existing values associated with `key`, replacing them with the items in provided `values`.
        """
        map['Mark'] = {'Geography', 'Calculus'}
        assert map['Mark'] == {'Geography', 'Calculus'}

    def __setitem_copies_values(map):
        """
        `map[key] = values` will add each item in `values` into the map codomain, not add the entire collection `values` by reference.
        """
        values = {'Calculus', 'English'}
        map['John'] = values
        assert map['John'] == values
        assert map['John'] is not values

    def setdefault(map, key, values=None):
        """
        Get the values associated with `key` in `map`, adding `key` associated with `values` if `key not in map`.

        @param key: in `map` domain.
        @param values: `iterable<value>` to associate with `key` in the `map` codomain if `key not in map`.
        @return: `set<value>` a0ssociated with `key`.
        """
        assert map.setdefault('John') == set()
        assert map['John'] == set()
        assert map.setdefault('John', {'Algebra', 'Statistics'}) == set()
        assert map['John'] == set()
        assert map.setdefault('Jake', {'Algebra'}) == {'Algebra'}
        assert map['Jake'] == {'Algebra'}

    def add(map, key, values=None):
        """
        Alias for `setdefault(key, values=None)`.

        @param key: in `map` domain.
        @param values: `iterable<value>` to associate with `key` in the `map` codomain if `key not in map`.
        @return: `set<value>` associated with `key`.
        """
        assert map.add('John') == set()
        assert map['John'] == set()
        assert map.add('John', {'Algebra', 'Statistics'}) == set()
        assert map['John'] == set()
        assert map.add('Jake', {'Algebra'}) == {'Algebra'}
        assert map['Jake'] == {'Algebra'}

    def __delitem__(map, key):
        """
        Remove `key` from `map` domain.

        @param key: to remove from `map` domain.
        """
        # Should values be auto-removed when deleting keys?
