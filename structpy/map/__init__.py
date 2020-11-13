
"""
Mapping elements between a domain and domain.
"""

from structpy.map.map import Map
from structpy.map.bijective.bimap import Bimap
from structpy.map.index.index import Index
from structpy.map.function.function import Function

from structpy.map.himap import Himap
from structpy.map.index.hiindex import Hiindex
from structpy.map.function.hifunction import Hifunction

__all__ = [
    'Map',
    'Bimap',
    'Index',
    'Function',
    'Himap',
    'Hiindex',
    'Hifunction'
]