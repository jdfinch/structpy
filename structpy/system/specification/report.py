
from functools import lru_cache

from structpy.system.printer import Printer
from structpy.system.specification.result import Result


class Report:

    def __init__(self):
        self._imps = {}
        self._specs = {}
        self.log = Printer()

    def add_result(self, implementation, spec, unit, success, time, msg=None, error_msg=None):
        imps = self._imps.setdefault(implementation, {}).setdefault(spec, {})
        specs = self._specs.setdefault(spec, {}).setdefault(implementation, {})
        result = Result(spec, unit, success, time, msg, error_msg)
        imps[unit] = result
        specs[unit] = result
        return result

    @lru_cache()
    def results(self, spec=None, imp=None):
        results = {}
        if imp is not None:
            if spec is None:
                for _, d in self._imps[imp].items():
                    results.update(d)
            else:
                results.update(self._imps[imp][spec])
        elif spec is not None:
            for _, d in self._specs[spec].items():
                results.update(d)
        else:
            for _, d in self._imps.items():
                for _, e in d.items():
                    results.update(e)
        return results

    def score(self, spec=None, imp=None):
        results = self.results(spec, imp)
        total = len(results)
        correct = len(list(filter(lambda x: x.success, results.values())))
        return (correct, total)

    def time(self, spec=None, imp=None):
        results = self.results(spec, imp)
        return sum([x.time for x in results.values()])

    def __str__(self):
        correct, total = self.score()
        return f'''<Report of {len(self.results())} tests 
        ({correct}/{total} passed)>'''

    def display(self, styled=True):
        output = []
        printer = Printer(file=output)
        for spec, imps in self._specs.items():
            printer.mode('bold', 'underline')(spec.name)
            for imp, d in imps.items():
                correct, total = self.score(spec, imp)
                time = self.time(spec, imp)
                units = [unit.display(styled) for unit in d.values()]
                color = 'green' if correct == total else 'red'
                with printer.mode(2):
                    printer.mode('bold', color)(imp.__name__)
                    with printer.mode(2):
                        printer('\n'.join(units))
                    time = '{:10.5f} s'.format(time)
                    summary = f'''{spec.name}:{imp.__name__}: 
                    {correct}/{total} passed in {time}'''
                    printer.mode(color)(summary)
        correct, total = self.score()
        time = self.time()
        time = '{:10.5f} s'.format(time)
        color = 'green' if correct == total else 'red'
        printer.mode(color)(f'{correct}/{total} passed in {time}')
        return output
