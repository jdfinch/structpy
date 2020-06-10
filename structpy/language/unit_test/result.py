

from structpy.language.unit_test.colors import colors


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
        test_string = self.unit.method.__name__
        if self.obj:
            def _class_to_string(cls):
                string = str(cls)
                return string[string.rfind('.') + 1:-2]
            if hasattr(self.obj, '__specification__'):
                spec_string = _class_to_string(self.obj.__specification__)
                object_string = _class_to_string(self.obj)
                title = '{}.{} {}'.format(spec_string, object_string, test_string)
            else:
                title = '{:29} {:20.20}'.format(test_string, str(self.obj))
        else:
            title = '{:50.50}'.format(test_string)
        time = '{:.4f}'.format(self.time_elapsed).lstrip('0') if \
            self.time_requirement is not None and self.passed else ''
        time_color = colors.fg.green if self.time_passed else colors.fg.red
        passed_color = colors.fg.green if self.passed else colors.fg.red
        format = '{}{:<50}  {}{:10}{}'
        return format.format(
            passed_color,
            title,
            time_color,
            time,
            colors.fg.black
        )


class ResultList(list):

    def summary(self):
        passed = 0
        failed = 0
        run = 0
        time_fail = 0
        for result in self:
            if result.passed:
                if result.time_passed:
                    passed += 1
            else:
                failed += 1
            run += 1
            if not result.time_passed:
                time_fail += 1
        return passed, failed, run, time_fail

    def __add__(self, other):
        return ResultList(self + other)

    def __str__(self):
        title = '{s:{c}^70}'.format(s=' Unit Test Results ', c='=')
        table = '\n'.join([str(result) for result in self])
        passed, failed, run, time_fail = self.summary()
        failed_msg = '{} failed'.format(failed) if failed else ''
        time_fail_msg = '{} timed out'.format(time_fail) if time_fail else ''
        traces = '\n\n'.join([str(result) + '\n' + result.traceback
                              for result in self if not result.passed])
        return '\n{}\n{}\n\n{}\n{}{} passed{}, {}{}{}, {}{}{}'.format(
            title, table,
            traces,
            colors.fg.green, passed, colors.fg.black,
            colors.fg.red, failed_msg, colors.fg.black,
            colors.fg.red, time_fail_msg, colors.fg.black)