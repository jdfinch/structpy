
import os, sys
from types import ModuleType
from inspect import isclass, isfunction
import pkgutil
from importlib import import_module, invalidate_caches

import structpy

def is_package(module):
    return hasattr(module, '__path__')

def sub_packages(root):
    package = root
    prefix = package.__name__ + "."
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
        module = import_module(modname)
        yield module
        if ispkg:
            yield from sub_packages(module)

def doc_str(obj):
    if hasattr(obj, '__doc__') and obj.__doc__ is not None:
        doc = obj.__doc__
        return '\n'.join([line.strip() for line in doc.strip().split('\n')])
    else:
        return str(obj)

def link(obj):
    if hasattr(obj, '__verify__'):
        return '###`{}`'.format(obj.__module__ + '.' + obj.__qualname__)
    elif hasattr(obj, '__specifications__'):
        return '###`{}`'.format(obj.__module__ + '.' + obj.__qualname__)
    else:
        return '###`{}`'.format(obj.__name__.split('.')[-1])

def dynamic_docstrings(module):
    for pkg in list(sub_packages(module)):
        if hasattr(pkg, '__all__'):
            for attr, obj in pkg.__dict__.items():
                if attr in pkg.__all__:
                    if hasattr(obj, '__specifications__'):
                        if obj.__doc__ is None:
                            obj.__doc__ = ''
                        obj.__doc__ = 'Implementation of ' \
                                      + ', '.join(['`{}`'.format(x.__module__ + '.' + x.__qualname__)
                                                 for x in obj.__specifications__]) \
                                      + '\n<br/>\n' + obj.__doc__
                    l = link(obj)
                    d = doc_str(obj)
                    if pkg.__doc__ is None:
                        pkg.__doc__ = ''
                    pkg.__doc__ += '\n<br/>\n{}\n{}\n<br/>'.format(l, d)
            pkg.__pdoc__ = {x: False for x in pkg.__all__}
        pkg.__qualname__ = pkg.__name__.split('.')[-1]


from pdoc.cli import main as pdoc, parser as pdoc_parser


if __name__ == '__main__':
    print(os.getcwd())
    dynamic_docstrings(structpy)
    pdoc(pdoc_parser.parse_args('--html --force --template-dir docs/pdoc_templates --output-dir docs structpy'.split()))
    os.system('google-chrome docs/structpy/index.html')