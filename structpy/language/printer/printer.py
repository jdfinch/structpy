
import sys
from structpy.language.printer.colors import colors
from collections import deque

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

    _options = set(options.values())

    def __init__(self, indent=0, color=colors.fg.black, end='\n', file=sys.stdout, indent_size=None):
        self.settings = PrinterSettings(indent, color, end, file, indent_size)

    def set(self, *settings, bg=None):
        for setting in settings:
            if isinstance(setting, int):
                pass

    def mode(self, *settings, bg=None):
        return PrinterMode(self, *settings, bg=bg)

    def __call__(self, *args, **kwargs):
        if self.settings.color is not None:
            print(self.settings.color, end='')
        if 'end' not in kwargs:
            kwargs['end'] = self.settings.end
        print(*args, **kwargs)
        print(Printer.op.reset, end='')


class PrinterSettings:

    def __init__(self, indent=0, color=colors.fg.black, end='\n', file=sys.stdout, indent_size=None):
        self.file = file
        self.indent = indent
        if isinstance(indent_size, int):
            indent_size = Printer._indent_size
        self.indent_size = indent_size
        self.color = color
        self.end = end

    def update(self, *settings, bg=None):
        pass

    def copy(self, *settings, bg=None):
        c = PrinterSettings()
        c.update(*settings, bg=bg)
        return c


class PrinterMode:

    def __init__(self, printer, new_settings):
        self.printer = printer
        self.old_settings = printer.settings
        self.new_settings = self.old_settings.copy(new_settings)

    def __enter__(self):
        self.printer.settings = self.new_settings

    def __exit__(self):
        self.printer.settings = self.old_settings

    def __call__(self, *args, **kwargs):
        self.__enter__()
        self.printer(*args, **kwargs)
        self.__exit__()


if __name__ == '__main__':

    print = Printer()