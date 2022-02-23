
from structpy.spec import *


RaisesKeyError = object()


class Map:

    Keychain = ...

    def __init__(map, data=None):

        map = Map({
            'mary': {
                'breakfast': {'egg', 'donut'},
                None: 'cracker'
            },
            'jake': [
                ['cookie', 'donut'],
                'egg'
            ],
            'sam': 'egg'
        })

    @property
    def reverse(map):

        assert map.reverse == {
            'egg': {
                Map.Keychain('mary', 'breakfast'),
                Map.Keychain('jake', 1),
                Map.Keychain('sam',)
            },
            'donut': {
                Map.Keychain('mary', 'breakfast'),
                Map.Keychain('jake', 0, 1),
            },
            'cracker': {
                Map.Keychain('mary')
            },
            'cookie': {
                Map.Keychain('jake', 0, 0)
            }
        }



        return ...

    def __getitem__(map, item):
        ...

    def getitem(map, key, default=RaisesKeyError):
        ...

    def get(map, key, default=RaisesKeyError):
        ...

    def gather(map, *keychain, default=RaisesKeyError):
        ...

    def chainget(map, *keychain, default=RaisesKeyError):
        ...








