
from structpy.utilities import Symbol, fill
import sys


default = Symbol()


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
        reset = '\033[0m'
        bold = '\033[01m'
        disable = '\033[02m'
        underline = '\033[04m'
        reverse = '\033[07m'
        strikethrough = '\033[09m'
        invisible = '\033[08m'

    options = {
        'reset': op.reset,
        'bold': op.bold,
        'disable': op.disable,
        'underline': op.underline,
        'reverse': op.reverse,
        'strike': op.strikethrough,
        'strikethrough': op.strikethrough,
        'invisible': op.invisible,
    }

    _options = {
        op.reset: 'reset',
        op.bold: 'bold',
        op.disable: 'disable',
        op.underline: 'underline',
        op.reverse: 'reverse',
        op.strikethrough: 'strike',
        op.invisible: 'invisible'
    }

    def __init__(self, *args, **kwargs):
        self.settings = PrinterSettings(*args, **kwargs)

    def set(self, *args, **kwargs):
        self.settings.update(*args, **kwargs)

    def mode(self, *args, **kwargs):
        return PrinterMode(self, *args, **kwargs)

    def write(self, s):
        file = self.settings.settings.get('file', sys.stdout)
        if file is None or isinstance(file, list):
            return self(s, end='')
        else:
            with self.mode('buf'):
                return self(s)

    def flush(self):
        pass

    def __call__(self, *args, **kwargs):
        settings = self.settings.copy(**kwargs)
        sep = settings.settings.get('sep', ' ')
        end = settings.settings.get('end', '\n')
        file = settings.settings.get('file', sys.stdout)
        flush = settings.settings.get('flush', False)
        prefix = ''.join((str(o) for o in (
            settings['fg'],
            settings['bg'],
            settings['bold'],
            settings['disable'],
            settings['underline'],
            settings['reverse'],
            settings['strike'],
            settings['invisible']
        )))
        suffix = self.op.reset if prefix else ''
        indent = ' ' * (settings['indent'] if settings['indent'] else 0)
        message = sep.join((str(arg) for arg in args)) + end
        rstripped = message.rstrip()
        imessage = rstripped.replace('\n', '\n'+indent) + message[len(rstripped):]
        printed = prefix + indent + imessage + suffix
        if isinstance(file, list):
            file.append(printed)
        elif file is not None:
            _print(printed, end='', file=file, flush=flush)
        else:
            self.settings.settings['buffer'].append(printed)
        return printed

    @property
    def buffer(self):
        return self.settings.settings['buffer']

    def buffered(self):
        return ''.join(self.settings.settings['buffer'])

    @property
    def indent(self):
        return self.mode('indent')


class PrinterSettings:

    def __init__(self, *args, **kwargs):
        self.settings = {'buffer': []}
        self.update(*args, **kwargs)

    def update(self, *args, **kwargs):
        settings = self._args_to_settings(*args, **kwargs)
        self.settings.update(settings)

    def fill(self, other):
        fill(self.settings, other, default=default)

    def copy(self, *args, **kwargs):
        c = PrinterSettings()
        c.settings.update(self.settings)
        c.update(*args, **kwargs)
        return c

    def _args_to_settings(self, *args, **kwargs):
        settings = {}
        for arg in args:
            if arg in Printer.foreground_colors:
                settings['fg'] = Printer.foreground_colors[arg]
            elif arg in Printer._foreground_colors:
                settings['fg'] = arg
            elif arg in Printer.options:
                settings[Printer._options[Printer.options[arg]]] = Printer.options[arg]
            elif isinstance(arg, int):
                settings['indent'] = self.settings.get('indent', 0) + arg
            elif arg == 'i' or arg == 'indent':
                settings['indent'] = self.settings.get('indent', 0) + Printer._indent_size
            elif isinstance(arg, tuple) and len(arg) == 3:
                settings['fg'] = Printer.fg(*arg)
            elif 'un' == arg[:2] and arg[:2] in Printer.options:
                settings[Printer._options[Printer.options[arg[:2]]]] = None
            elif isinstance(arg, str) and arg.startswith('buf'):
                settings['file'] = None
        for kw, arg in kwargs.items():
            if arg is not default:
                settings[kw] = arg
        return settings

    def __getitem__(self, key):
        item = self.settings.get(key, '')
        return item if item else ''


class PrinterMode:

    def __init__(self, printer, *args, **kwargs):
        self.printer = printer
        self.old_settings = printer.settings
        self.new_settings = self.old_settings.copy(*args, **kwargs)

    def __enter__(self):
        self.printer.settings = self.new_settings

    def __exit__(self, *_, **__):
        self.printer.settings = self.old_settings

    def __call__(self, *args, **kwargs):
        self.__enter__()
        result = self.printer(*args, **kwargs)
        self.__exit__()
        return result

_print = print
print = Printer()
