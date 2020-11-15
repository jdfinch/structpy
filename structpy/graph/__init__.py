
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
target, target - label : map
target, label - target : map
target, label - target : map

LabeledDigraph
target, target - label : function
target, label - target : map
target, label - target : map

ForwardLabeledDigraph
target, target - label : function
target, label - target : function
target, label - target : map

BackwardLabeledDigraph
target, target - label : function
target, label - target : map
target, label - target : function

PerfectLabeledDigraph
target, target - label : function
target, label - target : function
target, label - target : function
```"""


__all__ = [

]