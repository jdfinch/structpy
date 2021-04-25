"""

"""

from structpy import spec
from structpy.system import default


def __init__(Digraph):
    pass

def has(graph, node=default, target=default, label=default):
    pass

def len_nodes(graph):
    pass

def len_edges(graph):
    pass

def __contains__(graph, node):
    pass

def __iter__(graph):
    pass

def __len__(graph):
    pass

def nodes(graph, source=default, target=default, label=default, neighbor=default):
    pass

def edges(graph, source=default, target=default, label=default):
    pass

def sources(graph, node, label=default):
    pass

def targets(graph, node, label=default):
    pass

def add(graph, node, source=default, target=default):
    pass

def update(graph, edges):
    pass

def remove(graph, node, source=default, target=default):
    pass

def discard(graph, node, source=default, target=default):
    pass

def replace_node(graph, old, new):
    pass

def replace_label(graph, source, target, new):
    pass