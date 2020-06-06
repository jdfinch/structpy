
import inspect
import sys
from structpy.language.specification import spec

def module_of(function):
    return sys.modules[function.__module__]

def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }

def kwargs_str(kwargs):
    r = ''
    for k, v in kwargs.items():
        r += k + '='
        if isinstance(v, str):
            r += "'{}'".format(v)
        else:
            r += str(v)
        r += ', '
    if r:
        return r[:-2]
    else:
        return r

def doc_str(doc):
    return '\n'.join([line.strip() for line in doc.strip().split('\n')])


class Factory:

    def __init__(self, factory_function, implementations=None):
        if implementations is None:
            self.name = factory_function.__name__
            self.__kwargs__ = get_default_args(factory_function)
            self.__implementations__ = factory_function()
            self.pairs = []  # (kwargs, implementation)
            for kw, production in self.implementations(self.__kwargs__):
                self.pairs.append((kw, production))
            self._update_function_docstring(factory_function)
        else:
            raise NotImplementedError

    def _update_function_docstring(self, factory_function):
        module = module_of(factory_function)
        module.__doc__ = '# {}({})\n\n{}\n\n'.format(
            factory_function.__name__, kwargs_str(self.__kwargs__), module.__doc__)
        specpairs = set()
        for kwargs, production in self.pairs:
            kwargs = dict(kwargs)
            production = production.__specification__
            if 'implementation' in kwargs:
                del kwargs['implementation']
            production.___kwargs_for_update_function_docstring = kwargs
            specpairs.add(production)
        for production in specpairs:
            kwargs = production.___kwargs_for_update_function_docstring
            if isinstance(production, Factory):
                module.__doc__ += '\n<br/>\n###`{}`\n\n`{}`\n\n{}\n\n<br/>'.format(
                    production.__module__ + '.' + production.__qualname__,
                    kwargs_str(kwargs), doc_str(production.__doc__))
            elif hasattr(production, '__implementations__'):
                module.__doc__ += '\n<br/>\n###`{}`\n\n`{}`\n\n{}\n\n<br/>'.format(
                    production.__module__ + '.' + production.__qualname__,
                    kwargs_str(kwargs), doc_str(production.__doc__))

    def implementations(self, kwargs):
        kwargs = dict(kwargs)
        for production in self.__implementations__:
            if isinstance(production, Factory):
                kwargs.update(production.__kwargs__)
                yield from production.implementations(kwargs)
            elif hasattr(production, '__implementations__'):
                kwargs.update(production.__kwargs__)
                for implementation in production.__implementations__:
                    kw = dict(kwargs)
                    kw.update(implementation.__kwargs__)
                    yield kw, implementation
            else:
                if hasattr(production.__specification__, '__kwargs__'):
                    kwargs.update(production.__specification__.__kwargs__)
                kwargs.update(production.__kwargs__)
                yield kwargs, production

    def __call__(self, **kwargs):
        kw = self.__kwargs__
        kw.update(kwargs)
        for kwargs, implementation in self.pairs:
            if kwargs == kw:
                return implementation
        raise ValueError('Factory {} got unexpected setting signature {}'.format(self.name, kw))

