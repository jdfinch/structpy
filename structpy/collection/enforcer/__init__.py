
"""
Enforcer collections have function hooks that allow the user
to enforce data consistency whenever the collection is updated.
"""

from structpy.collection.enforcer.enforcer_set_implementation import EnforcerSet
from structpy.collection.enforcer.enforcer_dict_implementation import EnforcerDict

__all__ = [
    'EnforcerSet',
    'EnforcerDict'
]

