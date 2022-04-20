
unbound = object()


class UnitTests(list):
    """
    Collection of UnitTest objects representing a batch of tests to run against implementation code.
    """

    class factory:
        def __init__(self, f):
            self.f = f
        def __call__(self):
            return self.f()

    def __init__(self, **params):
        list.__init__(self)
        defaults = {}
        for param, default in params.items():
            if default is None:
                defaults[param] = unbound
            elif isinstance(default, UnitTests.factory):
                defaults[param] = default
            else:
                defaults[param] = lambda: default
        self.params = [{
            param: (unbound if value is None else lambda: value)
            for param, value in params.items()
        }]

    @property
    def bound_params(self):
        return self.params[-1]

    def run(self, output=False):
        results = []
        for unit in self:
            args = {k: v() for k, v in self.bound_params.items()}
            with unit.bind(**args):
                results.append(unit.run(output))

        return results

    def bind(self, **params):
        self.params.append({**self.params[-1], **params})

    def unbind(self, all=False):
        if all:
            self.params = self.params[0:1]
        elif not all and len(self.params) > 1:
            self.params.pop()