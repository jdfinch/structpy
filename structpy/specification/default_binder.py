
import inspect
import functools


class DefaultBinder:

    def __init__(self, f, default=None, force_namespace=False):
        self.f = f
        if inspect.isfunction(f):
            self.parameters = inspect.signature(f)
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

    def __call__(self, *args, **kwargs):
        arguments = []
        kwarguments = {}
        for i, (name, param) in enumerate(self.parameters.items()):
            if param.kind is inspect.Parameter.POSITIONAL_ONLY:
                if len(args) > i:
                    arguments.append(args[i])
                elif self.force_namespace and name in kwargs:
                    arguments.append(kwargs[name])
                    del kwargs[name]
                else:
                    arguments.append(self.default)
            elif param.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD:
                if len(args) > i:
                    kwarguments[name] = args[i]
                elif name in kwargs:
                    kwarguments[name] = kwargs[name]
                else:
                    kwarguments[name] = self.default
            elif param.kind is inspect.Parameter.VAR_POSITIONAL:
                arguments.extend(args[i:])
            elif param.kind is inspect.Parameter.KEYWORD_ONLY:
                if name in kwargs:
                    kwarguments[name] = kwargs[name]
                else:
                    kwarguments[name] = self.default
            elif param.kind is inspect.Parameter.VAR_KEYWORD:
                kwarguments.update(kwargs)
        return arguments, kwarguments

    bind = __call__
