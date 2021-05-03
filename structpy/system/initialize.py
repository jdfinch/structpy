
from inspect import signature, Parameter

positional = {Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD, Parameter.VAR_POSITIONAL}
variable = {Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD}


def initialize(*params, exclude=None):
    if len(params) == 1 and callable(params[0]):
        init = params[0]
        exclude = lambda x: False
    else:
        init = None
        if exclude:
            exclusions = set(exclude.pop('exclude'))
            exclude = lambda x: x in exclusions
        elif params:
            inclusions = set(params)
            exclude = lambda x: x not in inclusions
        else:
            exclude = lambda x: False
    def decorator(__init__):
        sig = signature(__init__)
        def decorated(self, *args, **kwargs):
            parameters = [(k, v) for k, v in sig.parameters.items()][1:]
            bound_args = []
            unbound_args = []
            for i, arg in enumerate(args):
                if len(parameters) > i and parameters[i][1].kind in positional:
                    bound_args.append(arg)
                else:
                    unbound_args.append(arg)
            bound_kwargs = {}
            unbound_kwargs = {}
            for kw, arg in kwargs.items():
                if kw in sig.parameters and sig.parameters[kw].kind not in variable:
                    bound_kwargs[kw] = arg
                else:
                    unbound_kwargs[kw] = arg
            if any([param[1].kind is Parameter.VAR_POSITIONAL for param in parameters]):
                bound_args.extend(unbound_args)
            if any([param[1].kind is Parameter.VAR_KEYWORD for param in parameters]):
                bound_kwargs.update(unbound_kwargs)
            cls_attrs = set(self.__dict__.keys())
            actual_bound_args = sig.bind(self, *bound_args, **bound_kwargs)
            actual_bound_args.apply_defaults()
            actual_bound_args = actual_bound_args.arguments
            __init__(self, *bound_args, **bound_kwargs)
            attrs = [k for k in self.__dict__.keys() if k not in cls_attrs and not exclude(k)]
            attr_default_fns = {}
            attr_construct_fns = {}
            for attr in attrs:
                default_fn_name = '_'+attr
                if hasattr(self, default_fn_name) and callable(getattr(self, default_fn_name)):
                    fn = getattr(self, default_fn_name)
                    fn_params = signature(fn).parameters
                    if len(fn_params) == 0:
                        attr_default_fns[attr] = fn
                    elif len(fn_params) == 1 and attr in fn_params:
                        attr_construct_fns[attr] = fn
                        if fn_params[attr].default is not Parameter.empty:
                            attr_default_fns[attr] = fn
            required_binding = {k: actual_bound_args[k] for k in actual_bound_args if k in attrs or '_'+k in attrs}
            binding = dict(required_binding)
            i = 0
            for arg in unbound_args:
                attr = attrs[i]
                while attr in sig.parameters or '_'+attr in sig.parameters:
                    i += 1
                    attr = attrs[i]
                binding[attr] = arg
                i += 1
            binding.update(unbound_kwargs)
            for param, arg in binding.items():
                if param in attr_construct_fns:
                    value = attr_construct_fns[param](arg)
                    if value is not None:
                        setattr(self, param, value)
                elif param not in required_binding:
                    setattr(self, param, arg)
            for param in set(attr_default_fns) - set(binding):
                value = attr_default_fns[param]()
                if value is not None:
                    setattr(self, param, value)
        return decorated
    return decorator(init) if init else decorator


if __name__ == '__main__':

    def print_obj(obj):
        print({k: v for k, v in obj.__dict__.items() if not callable(v)})

    class Car:

        @initialize
        def __init__(self):
            self.cost = '$10'
            self.make = 'honda'
            self.model = []
            self.year = 2000


    car = Car('$20', year=3000)
    print_obj(car)

