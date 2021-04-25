"""
Mapping of elements between a domain and codomain.
"""

from structpy import spec
from structpy.system import default


def __init__(Himap, mapping):
    map = Himap({
        'bat': {'Bat', 'Flying Mammal'},
        'baseball_bat': {
            Himap.values: {'Baseball Bat', 'Bat'},
            'spanish': {
                'common': {'Bate'},
                'uncommon': {'Raqueta', 'Cosa'}
            }
        }
    })
    return map

def _domain(map):
    assert set(map.domain) == {'bat', 'baseball_bat'}

def _codomain(map):
    assert set(map.codomain) == {
        'Bat', 'Flying Mammal',
        'Baseball Bat', 'Bate', 'Raqueta', 'Cosa'
    }

def __contains__(map, key):
    assert 'bat' in map
    assert 'Bat' not in map

def has_item(map, key=default, value=default, *keys):
    assert map.has_item('bat')
    assert map.has_item(value='Bat')
    assert map.has_item('bat', 'Bat')
    assert map.has_item('baseball_bat', 'Cosa', 'spanish', 'uncommon')
    assert map.has_item('baseball_bat', 'Cosa', 'spanish')

def has(map, *chain, value=default):
    assert map.has('bat')
    assert map.has('bat', 'Bat')
    assert map.has('baseball_bat', 'spanish', 'common')
    assert map.has('baseball_bat', 'spanish', 'common', 'Bate')
    assert map.has('baseball_bat', 'spanish', value='Bate')
    assert not map.has('baseball_bat', 'spanish', 'Bate')

def has_map(map, other):
    assert map.has_map({'bat': {'Bat'}})
    assert map.has_map({
        'bat': {'Bat', 'Flying Mammal'},
        'baseball_bat': {
            map.values: {'Bat'},
            'spanish': {
                'common': {'Bate'}
            }
        }
    })

def __getitem__(map, key):
    assert map['bat'] == {'Bat', 'Flying Mammal'}
    assert map['baseball_bat'] == {'Bat', 'Baseball Bat', 'Bate', 'Raqueta', 'Cosa'}
    assert map[['baseball_bat']] == {'Bat', 'Baseball Bat', 'Bate', 'Raqueta', 'Cosa'}
    assert map[['baseball_bat', 'spanish']] == {'Bate', 'Raqueta', 'Cosa'}
    assert map[['baseball_bat', 'spanish', 'common']] == {'Bate'}
    with spec.raises(KeyError): map[['baseball_bat', 'english']] == set()

def __call__(map, *keys):
    assert map('baseball_bat') == {'Bat', 'Baseball Bat', 'Bate', 'Raqueta', 'Cosa'}
    assert map('baseball_bat', 'spanish') == {'Bate', 'Raqueta', 'Cosa'}
    assert map('baseball_bat', 'spanish', 'common') == {'Bate'}
    with spec.raises(KeyError): map('baseball_bat', 'english') == set()

def get(map, *keys):
    assert map.get('bat') == {'Bat', 'Flying Mammal'}
    assert map.get('cat') == set()
    assert map.get('bat', 'small') == set()

def __iter__(map):
    assert set(map) == {'baseball_bat', 'bat'}

def __len__(map):
    assert len(map) == len(list(map.keys()))

def len_items(map):
    assert map.len_items() == 7

def len_values(map):
    assert map.len_values() == 7

def keys(map, key=default, value=default, *keys):
    assert set(map.keys()) == {
        ('bat',), ('baseball_bat',),
        ('baseball_bat', 'spanish', 'common'),
        ('baseball_bat', 'spanish', 'uncommon',)
    }

def values(map, *keys):
    assert map.values() == {'Bat', 'Baseball Bat', 'Bate', 'Raqueta', 'Cosa', 'Flying Mammal'}
    assert map.values('baseball_bat') == {'Bat', 'Baseball Bat', 'Bate', 'Raqueta', 'Cosa'}
    assert map.values('baseball_bat', 'spanish') == {'Bate', 'Raqueta', 'Cosa'}
    assert map.values('baseball_bat', 'spanish', 'common') == {'Bate'}
    with spec.raises(KeyError): map.values('baseball_bat', 'english') == set()

def items(map, *keys):
    assert set(map.items()) == {
        ('bat', 'Bat'), ('bat', 'Flying Mammal'),
        ('baseball_bat', 'Bat'), ('baseball_bat', 'Baseball Bat')
        ('baseball_bat', 'Bate'), ('baseball_bat', 'Raqueta'), ('baseball_bat', 'Cosa')
    }
    assert set(map.items('bat')) == {('bat', 'Bat'), ('bat', 'Flying Mammal')}
    assert set(map.items('baseball_bat', 'spanish')) == {
        ('baseball_bat', 'Bate'), ('baseball_bat', 'Raqueta'), ('baseball_bat', 'Cosa')
    }

def chains(map, key=default, value=default, *keys):
    assert set(map.chains()) == {
        ('bat', 'Bat'), ('bat', 'Flying Mammal'),
        ('baseball_bat', 'Bat'), ('baseball_bat', 'Baseball Bat'),
        ('baseball_bat', 'spanish', 'common', 'Bate'),
        ('baseball_bat', 'spanish', 'uncommon', 'Raqueta'),
        ('baseball_bat', 'spanish', 'uncommon', 'Cosa')
    }
    assert set(map.chains(keys=('baseball_bat', 'spanish', 'uncommon'))) == {
        ('baseball_bat', 'spanish', 'uncommon', 'Raqueta'),
        ('baseball_bat', 'spanish', 'uncommon', 'Cosa')
    }
    assert set(map.chains('baseball_bat', 'Bate')) == {
        ('baseball_bat', 'spanish', 'common', 'Bate')
    }
    assert set(map.chains(value='Bat')) == {
        ('bat', 'Bat'),
        ('baseball_bat', 'Bat')
    }

def add(map, *chain):
    map.add('cat', 'old', 'Old Cat')
    assert map.has('cat', 'old', 'Old Cat')
    map.add('cat', 'old', 'OC')
    assert map('cat' 'old') == {'OC', 'Old Cat'}
    map.add('cat', 'Cat')
    assert map('cat') == {'Cat'}
    map.add('cat', 'Kitty')
    assert map('cat') == {'Cat', 'Kitty'}
    map.add('cat', 'young', 'Kitten')
    assert map('cat') == {'Cat', 'Kitty', 'Kitten'}
    assert map('cat', 'young') == {'Kitten'}

def map(map, key, values):
    assert map.map('dog', ['Dog']) == {'Dog'}
    assert map.map('dog', ('Doggo', 'Pupper')) == {'Dog', 'Doggo', 'Pupper'}
    assert map('dog') == {'Dog', 'Doggo', 'Pupper'}
    assert map.map(['dog', 'other'], ['Pooch', 'Canine']) == {'Pooch', 'Canine'}
    assert map('dog', 'other') == {'Pooch', 'Canine'}

def update(map, other):
    map.update({'dog': {'relative': {'Friend'}}})
    assert map('dog', 'relative') == {'Friend'}
    assert map('dog') == {'Dog', 'Doggo', 'Pupper', 'Pooch', 'Canine', 'Friend'}
    map.update({'snake': {'Snake', 'Serpent'}})
    assert map('snake') == {'Snake', 'Serpent'}

def map_default(map, key, values):
    assert map.map_default(['lizard', 'normal'], ['Lizard', 'Reptile']) == {'Lizard', 'Reptile'}
    assert map('lizard', 'normal') == {'Lizard', 'Reptile'}
    assert map.map_default('lizard', ['Dragon']) == {'Lizard', 'Reptile'}
    assert map('lizard') == {'Lizard', 'Reptile'}

def remove_item(map, key, value, *keys):
    map.remove_item('lizard', 'Lizard')
    assert not map.has_item('lizard', 'Lizard')
    map.remove_item('lizard', 'Reptile', 'normal')
    assert not map.has_item('lizard', 'Reptile')
    assert 'lizard' not in map
    try: map.remove_item('lizard', 'Lizard'); assert False
    except KeyError: pass
    try: map.remove_item('dog', 'Cat'); assert False
    except ValueError: pass

def remove(map, *chain, value=default):
    map.remove('dog', 'relative')
    assert not map.has('dog', 'relative')
    assert not map.has_item('dog', 'Friend')
    map.remove('dog', value='Pupper')
    assert not map.has_item('dog', 'Pupper')
    map.remove('dog')
    assert 'dog' not in map
    try: map.remove('dog'); assert False
    except KeyError: pass

def discard_item(map, key, value, *keys):
    assert not map.has_item('lizard', 'Dragon')
    map.discard_item('lizard', 'Dragon')
    map.discard_item('lizard', 'Lizard')
    assert not map.has_item('lizard', 'Lizard')
    map.discard_item('lizard', 'Lizard')
    map.discard_item('lizard')
    assert 'lizard' not in map
    map.discard_item('lizard')

def discard(map, *chain, value=default):
    assert not map.has('cat', 'old')
    map.discard('cat', 'old')
    map.discard('cat', 'young')
    assert not map.has('cat', 'young')
    assert map.has_item('cat', 'Cat')
    map.discard('cat', value='Cat')
    assert not map.has_item('cat', 'Cat')
    map.discard('cat', value='Cat')
    assert 'cat' in map
    map.discard('cat')
    assert 'cat' not in map
    map.discard('cat')

def __delitem__(map, key):
    del map['snake']
    assert 'snake' not in map
    with spec.raises(KeyError): del map['snake']

def replace(map, old_item, new_value=default, new_item=default):
    map.replace(('bat', 'Flying Mammal'), 'fm')
    assert not map.has_item('bat', 'Flying Mammal')
    assert map.has_item('bat', 'fm')
    map.replace(('bat', 'fm'), new_item=('bat', 'x', 'FM'))
    assert not map.has_item('bat', 'fm')
    assert map.has('bat', 'x', 'FM')

def pop_item(map, key=default, value=default, *keys):
    assert len(map('baseball_bat', 'spanish', 'uncommon')) == 2
    assert map.pop_item('baseball_bat', 'spanish', 'uncommon') in {
        ('baseball_bat', 'spanish', 'uncommon', 'Cosa'),
        ('baseball_bat', 'spanish', 'uncommon', 'Raqueta')
    }
    assert len(map('baseball_bat', 'spanish', 'uncommon')) == 1
    assert len(map('baseball_bat', 'spanish')) == 2
    assert map.pop_item('baseball_bat', 'spanish') in {
        ('baseball_bat', 'spanish', 'uncommon', 'Cosa'),
        ('baseball_bat', 'spanish', 'uncommon', 'Raqueta'),
        ('baseball_bat', 'spanish', 'common', 'Bate')
    }
    assert map.pop_item('baseball_bat', 'spanish') in {
        ('baseball_bat', 'spanish', 'uncommon', 'Cosa'),
        ('baseball_bat', 'spanish', 'uncommon', 'Raqueta'),
        ('baseball_bat', 'spanish', 'common', 'Bate')
    }
    assert not map.has('baseball_bat', 'spanish')
    assert map.pop_item() in {
        ('bat', 'Bat'),
        ('bat', 'x', 'FM'),
        ('baseball_bat', 'Bat'),
        ('baseball_bat', 'Baseball Bat')
    }
    assert map.len_items() == 3

def pop(map, *chain, value=default):
    assert map.len_items == 3
    map.pop()
    map.pop()
    assert map.len_items() == 1


if __name__ == '__main__':
    from structpy.map_.map import Map
    spec.verify(Map)