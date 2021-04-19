from structpy.system.interface_implementation import I
from structpy.system.spec import spec
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