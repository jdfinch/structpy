
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

link_tmp = r'<a title="structpy.graph.undirected.unlabeled.specification.Graph" ' \
           r'href="undirected/unlabeled/specification.html#structpy.graph.undirected.unlabeled.specification.Graph">Graph</a>'
link_template = '<a title="{}" href="{}">{}</a>'

def relative_path(module, cls):
    module_directory = os.path.dirname(module.__file__)
    cls_html = sys.modules[cls.__module__].__file__.replace('.py', '.html')
    return os.path.relpath(cls_html, module_directory)


def link(obj, module, attr):
    if hasattr(obj, 'verify'):
        return '### [{}]({})'.format(attr, relative_path(module, obj))
    elif hasattr(obj, '__specifications__'):
        return '### [{}]({})'.format(attr, relative_path(module, obj))
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
                        if 'Implementation of' not in obj.__doc__:
                            implementation_string ='Implementation of ' \
                                      + ', '.join(['`{}`'.format(x.__module__ + '.' + x.__qualname__)
                                                 for x in obj.__specifications__])
                            specification_string = '\n<br>\n' + '<br>\n'.join([s.__doc__ for s in obj.__specifications__ if s.__doc__])
                            obj.__doc__ = implementation_string + specification_string + '<br>\n' + obj.__doc__
                    l = link(obj, pkg, attr)
                    d = doc_str(obj)
                    if pkg.__doc__ is None:
                        pkg.__doc__ = ''
                    pkg.__doc__ += '\n<br>\n{}\n{}\n<br>'.format(l, d)
            pkg.__pdoc__ = {x: False for x in pkg.__all__}
        pkg.__qualname__ = pkg.__name__.split('.')[-1]


from pdoc.cli import main as pdoc, parser as pdoc_parser


if __name__ == '__main__':
    print(os.getcwd())
    dynamic_docstrings(structpy)
    pdoc(pdoc_parser.parse_args('--html --force --template-dir docs/pdoc_templates --output-dir docs structpy'.split()))
    os.system('google-chrome docs/structpy/index.html')