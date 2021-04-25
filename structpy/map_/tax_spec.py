"""
Taxonomy.
"""

from structpy import spec
from structpy.system import default


def __init__(Tax, hierarchy):
    pass

def __contains__(tax, value):
    pass

def has(tax, tag, value=default):
    pass

def has_tax(tax, hierarcy):
    pass

def __ge__(tax, hierarchy):
    pass

def __getitem__(tax, value):
    pass

def __iter__(tax):
    pass

def __len__(tax):
    pass

def len_tags(tax):
    pass

def len_items(tax):
    pass

def values(tax, *tags):
    pass

def tags(tax, *values):
    pass

def supertags(tax, *tags):
    pass

def __setitem__(tax, value, tags):
    pass

def add(tax, value, *tags):
    pass

def update(tax, items):
    pass

def remove(tax, value, *tags):
    pass

def discard(tax, value, *tags):
    pass

def replace(tax, old, new):
    pass

def replace_tag(tax, old, new):
    pass





