

class UnitSequence:

    def __init__(self, units):
        self.units = list(units)

    def test(self):
        obj = None
        results = []
        for unit in self.units:
            result = unit.test(obj)
            if result.obj is not None:
                obj = result.obj
            results.append(result)


