
from structpy.spec import Spec, detail, expecting
from structpy.typing import *

from typing import TypeVar

from structpy.spec.map.hierarchical_map import Map as HierarchicalMap


T_get_default = TypeVar('T_get_default', bound=Hashable)


class Map(HierarchicalMap, Spec):
    """
    Many-to-many mapping between domain and codomain.

    The domain and codomain are each sets of `Hashable` elements in the `Map`. Each element in the domain can be associated to a set of 0 or more elements in the codomain.

    The mapping allows easy access to the set of codomain elements associated with an element in the domain. Additionally, the `Map` is reversible, allowing access of domain elements associated with a codomain element.
    """

    def __init__(
            map,
            mapping: Mapping[Hashable | list[Hashable], Iterable[Hashable]]
                     | Iterable[Hashable] | Iterable[list[Hashable]] = None,
            values: Iterable[Hashable] = None,
            items: Iterable[Iterable[Hashable]] = None
    ):
        """
        Constructor.

        :param mapping:
        :param values:
        :param items:
        """
        map = Map({
            'Mark': {'Geography', 'Algebra'},
            'Sally': {'Geography'}
        })

        with detail("`Map` objects can be constructed from an iterable of items representing element associations."):
            assert map == Map(items=[
                ('Mark', 'Geography'),
                ('Mark', 'Algebra'),
                ('Sally', 'Geography'),
                ('Sally', 'Programming')
            ])

        with detail("Copy a `Map` using the `Map` constructor."):
            copy = Map(map)
            assert map == copy
            assert map is not copy
            assert map['Mark'] == copy['Mark']
            assert map['Mark'] is not copy['Mark']
            assert next(iter(map['Sally'])) is next(iter(map['Sally']))

        with detail("`Map` can be constructed by defining key and value sets without associations."):
            m = Map(
                ['Mark', 'Sally'],
                ['Chamber', 'Prisoner', 'Infinity', 'Chronicle']
            )
            assert m.keys() == {'Mark', 'Sally'}
            assert m.values() == {'Geography', 'Algebra'}
            assert m.items() == []

    def __eq__(map, other: Any) -> bool:
        """
        A `Map` object `map` is equal to an `Iterable` `other` when:

        1. The domain set of `map` is equal to the set created by iterating over `other`.
        2. For each domain element `e` in `map`, the set of corresponding codomain elements is equal to the set created by iterating over `other[e]`.

        :param other: An object to compare to `Map`.
        :return: Whether the mapping in `map` is equivalent to that defined by the iteration and subscripting of `other`.
        """
        assert map == {
            'Mark': ['Geography', 'Algebra'],
            'Sally': ['Geography']
        }
        return ...

    def __getitem__(map, key: Hashable | list[Hashable]) -> set:
        """
        Get the set of codomain elements associated with `key`.

        :param key: An element in the `map` domain.
        :return: Values in the codomain associated with `key`.
        """
        assert map['Mark'] == {'Geography', 'Algebra'}
        assert map['Sally'] == {'Geography'}

        with detail("Calling `map[key]` where `key not in map` raises `KeyError`."):
            with expecting(KeyError):
                values = map['Tom']

        with detail("Return value of `map[x]` is not a reference to the underlying codomain set."):
            map['Sally'].add('History')
            assert map['Sally'] == {'Geography'}
        return ...

    def __contains__(map, key: Any) -> bool:
        """
        Check if the `map` contains a domain element.

        :param key:
        :return: Whether `key` is an element in the `map` domain.
        """
        assert 'Mark' in map
        assert 'Tom' not in map

        with detail("Any object can be checked for `in map` without error"):
            assert {} not in map
        return ...

    def __len__(map) -> int:
        """
        Get the number of elements in the `map` domain.

        Note that the number of elements in the `map` codomain can be found with `len(map.reverse)` or `len(map.values)`.

        :return: Non-negative number of domain elements.
        """
        assert len(map) == 2
        return ...

    def __iter__(map) -> Iterator:
        """
        The elements of a `Map` domain can be iterated over.

        :return: Iterator over keys of `map`.
        """
        keys = set()
        for key in map:
            keys.add(key)
        assert keys == {'Mark', 'Sally'}
        return ...

    def keys(map, up_to: int =None) -> set:
        """
        :return: A read-only view of the `Map` domain.
        """
        assert map.keys() == {'Mark', 'Sally'}
        return ...

    def values(map) -> set:
        """
        :return: View of values in `map` codomain.
        """
        assert map.values() == {'Geography', 'Algebra'}
        return ...

    def items(map) -> set[tuple[Any, Any]] | list[tuple[list, Any]]:
        """
        :return: View of (key, value) pairs in `map`.
        """
        assert map.items() == {
            ('Mark', 'Geography'),
            ('Mark', 'Algebra'),
            ('Sally', 'Geography')
        }
        return ...

    def get(map, key: Hashable, default: T_get_default = None) -> set | T_get_default:
        """
        Access values by key without `KeyError`.

        :return: Values associated with `key`, or `default` if `key not in map`.
        """
        assert map.get('Mark') == {'Geography', 'Algebra'}
        assert map.get('John') == set()
        default = object()
        assert map.get('John', default) is default
        return ...

    @property
    def reverse(map) -> 'Map':
        """
        :return: View of `map` with domain and codomain inverted.
        """
        assert map.reverse == {
            'Geography': {'Mark', 'Sally'},
            'Algebra': {'Mark'}
        }

        with detail("Any mutations to `map.reverse` will be reflected in `map` and vice versa."):
            map.reverse['Geography'].add('Joe')
            assert map.reverse == {
                'Geography': {'Mark', 'Sally', 'Joe'},
                'Algebra': {'Mark'}
            }
            assert map == {
                'Mark': {'Geography', 'Algebra'},
                'Sally': {'Geography'},
                'Joe': {'Geography'}
            }
        return ...

    r = reverse

    def issubset(map, other):
        ...
    __le__ = issubset

    def ispropersubset(map, other):
        ...
    __lt__ = ispropersubset

    def issuperset(map, other):
        ...
    __ge__ = issuperset

    def ispropersuperset(map, other):
        ...
    __gt__ = ispropersuperset

    def isdisjoint(map, other):
        ...

    def __setitem__(map, key: Hashable, values: Iterable[Hashable]):
        """
        Assign values from iterable `values` to `key`, replacing any existing values associated with `key`.

        If `key not in map`, add `key` to map keys.

        :param key: Key to add to `map` domain.
        :param values: Values to associate with `key` in the `map` codomain.
        """
        map['John'] = {'Calculus', 'English'}
        assert map['John'] == {'Calculus', 'English'}
        map['Mark'] = {'Humanities', 'Calculus'}
        assert map['Mark'] == {'Humanities', 'Calculus'}

        with detail("`Map` value sets are stable, not reconstructed."):
            marks_values = map['Mark']
            map['Mark'] = {'Programming'}
            assert map['Mark'] is marks_values
            assert marks_values == {'Programming'}

        with detail("`Map`s use their own `set` to represent `values`, rather than taking a provided `values` collection by reference."):
            values = {'Calculus', 'English'}
            map['John'] = values
            assert map['John'] == values
            assert map['John'] is not values

    def add(map, key, values=None):
        """
        Add a key and/or values to the `Map`.

        Similar to `map.setdefault(key, values)`, but `add` will add `values` to the set of existing values associated with `key`, and will never replace existing values.

        :param key: Key to add to `map` domain.
        :param values: Values to associate with `key`.
        :return: `set` of values associated with `key`.
        """
        assert map.add('John') == set()
        assert map['John'] == set()
        assert map.add('John', {'Algebra', 'Statistics'}) == set()
        assert map['John'] == set()
        assert map.add('Jake', {'Algebra'}) == {'Algebra'}
        assert map['Jake'] == {'Algebra'}

    def setdefault(map, key: Hashable, values: Iterable[Hashable] =None) -> set:
        """
        Get the values associated with `key` in `map`, adding `key` associated with `values` if `key not in map`.

        Similar to `map.add(key, values)`, but `setdefault` will replace values associated with `key` if `key` already exists in `map`'s domain.

        :param key: Key in `map` domain.
        :param values: Values to associate with `key` in the `map` codomain if `key not in map`.
        :return: `set` of values associated with `key`.
        """
        assert map.setdefault('John') == set()
        assert map['John'] == set()
        assert map.setdefault('John', {'Algebra', 'Statistics'}) == set()
        assert map['John'] == set()
        assert map.setdefault('Jake', ['Algebra']) == {'Algebra'}
        assert map['Jake'] == {'Algebra'}
        return ...

    def __delitem__(map, key):
        """
        Remove `key` from `map` domain.

        @param key: to remove from `map` domain.
        """
        # Should values be auto-removed when deleting keys?

    delete = __delitem__

    def remove(map, key, value=None): ...

    def discard(map, key, value=None): ...

    def pop(map, key, default=None): ...

    def popitem(map, key=None):
        ...

    def clear(map):
        ...

    def union_update(map, other): ...
    __ior__ = union_update

    def intersection_update(map, other): ...
    __iand__ = intersection_update

    def difference_update(map, other): ...
    __isub__ = difference_update

    def symmetric_difference_update(map, other): ...
    __ixor__ = symmetric_difference_update

    def union(map, other): ...
    __or__ = union

    def intersection(map, other): ...
    __and__ = intersection

    def difference(map, other): ...
    __sub__ = difference

    def symmetric_difference(map, other): ...
    __xor__ = symmetric_difference

    @Spec[HierarchicalMap]
    def __init__(self):
        """
        `Map` should satisfy the hierarchical `Map` spec.
        """

