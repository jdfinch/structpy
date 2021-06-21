from structpy.system.interface_implementation import I
import structpy.system.specification.spec as spec
from structpy.system.printer import print, Printer

from structpy.utilities.symbol import Symbol as _Symbol
default = _Symbol('default argument')

__all__ = [
    'spec',
    'print',
    'Printer',
    'default',
    'I'
]