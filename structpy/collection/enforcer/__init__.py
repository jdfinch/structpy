
"""
Enforcer collections have function hooks that allow the user
to enforce data consistency whenever the collection is updated.
"""

from structpy.collection.enforcer.enforcer_set import EnforcerSet
from structpy.collection.enforcer.enforcer_dict import EnforcerDict
from structpy.collection.enforcer.enforcer_hidict import EnforcerHidict
from structpy.collection.enforcer.enforcer_hidir import EnforcerHidir

__all__ = [
    'EnforcerSet',
    'EnforcerDict',
    'EnforcerHidict',
    'EnforcerHidir'
]

