
from structpy.system.printer import Printer


class Result:

    def __init__(self, spec, unit, success=False, time=None, msg=None, error_msg=None):
        self.spec = spec
        self.unit = unit
        self.success = success
        self.time = time
        self.msg = msg
        self.error_msg = error_msg

    def __str__(self):
        return f'''<Test result of {self.spec}.{self.unit.__name__} 
        ({"pass" if self.success else "fail"})>
        '''
    __repr__ = __str__

    def display(self, styled=True):
        output = []
        printer = Printer(file=output, styled=styled)
        color = 'green' if self.success else 'red'
        header = f'{self.spec.name}.{self.unit.__name__}'
        printer.mode(color, 'bold')(header, end='')
        time = '  ({:10.5f} s)'.format(self.time) if self.success else ''
        printer.mode(color)(time)
        if self.msg:
            with printer.mode(2):
                printer(self.msg)
        if self.error_msg:
            printer.mode(2, 'red')(self.error_msg)
        return ''.join(output)
