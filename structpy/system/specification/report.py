

from structpy.system.printer import Printer


class Report:

    def __init__(self, results):
        self.results = tuple(results)
        self.successful = tuple((r for r in results if r.success))
        self.failed = tuple((r for r in results if not r.success))

    @property
    def timedelta(self):
        return sum((result.timedelta for result in self.results))

    def display(self):
        printer = Printer()
        fullcolor = {**{not self.successful: 'red'}, **{not self.failed: 'green'}}.get(True)
        with printer.mode('bold', end='', fg=fullcolor):
            if self.successful:
                printer.mode('green')(len(self.successful), 'succeeded')
            if self.failed:
                if self.successful:
                    printer(', ')
                printer.mode('red')(len(self.failed), 'failed')
            printer(f' in {self.timedelta:.5f}s')

    def __iter__(self):
        return iter(self.results)

    def __len__(self):
        return len(self.results)

    def __getitem__(self, item):
        return self.results[item]

    def __str__(self):
        return f'Report({", ".join((str(r) for r in self))})'

