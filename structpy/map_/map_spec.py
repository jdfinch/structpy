"""
Mapping of elements between a domain and codomain.
"""

from structpy import spec
from structpy.system import default


def __init__(Map, mapping=default):
    map = Map({
        'fast': {'car', 'jet'},
        'air': {'jet', 'balloon'}
    })
    return map

def __contains__(map, key):
    assert 'fast' in map
    assert 'car' not in map

def has(map, key, value=default):
    assert map.has('fast')
    assert map.has('fast', 'car')
    assert map.has(value='jet')
    assert not map.has('fast', 'balloon')

def __getitem__(map, key):
    assert map['fast'] == {'car', 'jet'}
    try: map['slow']
    except KeyError: pass

def get(map, key):
    assert map.get('fast') == {'car', 'jet'}
    assert map.get('slow') == set()

def __iter__(map):
    assert set(map) == {'fast', 'air'}

def __len__(map):
    assert len(map) == 2

def len_keys(map):
    assert map.len_keys() == 2

def len_values(map):
    assert map.len_values() == 3

def len_items(map):
    assert map.len_items() == 4

def keys(map, value=default):
    assert set(map.keys()) == {'fast', 'air'}
    assert map.keys('jet') == {'fast', 'air'}
    assert map.keys('car') == {'fast'}

def values(map, key=default):
    assert set(map.values()) == {'jet', 'car', 'balloon'}
    assert map.values('fast') == {'jet', 'car'}

def items(map):
    assert set(map.items()) == {
        ('fast', 'jet'), ('fast', 'car'), ('air', 'jet'), ('air', 'balloon')
    }

def add(map, key, value):
    map.add('fast', 'rocket')
    assert map['fast'] == {'jet', 'car', 'rocket'}
    map.add('space', 'rocket')
    assert map['space'] == {'rocket'}

def update(map, key, values):
    map.update('fast', ['starship'])
    assert map['fast'] == {'starship', 'car', 'jet'}
    map.update('ocean', ['submarine', 'ship'])
    assert map['ocean'] == {'submarine', 'ship'}

def map(map, mapping):
    map.map({
        'fast': {'starship'},
        'slow': {'tank', 'balloon'}
    })
    assert map['fast'] == {'car', 'jet', 'starship'}
    assert map['slow'] == {'tank', 'balloon'}

def remove(map, key, value=default):
    map.remove('air', 'balloon')
    assert map['air'] == {'jet'}
    map.remove('air')
    assert 'air' not in map
    try: map.remove('air')
    except KeyError: pass

def discard(map, key, value=default):
    map.discard('air', 'balloon')
    assert map['air'] == {'jet'}
    map.discard('air')
    assert 'air' not in map
    map.discard('air')

def __delitem__(map, key):
    del map['fast']
    assert 'fast' not in map
    try: del map['fast']
    except KeyError: pass

def pop(map, key=default):
    assert map.pop('air') in {('air', 'jet'), ('air', 'balloon')}
    assert len(map['air']) == 1
    assert map.pop('air') in {('air', 'jet'), ('air', 'balloon')}
    assert 'air' not in map


from structpy.map_.map import Map

if __name__ == '__main__':
    spec.verify(Map)