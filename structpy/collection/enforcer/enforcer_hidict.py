
from structpy import implementation
from structpy.collection.enforcer.enforcer_hidict_spec import EnforcerHidictSpec

from structpy.collection.enforcer.enforcer_dict import EnforcerDict
from structpy.collection.hidict import Hidict

from functools import reduce


# @implementation(HidictSpec)
# class Hidict(EnforcerDict):
#
#     def __init__(self, dict_like=None, add_function=None, remove_function=None, order=1):
#         assert order >= 1
#         self.order = order
#         EnforcerDict.__init__(self, dict_like, add_function, remove_function)
#
#     def __getitem__(self, items):
#         return EnforcerDict.__getitem__(self, items[0]).__getitem__(items[1:])
#
#     def __setitem__(self, keys, value):
#         if self.order == 1:
#             key = keys[0]
#             keyprime = keys[1]
#             if key not in self:
#                 EnforcerDict.__setitem__(self, key, {})
#             EnforcerDict.__getitem__(self, key)[keyprime] = value



class EnforcerHidict(EnforcerDict, Hidict):
    pass