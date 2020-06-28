
"""
Defines graphs.

"""

note = """
```text
Directed
Undirected

Labeled Directed
Labeled Undirected

Mapping options:
- map (many to many)
- function (many to one)

MultiLabeledDigraph
source, target - label : map
source, label - target : map
target, label - source : map

LabeledDigraph
source, target - label : function
source, label - target : map
target, label - source : map

ForwardLabeledDigraph
source, target - label : function
source, label - target : function
target, label - source : map

BackwardLabeledDigraph
source, target - label : function
source, label - target : map
target, label - source : function

PerfectLabeledDigraph
source, target - label : function
source, label - target : function
target, label - source : function
```"""

from structpy.graph.undirected.unlabeled.undigraph_spec import UndigraphSpec
from structpy.graph.undirected.unlabeled.undigraph_type_spec import UndigraphTypeSpec

__all__ = [
    'UndigraphSpec',
    'UndigraphTypeSpec'
]