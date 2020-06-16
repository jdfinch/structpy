

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
        if self.traceback:
            traceback = '\n\n{}\n\n'.format(self.traceback)
        else:
            traceback = ''
        format = '{}{:<50}  {}{:10}{}{}'
        return format.format(
            passed_color,
            title,
            time_color,
            time,
            colors.fg.black,
            traceback
        )
