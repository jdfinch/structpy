
"""
Enforcer collections have function hooks that allow the user
to enforce data consistency whenever the collection is updated.
"""

from structpy.collection.enforcer.enforcer_set import EnforcerSet
from structpy.collection.enforcer.enforcer_dict import EnforcerDict

__all__ = [
    'EnforcerSet',
    'EnforcerDict'
]

