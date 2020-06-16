
from structpy.language.unit_test.colors import colors

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
        failed_sep = ', ' if failed else ''
        failed_msg = '{} failed'.format(failed) if failed else ''
        time_fail_msg = '{} timed out'.format(time_fail) if time_fail else ''
        time_fail_sep = ', ' if time_fail_msg else ''
        return '\n{}\n{}\n\n{}{} passed{}{}{}{}{}{}{}{}{}'.format(
            title, table,
            colors.fg.green, passed, colors.fg.black, failed_sep,
            colors.fg.red, failed_msg, colors.fg.black, time_fail_sep,
            colors.fg.red, time_fail_msg, colors.fg.black)