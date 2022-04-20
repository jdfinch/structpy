
from structpy.spec import Spec, detail, expecting
from structpy.typing import *

from typing import TypeVar, Generic, Type


DefaultType = TypeVar('DefaultType')
KeyChain = TypeVar('KeyChain', bound=tuple)
Element = Hashable | list[Hashable]
Elements = Iterable[Element]


class Map(Generic[KeyChain], Spec):
    """
    Hierarchical mapping.
    """

    KeyChain: Type[KeyChain] = type('KeyChain', (tuple,), {})

    def __init__(
            map,
            mapping: Mapping[Element, Elements] | Elements = None,
            values: Elements = None,
            items: Iterable[tuple[Element, Element]] = None
    ):
        """
        Constructor.

        :param mapping:
        :param values:
        :param items:
        """
        map = Map({
            'John': {
                'Harry Potter': {'Chamber', 'Prisoner'},
                'Marvel': {'Infinity'}
            },
            'Sally': {'Chronicle'}
        })

        with detail("`Map` objects can be constructed from an iterable of items representing element associations."):
            assert map == Map(items=[
                (['John', 'Harry Potter'], 'Chamber'),
                (['John', 'Harry Potter'], 'Prisoner'),
                (['John', 'Marvel'], 'Infinity'),
                ('Sally', 'Chronicle')
            ])

        with detail("Copy a `Map` using the `Map` constructor."):
            copy = Map(map)
            assert map == copy
            assert map is not copy
            assert map[['John', 'Harry Potter']] == copy[['John', 'Harry Potter']]
            assert map[['John', 'Harry Potter']] is not copy[['John', 'Harry Potter']]

        with detail("`Map` can be constructed by defining key and value sets without associations."):
            m = Map(
                [('John', 'Harry Potter'), ('John', 'Marvel'), ('Sally',)],
                ['Chamber', 'Prisoner', 'Infinity', 'Chronicle']
            )
            assert m.keys() == {('John', 'Harry Potter'), ('John', 'Marvel'), ('Sally',)}
            assert m.values() == {'Chamber', 'Prisoner', 'Infinity', 'Chronicle'}
            assert m.items() == []

        with detail("Use `None` as a nested key to mix key chain lengths."):
            m = Map({
                'Sally': {
                    None: {'Chronicle'},
                    'Hobbit': {'Unexpected', 'Desolation'}
                }
            })
            assert m.items() == {
                ('Sally', 'Chronicle'),
                (('Sally', 'Hobbit'), 'Desolation'),
                (('Sally', 'Hobbit'), 'Unexpected')
            }
            assert m == {
                'Sally': {
                    None: {'Chronicle'},
                    'Hobbit': {'Unexpected', 'Desolation'}
                }
            }

        with detail("Use `None` as a top-level key to organize values that are unassociated with any key."):
            m = Map({
                'Tom': {'Marvel': {'Avengers', 'Ultron'}},
                None: {'Infinity', 'Endgame'}
            })
            assert m.keys() == {('Tom',), ('Tom', 'Marvel')}
            assert m.values() == {'Avengers', 'Ultron', 'Infinity', 'Endgame'}

    def __eq__(map, other: Any) -> bool:
        """
        A `Map` object `map` is equal to an `Iterable` `other` when:

        1. The domain set of `map` is equal to the set created by iterating over `other`.
        2. For each domain element `e` in `map`, the set of corresponding codomain elements is equal to the set created by iterating over `other[e]`.

        :param other: An object to compare to `Map`.
        :return: Whether the mapping in `map` is equivalent to that defined by the iteration and subscripting of `other`.
        """
        assert map == {
            'John': {
                'Harry Potter': {'Chamber', 'Prisoner'},
                'Marvel': {'Infinity'}
            },
            'Sally': {
                None: {'Chronicle'}
            }
        }

        with detail("`Map` objects with keyless value sets are only equal to map-likes that define a keyless value set using `None` as a key"):
            m = Map({
                'Tom': {'Marvel': {'Avengers', 'Ultron'}},
                None: {'Infinity', 'Endgame'}
            })
            assert m == {
                'Tom': {'Marvel': {'Avengers', 'Ultron'}},
                None: {'Infinity', 'Endgame'}
            }
            assert m != {
                'Tom': {'Marvel': {'Avengers', 'Ultron'}},
            }
            assert m != Map({
                'Tom': {'Marvel': {'Avengers', 'Ultron'}},
            })
        return ...

    def __getitem__(map, key: Element) -> set | Mapping[Element, Elements]:
        """
        Get the set of codomain elements associated with `key`.

        :param key: An element in the `map` domain.
        :return: Values in the codomain associated with `key`.
        """
        assert map[['John', 'Harry Potter']] == {'Chamber', 'Prisoner'}
        assert map[['John']] == {'Chamber', 'Prisoner', 'Infinity'}
        assert map[['Sally']] == {'Chronicle'}
        assert map['John'] == {
            'Harry Potter': {'Chamber', 'Prisoner'},
            'Marvel': {'Infinity'}
        }

        with detail("Calling `map[key]` where `key not in map` raises `KeyError`."):
            with expecting(KeyError):
                values = map['Tom']
            with expecting(KeyError):
                values = map[['John', 'Hobbit']]

        with detail("Return value of `map[x]` is not a reference to the underlying codomain `set` or nested `dict`."):
            map['Sally'].add('History')
            assert map['Sally'] == {'Geography'}

        with detail("Can use `Map.KeyChain` objects instead of `list`s."):
            assert map[Map.KeyChain(('John', 'Harry Potter'))] == {'Chamber', 'Prisoner'}
        return ...

    def __contains__(map, key: Any) -> bool:
        """
        Check if the `map` contains a domain element.

        :param key:
        :return: Whether `key` is an element in the `map` domain.
        """
        assert 'John' in map
        assert 'Tom' not in map
        assert ['John'] in map
        assert ['John', 'Harry Potter'] in map
        assert ['Sally', 'Harry Potter'] not in map

        with detail("Any object can be checked for `in map` without error"):
            assert {} not in map
        return ...

    def __len__(map) -> int:
        """
        Get the number of elements in the `map` domain.

        Note that the number of elements in the `map` codomain can be found with `len(map.reverse)` or `len(map.values)`.

        :return: Non-negative number of domain elements.
        """
        assert len(map) == 3
        return ...

    def __iter__(map) -> Iterator:
        """
        The elements of a `Map` domain can be iterated over.

        :return: Iterator over keys of `map`.
        """
        s = set()
        for key in map:
            s.add(key)
        assert s == {('John', 'Harry Potter'), ('John', 'Marvel'), ('Sally',)}
        return ...

    def keys(map, up_to: int =None) -> set:
        """
        Get a set of keys in the `Map` domain.

        Specifying a positive integer `up_to` returns only keychains of length `up_to` or less.

        Specifying `up_to=0` returns all keychains.

        :return: Set of keys in the `Map` domain.
        """
        assert map.keys() == {'John', 'Sally'}
        assert map.keys(2) == {('John',), ('John', 'Harry Potter'), ('John', 'Marvel'), ('Sally',)}
        assert map.keys(1) == {('John',), ('Sally',)}

        with detail("Passing `up_to=0` returns the set of first keys"):
            assert map.keys(0) == {'John', 'Sally'}

        with detail("Passing `up_to=-x` returns key chain prefixes with x remaining keys in the full chain."):
            assert map.keys(-1) == {('John',)}

        with detail("Key chains returned by `Map` are `KeyChain` objects, not just `tuple`s."):
            some_keychain = next(iter(map.keys()))
            assert type(some_keychain) != tuple
            assert isinstance(some_keychain, tuple)
            assert isinstance(some_keychain, Map.KeyChain)

        with detail("Key chains returned by `Map` can be used as keys to access items."):
            some_keychain = next(iter(map.keys()))
            assert some_keychain in map
            values = map[some_keychain]
            assert values
        return ...

    def values(map) -> set:
        """
        :return: View of values in `map` codomain.
        """
        assert map.values() == {'Chamber', 'Prisoner', 'Infinity', 'Chronicle'}
        return ...

    def items(map) -> set[tuple]:
        """
        :return: View of (key, value) pairs in `map`.
        """
        assert sorted(map.items()) == {
            (['John', 'Harry Potter'], 'Chamber'),
            (['John', 'Harry Potter'], 'Prisoner'),
            (['John', 'Marvel'], 'Infinity'),
            (['Sally'], 'Chronicle')
        }
        return ...

    def get(map, key: Element, default: DefaultType =None) -> set | DefaultType:
        """
        Access values by key without `KeyError`.

        :return: Values associated with `key`, or `default` if `key not in map`.
        """
        assert map.get(['John', 'Harry Potter']) == {'Chamber', 'Prisoner'}
        assert map.get('John') == {
            'Harry Potter': {'Chamber', 'Prisoner'},
            'Marvel': {'Infinity'}
        }
        assert map.get('Tom') is None
        default = object()
        assert map.get('Tom', default) is default
        return ...

    @property
    def reverse(map) -> 'Map':
        """
        :return: View of `map` with domain and codomain inverted.
        """
        assert map.reverse == {
            'Chamber': ('John', 'Harry Potter'),
            'Prisoner': ('John', 'Harry Potter'),
            'Infinity': ('John', 'Marvel'),
            'Chronicle': ('Sally',)
        }
        assert isinstance(map.reverse, Map)

        with detail("Any mutations to `map.reverse` will be reflected in `map` and vice versa."):
            map.add(['John', 'Marvel'], 'Endgame')
            assert map.reverse['Endgame'] == {('John', 'Marvel')}
            assert map[['John', 'Marvel']] == {'Infinity', 'Endgame'}
        return ...

    def issubset(map, other: Mapping[Element, Elements] | Elements) -> bool:
        assert map.issubset({
            'John': {
                'Harry Potter': {'Chamber', 'Prisoner', 'Goblet'},
                'Marvel': {'Infinity'}
            },
            'Sally': {'Chronicle', 'Marriage'}
        })
        assert not map.issubset({
            'John': {
                'Harry Potter': {'Chamber'},
                'Marvel': {'Infinity'}
            },
            'Sally': {'Chronicle'}
        })

        with detail("Use of the `<=` operator checks for subset."):
            assert map <= {
                'John': {
                    'Harry Potter': {'Chamber', 'Prisoner', 'Goblet'},
                    'Marvel': {'Infinity'}
                },
                'Sally': {'Chronicle', 'Marriage'}
            }

        with detail("Passing a (non-mapping) iterable to `.issubset` will check if the set defined by that iterable is a superset of the `map` domain set."):
            assert map.issubset({
                ('John',),
                ('John', 'Harry Potter'),
                ('John', 'Marvel'),
                ('Sally',),
                ('Tom',)
            })

        with detail("`Map`s that are equal are subsets of each other."):
            assert map.issubset(Map(map))

        @Spec.subtest
        def test1():
            assert not map.issubset({
                ('John', 'Harry Potter'),
                ('John', 'Marvel'),
                ('Sally',)
            })
            assert not map.issubset({
                'John',
                ('John', 'Harry Potter'),
                ('John', 'Marvel'),
                'Sally'
            })
        return ...

    __le__ = issubset

    def ispropersubset(map, other: Mapping[Element, Elements] | Elements) -> bool:
        assert map.ispropersubset({
            'John': {
                'Harry Potter': {'Chamber', 'Prisoner', 'Goblet'},
                'Marvel': {'Infinity'}
            },
            'Sally': {'Chronicle', 'Marriage'}
        })
        assert not map.ispropersubset({
            'John': {
                'Harry Potter': {'Chamber'},
                'Marvel': {'Infinity'}
            },
            'Sally': {'Chronicle'}
        })

        with detail("Use of the `<` operator checks for subset."):
            assert map < {
                'John': {
                    'Harry Potter': {'Chamber', 'Prisoner', 'Goblet'},
                    'Marvel': {'Infinity'}
                },
                'Sally': {'Chronicle', 'Marriage'}
            }

        with detail("Passing a (non-mapping) iterable to `.ispropersubset` will check if the set defined by that iterable is a superset of the `map` domain set."):
            assert map.ispropersubset({
                ('John',),
                ('John', 'Harry Potter'),
                ('John', 'Marvel'),
                ('Sally',),
                ('Tom',)
            })

        with detail("`Map`s that are equal are NOT proper subsets of each other."):
            assert not map.ispropersubset(Map(map))

        @Spec.subtest
        def test1():
            assert not map.ispropersubset({
                ('John', 'Harry Potter'),
                ('John', 'Marvel'),
                ('Sally',)
            })
            assert not map.ispropersubset({
                ('John',),
                ('John', 'Harry Potter'),
                ('John', 'Marvel'),
                ('Sally',),
                'Tom'
            })
        return ...

    __lt__ = ispropersubset

    def issuperset(map, other: Mapping[Element, Elements] | Elements) -> bool:
        assert map.issuperset({
            'John': {
                'Harry Potter': {'Chamber'},
                'Marvel': {'Infinity'}
            },
            'Sally': {'Chronicle'}
        })
        assert not map.issuperset({
            'John': {
                'Harry Potter': {'Chamber', 'Prisoner', 'Goblet'},
                'Marvel': {'Infinity'}
            },
            'Sally': {'Chronicle', 'Marriage'}
        })

        with detail("Use of the `>=` operator checks for subset."):
            assert map >= {
                'John': {
                    'Harry Potter': {'Chamber'},
                    'Marvel': {'Infinity'}
                },
                'Sally': {'Chronicle'}
            }

        with detail("Passing a (non-mapping) iterable to `.issuperset` will check if the set defined by that iterable is a superset of the `map` domain set."):
            assert map.issuperset({
                ('John',),
                ('John', 'Harry Potter'),
                ('John', 'Marvel'),
            })

        with detail("`Map`s that are equal are supersets of each other."):
            assert map.issuperset(Map(map))

        @Spec.subtest
        def test1():
            assert map.issuperset({
                ('John',),
                ('John', 'Harry Potter'),
                ('Sally',)
            })
            assert not map.issuperset({
                'John',
                ('John', 'Harry Potter'),
                ('John', 'Marvel'),
            })
        return ...

    __ge__ = issuperset

    def ispropersuperset(map, other: Mapping[Element, Elements] | Elements) -> bool:
        assert map.ispropersuperset({
            'John': {
                'Harry Potter': {'Chamber'},
                'Marvel': {'Infinity'}
            },
            'Sally': {'Chronicle'}
        })
        assert not map.ispropersuperset({
            'John': {
                'Harry Potter': {'Chamber', 'Prisoner', 'Goblet'},
                'Marvel': {'Infinity'}
            },
            'Sally': {'Chronicle', 'Marriage'}
        })

        with detail("Use of the `>` operator checks for subset."):
            assert map > {
                'John': {
                    'Harry Potter': {'Chamber'},
                    'Marvel': {'Infinity'}
                },
                'Sally': {'Chronicle'}
            }

        with detail("Passing a (non-mapping) iterable to `.ispropersuperset` will check if the set defined by that iterable is a superset of the `map` domain set."):
            assert map.ispropersuperset({
                ('John',),
                ('John', 'Harry Potter'),
                ('John', 'Marvel'),
            })

        with detail("`Map`s that are equal are NOT proper supersets of each other."):
            assert not map.ispropersuperset(Map(map))

        @Spec.subtest
        def test1():
            assert map.ispropersuperset({
                ('John',),
                ('John', 'Harry Potter'),
                ('Sally',)
            })
            assert not map.ispropersuperset({
                'John',
                ('John', 'Harry Potter'),
                ('John', 'Marvel'),
            })
        return ...

    __gt__ = ispropersuperset

    def isdisjoint(map, other: Mapping[Element, Elements] | Elements) -> bool:
        """
        :param other: A
        :return: Whether the set of keychains are disjoint between `Map` and `other`.
        """
        assert map.isdisjoint({
            'Tom': {
                'Harry Potter': {'Chamber'},
                'Marvel': {'Infinity', 'Endgame'}
            }
        })
        assert not map.isdisjoint({
            'Tom': {
                'Harry Potter': {'Chamber'},
                'Marvel': {'Infinity', 'Endgame'}
            },
            'Sally': set()
        })

        with detail("Can check `.isdisjoint` against an `Iterable` of keychains."):
            assert not map.isdisjoint({('Tom', 'Harry Potter'), ('Sally',)})

        @Spec.subtest
        def test1():
            """
            If `other` is `Map`-like, tuple keys are treated as a single key, not a keychain. Keys must be nested in `Map`-likes to be treated as a keychain.
            """
            assert map.isdisjoint({
                ('John', 'Harry Potter'): {'Chamber'}
            })
        @Spec.subtest
        def test2():
            assert map.isdisjoint({'Sally', ('Tom', 'Harry Potter')})
        return ...

    def __setitem__(map, key: Element, values: Mapping[Element, Elements] | Elements):
        """
        Assign values from iterable `values` to `key`, replacing any existing values associated with `key`.

        Replaced values will be removed from the `Map` entirely if they are no longer associated with any key in the `Map`.

        If `key not in map`, add `key` to map keys.

        :param key: Key to add to `map` domain.
        :param values: Values (or sub-`Map`-like) to associate with `key` in the `map` codomain.
        """
        map[['John']] = {'Inception', 'Interstellar'}
        assert map['John'] == {
            None: {'Inception', 'Interstellar'},
            'Harry Potter': {'Chamber', 'Prisoner'},
            'Marvel': {'Infinity'}
        }

        map[['John', 'Marvel']] = {'Ultron', 'Endgame'}
        assert map['John'] == {
            None: {'Inception', 'Interstellar'},
            'Harry Potter': {'Chamber', 'Prisoner'},
            'Marvel': {'Ultron', 'Endgame'}
        }

        map['John'] = {
            'Star Wars': {'Empire', 'Return'}
        }
        assert map['John'] == {
            'Star Wars': {'Empire', 'Return'}
        }

        with detail("`Map`s use their own `set` to represent `values`, rather than taking a provided `values` collection by reference."):
            values = {'Ultron', 'Endgame'}
            map[['John', 'Marvel']] = values
            assert map[['John', 'Marvel']] == values
            assert map[['John', 'Marvel']] is not values

        with detail("Replacement of values can remove values completely"):
            m = Map({
                'John': {
                    'Marvel': {'Ultron', 'Infinity'}
                },
                'Sally': {
                    'Marvel': {'Infinity', 'Endgame'}
                }
            })
            m[['John', 'Marvel']] = {'Avengers'}
            assert m == {
                'John': {
                    'Marvel': {'Avengers'}
                },
                'Sally': {
                    'Marvel': {'Infinity', 'Endgame'}
                }
            }
            assert m.values() == {'Avengers', 'Infinity', 'Endgame'}

    def add(map, key: Element, values: Mapping[Element, Elements] | Elements=None):
        """
        Add a key and/or values to the `Map`.

        Similar to `map.setdefault(key, values)`, but `add` will add `values` to the set of existing values associated with `key`, and will never replace existing values.

        :param key: Key to add to `map` domain, or existing key to add values to.
        :param values: Values (or sub-`Map`-like) to associate with `key`.
        """
        map.add(['Tom', 'Star Wars'])
        assert map.keys() == {
            ('John',), ('John', 'Harry Potter'), ('John', 'Marvel'),
            ('Sally',),
            ('Tom',), ('Tom', 'Star Wars')
        }
        assert map['Tom'] == {'Star Wars': []}

        map.add(['Tom', 'Star Wars'], {'Empire', 'Return'})
        assert map['Tom'] == {'Star Wars': {'Empire', 'Return'}}
        map.add(['Tom', 'Star Wars'], {'Attack', 'Revenge'})
        assert map['Tom'] == {'Star Wars': {'Empire', 'Return', 'Attack', 'Revenge'}}

    def additem(map, key: Element, value: Element):
        """
        Add a single value to the value set associated with `key`.

        :param key: Key or keychain to add a value to.
        :param value: Value to add.
        """
        map.add(['Tom', 'Star Wars'], 'Empire')
        assert map['Tom'] == {'Star Wars': {'Empire'}}

        map.add(['Tom', 'Star Wars'], 'Revenge')
        assert map['Tom'] == {'Star Wars': {'Empire', 'Revenge'}}

    def setdefault(map, key: Element, values: Elements | Mapping[Element, Elements] = None) -> set | Mapping[Element, Elements]:
        """
        Get values associated with a key/keychain, or insert the key/keychain with the provided values if it is not in `map`.

        Similar to `map.setdefault(key, values)`, but `add` will add `values` to the set of existing values associated with `key`, and will never replace existing values.

        :param key: Key to add to `map` domain, or existing key to add values to.
        :param values: Values (or sub-`Map`-like) to associate with `key` if `key not in map`.
        :return: Values associated with `key`.
        """
        assert map.setdefault(['Tom', 'Star Wars']) is None
        assert map.keys() == {
            ('John',), ('John', 'Harry Potter'), ('John', 'Marvel'),
            ('Sally',),
            ('Tom',), ('Tom', 'Star Wars')
        }
        assert map['Tom'] == {'Star Wars': []}

        assert map.setdefault(['Megan', 'Marvel'], {'Avengers'}) == {'Avengers'}
        assert map[['Megan', 'Marvel']] == {'Avengers'}

        assert map.setdefault(['Megan', 'Marvel'], {'Infinity', 'Endgame'}) == {'Avengers'}
        assert map[['Megan', 'Marvel']] == {'Avengers'}
        return ...

    def __delitem__(map, key: Element):
        """
        Remove a key, and any of its values that are not associated to any other key.

        :param key: to remove from `map` domain.
        """
        del map[['John', 'Marvel']]
        assert map == {
            'John': {'Harry Potter': {'Chamber', 'Prisoner'}},
            'Sally': {'Chronicle'}
        }

        del map['John']
        assert map == {
            'Sally': {'Chronicle'}
        }
        assert map.values() == {'Chronicle'}

        with detail("`.delete` can also be used to delete items by key."):
            map.delete('Sally')
            assert map == {}

        with detail("`.delete` raises `KeyError` if `key not in map`"):
            with expecting(KeyError):
                del map['Tom']

    def delete(map, key: Element, value: Elements =None):
        """
        Remove a key, OR the association between a key and one of its values.

        Removing the association between a key and one of its values will remove that value if it is not associated to any other key.

        Raises `KeyError` if `key` or `value` does not exist.

        :param key: to remove from `map` domain.
        :param value:
        """
        map.delete(['John', 'Marvel'])
        assert map == {
            'John': {'Harry Potter': {'Chamber', 'Prisoner'}},
            'Sally': {'Chronicle'}
        }
        assert map.values() == {'Chamber', 'Prisoner', 'Chronicle'}

        map.delete(['John', 'Harry Potter'], 'Prisoner')
        assert map == {
            'John': {'Harry Potter': {'Prisoner'}},
            'Sally': {'Chronicle'}
        }
        assert map.values() == {'Prisoner', 'Chronicle'}

        map.delete('John')
        assert map == {
            'Sally': {'Chronicle'}
        }
        assert map.values() == {'Chronicle'}

        with detail("`del` can also be used to delete items by key."):
            del map['Sally']
            assert map == {}

        with detail("`.delete` raises `KeyError` if `key not in map`"):
            with expecting(KeyError):
                del map['Tom']

        @Spec.subtest
        def test1():
            m = Map({
                'John': {
                    None: {'Chronicle'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                },
                'Sally': {
                    None: {'Chamber'},
                    'Harry Potter': {'Prisoner', 'Goblet'}
                }
            })
            m.delete('John')
            assert m.values() == {'Chamber', 'Prisoner', 'Goblet'}
            assert m == {
                'Sally': {
                    None: {'Chamber'},
                    'Harry Potter': {'Prisoner', 'Goblet'}
                }
            }

        @Spec.subtest
        def test2():
            m = Map({
                'John': {
                    None: {'Chronicle', 'Prisoner'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                }
            })
            m.delete('John', 'Prisoner')
            assert m == {
                'John': {
                    None: {'Chronicle'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                }
            }

            with expecting(ValueError):
                m.delete('John', 'Chamber')

        @Spec.subtest
        def test3():
            m = Map({
                'John': {
                    None: {'Chronicle', 'Prisoner'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                }
            })
            m.delete(['John'], 'Prisoner')
            assert m == {
                'John': {
                    None: {'Chronicle'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                }
            }

            with expecting(ValueError):
                m.delete(['John'], 'Chamber')

        @Spec.subtest
        def test4():
            m = Map({
                'John': {
                    None: {'Chronicle', 'Prisoner'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                }
            })
            m.delete(['John', ...], 'Prisoner')
            assert m == {
                'John': {
                    None: {'Chronicle'},
                    'Harry Potter': {'Chamber'}
                }
            }
            assert m.values() == {'Chronicle', 'Chamber'}

    def clear(map, key: Element =None, value: Elements =None):
        """
        Remove a key, OR the association between a key and one of its values.

        Removing the association between a key and one of its values will remove that value if it is not associated to any other key.

        Unlike `.delete`, `.clear` never raises `KeyError`, even if `key` or `value` do not exist.

        :param key: to remove from `map` domain.
        :param value:
        """
        map.clear(['John', 'Marvel'])
        assert map == {
            'John': {'Harry Potter': {'Chamber', 'Prisoner'}},
            'Sally': {'Chronicle'}
        }
        assert map.values() == {'Chamber', 'Prisoner', 'Chronicle'}

        map.clear(['John', 'Harry Potter'], 'Prisoner')
        assert map == {
            'John': {'Harry Potter': {'Prisoner'}},
            'Sally': {'Chronicle'}
        }
        assert map.values() == {'Prisoner', 'Chronicle'}

        map.clear('John')
        assert map == {
            'Sally': {'Chronicle'}
        }
        assert map.values() == {'Chronicle'}

        map.clear('Tom')

        @Spec.subtest
        def test1():
            m = Map({
                'John': {
                    None: {'Chronicle'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                },
                'Sally': {
                    None: {'Chamber'},
                    'Harry Potter': {'Prisoner', 'Goblet'}
                }
            })
            m.clear('John')
            assert m.values() == {'Chamber', 'Prisoner', 'Goblet'}
            assert m == {
                'Sally': {
                    None: {'Chamber'},
                    'Harry Potter': {'Prisoner', 'Goblet'}
                }
            }

        @Spec.subtest
        def test2():
            m = Map({
                'John': {
                    None: {'Chronicle', 'Prisoner'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                }
            })
            m.clear('John', 'Prisoner')
            assert m == {
                'John': {
                    None: {'Chronicle'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                }
            }

            m.clear('John', 'Chamber')

        @Spec.subtest
        def test3():
            m = Map({
                'John': {
                    None: {'Chronicle', 'Prisoner'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                }
            })
            m.clear(['John'], 'Prisoner')
            assert m == {
                'John': {
                    None: {'Chronicle'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                }
            }

            m.clear(['John'], 'Chamber')

        @Spec.subtest
        def test4():
            m = Map({
                'John': {
                    None: {'Chronicle', 'Prisoner'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                }
            })
            m.clear(['John', ...], 'Prisoner')
            assert m == {
                'John': {
                    None: {'Chronicle'},
                    'Harry Potter': {'Chamber'}
                }
            }
            assert m.values() == {'Chronicle', 'Chamber'}

    def remove(map, key, value=None):
        """
        Remove a key, OR the association between a key and one of its values.

        Unlike `.delete`, `.remove` will never remove `values` from the `Map` entirely.

        Raises `KeyError` if `key` or `value` does not exist.

        :param key: to remove from `map` domain.
        :param value:
        """
        map.remove(['John', 'Marvel'])
        assert map == {
            'John': {'Harry Potter': {'Chamber', 'Prisoner'}},
            'Sally': {'Chronicle'},
            None: {'Infinity'}
        }
        assert map.values() == {'Chamber', 'Prisoner', 'Chronicle', 'Infinity'}

        map.remove(['John', 'Harry Potter'], 'Prisoner')
        assert map == {
            'John': {'Harry Potter': {'Chamber'}},
            'Sally': {'Chronicle'},
            None: {'Infinity', 'Prisoner'}
        }
        assert map.values() == {'Chamber', 'Prisoner', 'Chronicle', 'Infinity'}

        map.remove('John')
        assert map == {
            'Sally': {'Chronicle'}
        }
        assert map.values() == {'Chamber', 'Prisoner', 'Chronicle', 'Infinity'}

        with detail("`.remove` raises `KeyError` if `key not in map`"):
            with expecting(KeyError):
                map.remove('Tom')

        @Spec.subtest
        def test1():
            m = Map({
                'John': {
                    None: {'Chronicle'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                },
                'Sally': {
                    None: {'Chamber'},
                    'Harry Potter': {'Prisoner', 'Goblet'}
                }
            })
            m.remove('John')
            assert m.values() == {'Chronicle', 'Chamber', 'Prisoner', 'Goblet'}
            assert m == {
                'Sally': {
                    None: {'Chamber'},
                    'Harry Potter': {'Prisoner', 'Goblet'}
                },
                None: {'Chronicle'}
            }

        @Spec.subtest
        def test2():
            m = Map({
                'John': {
                    None: {'Chronicle', 'Prisoner'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                }
            })
            m.remove('John', 'Prisoner')
            assert m == {
                'John': {
                    None: {'Chronicle'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                }
            }

            with expecting(ValueError):
                m.remove('John', 'Chamber')

        @Spec.subtest
        def test3():
            m = Map({
                'John': {
                    None: {'Chronicle', 'Prisoner'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                }
            })
            m.remove(['John'], 'Prisoner')
            assert m == {
                'John': {
                    None: {'Chronicle'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                }
            }

            with expecting(ValueError):
                m.remove(['John'], 'Chamber')

        @Spec.subtest
        def test4():
            m = Map({
                'John': {
                    None: {'Chronicle', 'Prisoner'},
                    'Harry Potter': {'Chamber', 'Prisoner'}
                }
            })
            m.remove(['John', ...], 'Prisoner')
            assert m == {
                'John': {
                    None: {'Chronicle'},
                    'Harry Potter': {'Chamber'}
                }
            }
            assert m.values() == {'Chronicle', 'Chamber'}

    def discard(map, key, value=None):
        """

        :param key:
        :param value:
        :return:
        """

    def pop(map, key=None, default=None): ...

    def popitem(map, key=None, default=None): ...

    def union_update(map, other): ...

    update = union_update
    __ior__ = union_update

    def intersection_update(map, other): ...

    __iand__ = intersection_update

    def filtrate_update(map, other): ...

    __itruediv__ = filtrate_update

    def difference_update(map, other): ...

    __isub__ = difference_update

    def symmetric_difference_update(map, other): ...

    __ixor__ = symmetric_difference_update

    def residuum_update(map, other): ...

    __imod__ = residuum_update

    def symmetric_residuum_update(map, other): ...

    __ipow__ = symmetric_residuum_update

    def union(map, other): ...

    __or__ = union

    def intersection(map, other): ...

    __and__ = intersection

    def filtrate(map, other): ...

    __truediv__ = filtrate

    def difference(map, other): ...

    __sub__ = difference

    def symmetric_difference(map, other): ...

    __xor__ = symmetric_difference

    def residuum(map, other): ...

    __mod__ = residuum

    def symmetric_residuum(map, other): ...

    __pow__ = symmetric_residuum





