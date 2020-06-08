


class Result:

    def __init__(self):
        self.unit = None
        self.passed = None
        self.time_requirement = None
        self.time_elapsed = None
        self.time_passed = None
        self.traceback = None
        self.obj = None

    def __str__(self):
        return 'placeholder for test result'


class ResultList(list):

    def __add__(self, other):
        return ResultList(self + other)

    def __str__(self):
        return '\n'.join([str(result) for result in self])