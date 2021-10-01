"""
Mapping of elements between a domain and codomain.
"""

from structpy import specxxx
from structpy.system import default


def __init__(Himap, mapping=default):
    map = Himap({
        'fast': {
            Himap.vals: {'rocket'},
            'air': {'jet'},
            'land': {'car', 'train'}
        },
        'cargo': {'train', 'jet', 'semi'}
    })

def __contains__(map, keys):
    assert ('fast', 'air') in map
    assert ('fast',) in map
    assert ['fast'] in map
    assert ('air',) not in map
    assert 'fast' not in map
    assert ('rocket',) not in map

def has(map, keys, value=default):
    assert map.has(('fast',))
    assert map.has(('fast', 'air'))
    assert map.has(('fast', 'air'), 'jet')
    assert not map.has(('fast',), 'semi')
    assert map.has(value='semi')

def __getitem__(map, keys):
    assert map[('fast', 'land')] == {'car', 'train'}
    assert map[['fast']] == {'rocket', 'jet', 'car', 'train'}
    try: map['slow']
    except KeyError: pass

def get(map, keys):
    assert map.get(('fast', 'land')) == {'car', 'train'}
    assert map.get(['fast']) == {'rocket', 'jet', 'car', 'train'}
    assert map.get(['slow']) == set()

def __iter__(map):
    assert set(map) == {'fast', 'land', 'air', 'cargo'}

def __len__(map):
    assert len(map) == 4

def len_keys(map):
    assert map.len_keys() == 4

def len_values(map):
    assert map.len_values() == 5

def len_items(map):
    assert map.len_items() == 7

def keys(map, value=default):
    assert set(map.keys()) == {
        ('fast',), ('fast', 'air'), ('fast', 'land',), ('cargo',)
    }
    assert map.keys('jet') == {('fast', 'air'), ('cargo',)}
    try: map.keys('sub')
    except ValueError: pass

def values(map, keys=default):
    assert set(map.values()) == {'rocket', 'jet', 'train', 'semi', 'car'}
    assert map.values(('fast',)) == {'rocket'}
    assert map.values(('fast', 'land')) == {'car', 'jet'}
    try: map.values(('slow',))
    except KeyError: pass

def items(map, keys=default, value=default):
    assert set(map.items()) == {
        (('fast',), 'rocket'), (('fast', 'air'), 'jet'), (('fast', 'land'), 'car'),
        (('fast', 'land'), 'train'), (('cargo',), 'train'), (('cargo',), 'semi'),
        (('cargo',), 'jet')
    }
    assert map.items(('fast', 'air')) == {(('fast', 'air'), 'jet')}
    assert map.items(('fast',)) == {
        (('fast', 'air'), 'jet'), (('fast',), 'rocket'), (('fast', 'land'), 'car'),
        (('fast', 'land'), 'train')
    }
    assert map.items(value='jet') == {(('fast', 'air'), 'jet'), (('cargo',), 'jet')}
    assert map.items(('fast',), 'jet') == {(('fast', 'air'), 'jet')}

def add(map, keys, value):
    map.add(('fast',), 'magnarail')
    assert map[('fast',)] == {'magnarail', 'rocket', 'car', 'train', 'jet'}
    map.add(('slow',), 'balloon')
    assert map[('slow',)] == {'balloon'}
    map.add(('slow', 'land'), 'horse')
    assert map[('slow', 'land')] == {'horse'}

def update(map, keys, values):
    map.update(('fast',), ['magnarail', 'helicopter'])
    assert map[('fast',)] == {'magnarail', 'helicopter', 'rocket', 'car', 'train', 'jet'}
    map.update(('slow', 'sea'), ['sub', 'ship'])
    assert map[('slow', 'sea')] == {'sub', 'ship'}

def remove(map, keys, value=default):
    map.remove(('fast', 'land'), 'train')
    assert map[('fast', 'land')] == {'car'}
    map.remove(('fast',), 'jet')
    assert ('fast', 'air') not in map
    map.remove(('fast',))
    assert ('fast',) not in map
    try: map.remove(('fast',))
    except KeyError: pass

def discard(map, keys, value=default):
    map.discard(('fast', 'land'), 'train')
    assert map[('fast', 'land')] == {'car'}
    map.discard(('fast',), 'jet')
    assert ('fast', 'air') not in map
    map.discard(('fast',))
    assert ('fast',) not in map
    map.discard(('fast',))

def __delitem__(map, keys):
    del map[('fast', 'land')]
    assert ('fast', 'land') not in map
    del map[('fast',)]
    assert ('fast',) not in map
    try: del map[('fast',)]
    except KeyError: pass

def pop(map, key=default, value=default):
    assert map.pop(('fast', 'land'), 'car') == (('fast', 'land'), 'car')
    assert not map.has(('fast', 'land'), 'car')
    assert map.pop(('fast', 'air')) == (('fast', 'air'), 'jet')
    assert not map.has(('fast', 'air'))
    item = map.pop(('fast',))
    assert item in {(('fast',), 'rocket'), (('fast', 'land'), 'train')}
    assert not map.has(*item)

