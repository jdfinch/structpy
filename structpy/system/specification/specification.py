
from inspect import getmembers, isfunction

class Spec:

    specs = {}

    def __new__(cls, module):
        if module in Spec.specs:
            return Spec.specs[module]
        else:
            return super(Spec, cls).__new__(cls, module)

    def __init__(self, module):
        if module in Spec.specs:
            return
        else:
            self.module = module
            self.units = []
            lineno = lambda x: x[1].__code__.co_firstlineno
            functions = sorted(getmembers(module, isfunction), key=lineno)
            for _, function in functions:
                self.units.extend(self.add(function))
            self.implementations = []
            Spec.specs[self.module] = self

    def add(self, function):
        collected = [function]
        if hasattr(function, 'units'):
            return collected
        function.units = []
        satisfieds = getattr(function, 'satisfied', [])
        if not isinstance(satisfieds, (list, set, tuple)):
            satisfieds = [satisfieds]
        for satisfied in satisfieds:
            collected.extend(self.add(satisfied))
        lineno = lambda x: x[1].__code__.co_firstlineno
        subfunctions = sorted(getmembers(function, isfunction), key=lineno)
        for _, subfunction in subfunctions:
            function.units.append(self.add(subfunction))
        return collected

    def verify(self, *implementations):
        if implementations:
            for implementation in implementations:
                pass
        else:
            pass

    def __getattr__(self, item):
        return lambda x: None

    @property
    def name(self):
        return self.module.__name__