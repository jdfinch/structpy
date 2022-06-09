
import inspect
import functools


class DefaultBinder:

    def __init__(self, f, default=None, force_namespace=False):
        self.f = f
        if inspect.isfunction(f):
            self.parameters = inspect.signature(f).parameters
        else:
            self.parameters = {
                key: inspect.Parameter(
                    key,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    default=value
                ) for key, value in f.items()
            }
        self.default = default
        self.force_namespace = force_namespace

    def arguments(self, *args, **kwargs):
        arguments = []
        kwarguments = {}
        for i, (name, param) in enumerate(self.parameters.items()):
            if param.kind is inspect.Parameter.POSITIONAL_ONLY:
                if len(args) > i:
                    arguments.append(args[i])
                elif self.force_namespace and name in kwargs:
                    arguments.append(kwargs[name])
                    del kwargs[name]
                elif param.default is inspect.Parameter.empty:
                    arguments.append(self.default)
                else:
                    arguments.append(param.default)
            elif param.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD:
                if len(args) > i:
                    kwarguments[name] = args[i]
                elif name in kwargs:
                    kwarguments[name] = kwargs[name]
                elif param.default is inspect.Parameter.empty:
                    kwarguments[name] = self.default
                else:
                    kwarguments[name] = param.default
            elif param.kind is inspect.Parameter.VAR_POSITIONAL:
                arguments.extend(args[i:])
            elif param.kind is inspect.Parameter.KEYWORD_ONLY:
                if name in kwargs:
                    kwarguments[name] = kwargs[name]
                elif param.default is inspect.Parameter.empty:
                    kwarguments[name] = self.default
                else:
                    kwarguments[name] = param.default
            elif param.kind is inspect.Parameter.VAR_KEYWORD:
                kwarguments.update(kwargs)
        return arguments, kwarguments

    def bound(self, *args, **kwargs):
        assert callable(self.f)
        arguments, kwarguments = self.arguments(*args, **kwargs)
        return functools.partial(self.f, *arguments, **kwarguments)

    def __call__(self, *args, **kwargs):
        assert callable(self.f)
        arguments, kwarguments = self.arguments(*args, **kwargs)
        return self.f(*arguments, **kwarguments)

    call = __call__
