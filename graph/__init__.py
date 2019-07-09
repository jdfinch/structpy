"""
General Purpose Graph Framework
---

"""

import structpy.graph
from structpy.graph.core.graph import Graph
from structpy.graph.core.dag import Dag
from structpy.graph.core.tree import Tree
from structpy.graph.core.sequence import Sequence
from structpy.graph.dictionary_graph import DictionaryGraph
from structpy.graph.list_graph import ListGraph
from structpy.graph.list_tree import ListTree
from structpy.graph.bidictionary_graph import BidictionaryGraph
from structpy.graph.bidictionary_tree import BidictionaryTree
from structpy.graph.frontiers.queue import Queue
from structpy.graph.frontiers.stack import Stack
from structpy.graph.pointer_graph import PointerGraph
from structpy.graph.pointer_tree import PointerTree
from structpy.graph.array_sequence import ArraySequence

from structpy.graph.flex.flex_graph import FlexGraph
from structpy.graph.flex.flex_tree import FlexTree
from structpy.graph.point_map.map_point_graph import MapPointGraph