
import sys

from structpy.system.dclass import Dclass

pythonprint = print
default = object()


__all__ = [
    'Printer',
    'print',
    'pythonprint',
    'Capture'
]


class Printer:

    _indent_size = 4

    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        gray='\033[37m'
        darkgray='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'

        def __init__(self, r, g, b):
            self.rgb = (r, g, b)

        def __str__(self):
            r, g, b = self.rgb
            return f'\033[38;2;{r};{g};{b}m'

    foreground_colors = {
        'black': fg.black,
        'red': fg.red,
        'green': fg.green,
        'orange': fg.orange,
        'blue': fg.blue,
        'purple': fg.purple,
        'cyan': fg.cyan,
        'gray': fg.gray,
        'grey': fg.gray,
        'lightgrey': fg.gray,
        'lightgray': fg.gray,
        'darkgray': fg.darkgray,
        'darkgrey': fg.darkgray,
        'lightred': fg.lightred,
        'lightgreen': fg.lightgreen,
        'lightblue': fg.lightblue,
        'lightcyan': fg.lightcyan,
        'yellow': fg.yellow,
        'pink': fg.pink
    }

    _foreground_colors = set(foreground_colors.values())

    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        gray='\033[47m'

        def __init__(self, r, g, b):
            self.rgb = (r, g, b)

        def __str__(self):
            r, g, b = self.rgb
            return f'\033[48;2;{r};{g};{b}m'

    background_colors = {
        'black': bg.black,
        'red': bg.red,
        'green': bg.green,
        'orange': bg.orange,
        'blue': bg.blue,
        'purple': bg.purple,
        'cyan': bg.cyan,
        'grey': bg.gray,
        'gray': bg.gray,
        'lightgrey': bg.gray,
        'lightgray': bg.gray
    }

    _background_colors = set(background_colors.values())

    class op:
        bold = '\033[01m'
        disable = '\033[02m'
        underline = '\033[04m'
        reverse = '\033[07m'
        strike = '\033[09m'
        invisible = '\033[08m'

    options = {
        'bold': op.bold,
        'disable': op.disable,
        'underline': op.underline,
        'reverse': op.reverse,
        'strike': op.strike,
        'invisible': op.invisible,
    }

    _options = {
        op.bold: 'bold',
        op.disable: 'disable',
        op.underline: 'underline',
        op.reverse: 'reverse',
        op.strike: 'strike',
        op.invisible: 'invisible'
    }

    reset = '\033[0m'


    def __init__(self, *args, **kwargs):
        self.settings = PrinterSettings(*args, **kwargs)

    def set(self, *args, **kwargs):
        self.settings.set(*args, **kwargs)

    def mode(self, *args, **kwargs):
        return PrinterMode(self, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        settings = self.settings.copy(**kwargs)
        if settings.record and not isinstance(settings.record, list):
            settings.record = []
            self.settings.record = settings.record
        if settings.styled:
            prefix = f'{str(settings.fg) if settings.fg else ""}'               \
                     f'{str(settings.bg) if settings.bg else ""}'               \
                     f'{Printer.op.bold if settings.bold else ""}'              \
                     f'{Printer.op.disable if settings.disable else ""}'        \
                     f'{Printer.op.underline if settings.underline else ""}'    \
                     f'{Printer.op.reverse if settings.reverse else ""}'        \
                     f'{Printer.op.strike if settings.strike else ""}'          \
                     f'{Printer.op.invisible if settings.invisible else ""}'
        else:
            prefix = ''
        suffix = Printer.reset if prefix else ''
        message = settings.sep.join((str(arg) for arg in args)) + settings.end
        indent = ' ' * settings.indent
        stripped_message = message.rstrip()
        rstripped = message[len(stripped_message):]
        message = stripped_message.replace('\n', '\n' + indent)
        padding = indent if self.settings._prev_out.endswith('\n') else ''
        printed = prefix + padding + message + suffix + rstripped
        if isinstance(settings.record, list):
            settings.record.append(printed)
        if settings.file is not None:
            pythonprint(printed, end='', file=settings.file, flush=settings.flush)
        self.settings._prev_out = printed
        return printed

    def write(self, s):
        self(s, end='')

    def flush(self):
        pass

    def capturing_stdin(self, silence=False, **kwargs):
        return Capture(self, capture_stdin=True, record=True,
                       file=(None if silence else self.settings.file), **kwargs)

    def capturing_stdout(self, silence=False, **kwargs):
        return Capture(self, capture_stdout=True, record=True,
                       file=(None if silence else self.settings.file), **kwargs)

    def capturing_stderr(self, silence=False, **kwargs):
        return Capture(self, capture_stderr=True, record=True,
                       file=(None if silence else self.settings.file), **kwargs)

    @property
    def records(self):
        return self.settings.record

    @property
    def record(self):
        return ''.join(self.settings.record)


class PrinterSettings(Dclass):

    def __init__(self, *args, **kwargs):
        self.fg = None
        self.bg = None
        self.indent = 0
        self.bold = False
        self.disable = False
        self.underline = False
        self.reverse = False
        self.strike = False
        self.invisible = False
        self.sep = ' '
        self.end = '\n'
        self.flush = False
        self.styled = True
        self.file = sys.stdout
        self.record = None
        self.capture = False
        self._prev_out = '\n'
        Dclass.__init__(self)
        if len(args) == 1 and isinstance(args[0], (PrinterSettings, Printer)):
            if isinstance(args[0], Printer):
                other = args[0].settings
            else:
                other = args[0]
            self(**other())
        else:
            self.set(*args, **kwargs)

    def set(self, *args, **kwargs):
        for arg in args:
            if arg in Printer.foreground_colors:
                self.fg = Printer.foreground_colors[arg]
            elif arg in Printer._foreground_colors or isinstance(arg, Printer.fg):
                self.fg = arg
            elif arg in Printer._background_colors or isinstance(arg, Printer.bg):
                self.bg = arg
            elif arg in Printer.options:
                self[arg] = True
            elif arg in Printer._options:
                arg = Printer._options[arg]
                self[arg] = True
            elif isinstance(arg, str) and arg.startswith('un') and arg[2:] in Printer.options:
                self[arg[2:]] = False
            elif isinstance(arg, int):
                self.indent = arg
            elif isinstance(arg, str) and arg and 'indent'.startswith(arg):
                self.indent += Printer._indent_size
            elif isinstance(arg, tuple) and len(arg) == 3:
                self.fg = Printer.fg(*arg)
        for kw, arg in kwargs.items():
            if arg is not default and (kw in self() or kw in {'op', 'ops'}):
                if kw == 'fg' and arg in Printer.foreground_colors:
                    arg = Printer.foreground_colors[arg]
                elif kw == 'bg' and arg in Printer.background_colors:
                    arg = Printer.background_colors[arg]
                elif kw == 'op' and arg in Printer.options:
                    kw = arg
                    arg = True
                elif kw == 'ops' and isinstance(arg, (set, list, tuple)):
                    for a in arg:
                        if a in Printer.options:
                            kw = a
                            arg = True
                            self[kw] = arg
                    continue
                elif kw in {'op', 'ops'} and arg is None:
                    for op in Printer.options:
                        self[op] = False
                    continue
                elif 'indent'.startswith(kw):
                    kw = 'indent'
                    if not isinstance(arg, (int, float)):
                        if arg:
                            arg = self.indent + Printer._indent_size
                        else:
                            arg = 0
                    else:
                        arg = int(arg)
                self[kw] = arg

    def copy(self, *args, **kwargs):
        c = PrinterSettings()
        c(**self())
        c.set(*args, **kwargs)
        return c


class PrinterMode(Printer):

    def __init__(self, printer, *args, **kwargs):
        self.old_settings = printer.settings
        self.printer = printer
        Printer.__init__(self)
        self.settings = printer.settings.copy(*args, **kwargs)

    def __enter__(self):
        self.printer.settings = self.settings
        return self

    def __exit__(self, *_, **__):
        self.printer.settings = self.old_settings


class Capture:

    def __init__(self, f,
                 capture_stdin=True,
                 capture_stdout=True,
                 capture_stderr=False,
                 **kwargs):
        self.file = f
        self.cap_stdin = capture_stdin
        self.cap_stdout = capture_stdout
        self.cap_stderr = capture_stderr
        self.stdin = None
        self.stdout = None
        self.stderr = None
        if self.cap_stderr:
            self.stderr = sys.stderr
            sys.stderr = self.file
        if self.cap_stdout:
            self.stdout = sys.stdout
            sys.stdout = self.file
        if self.cap_stdin:
            self.stdin = sys.stdin
            sys.stdin = self.file
        if isinstance(self.file, Printer):
            self.file = self.file.mode(**kwargs)

    def __enter__(self):
        if isinstance(self.file, Printer):
            return self.file.__enter__()
        return self.file

    def __exit__(self, *_, **__):
        if self.cap_stderr:
            sys.stderr = self.stderr
        if self.cap_stdout:
            sys.stdout = self.stdout
        if self.cap_stdin:
            sys.stdin = self.stdin
        if isinstance(self.file, Printer):
            self.file.__exit__()

    stop = __exit__


print = Printer()


if __name__ == '__main__':

    print('hello world')
    print.mode('red')('hell world')
    print.mode('green')('high world')
    print('regular world')

    with print.mode(indent=4) as p:
        p('this is a test')
        p('am i in here?')
        p('this is a test')
    print('-' * 20, '\n')

    print('capture test', ops=('bold', 'underline'))
    with print.capturing_stdout(silence=False, indent=2) as cap:
        pythonprint('x', 'y', 'z')
        pythonprint('this is captured')
    print()
    print('Captured record:', underline=True)
    print(repr(cap.record))
    print(len(cap.record))
    print(len('  x y z\n  this is captured\n'))