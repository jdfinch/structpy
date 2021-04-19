
from structpy import spec


def __init__(Printer):
    """

    """
    printer = Printer()
    return printer

def call(printer):
    """

    """
    printer('Hello world')

def mode(printer, *args, **kwargs):
    """

    """
    printer.mode('green')('Check.', end=' ')
    printer('Check.')

    with printer.mode('red'):
        printer('Problems!')
    with printer.mode(printer.fg.blue, 'i'):
        printer('Good!')
        printer('It works!')
        with printer.mode(2, (255, 100, 200)):
            printer('Even more indent!')
        printer('Back to 4.')
    with printer.mode('red', 'bold'):
        printer('Boom.')

def set(printer, *args, **kwargs):
    printer.set('bold')
    printer('Bolded!')
    printer.set('blue')
    printer('Bolded', end=' ')
    printer.set(bold=False)
    printer('blue!')


if __name__ == '__main__':
    from structpy.system.printer import Printer
    spec.verify(Printer)


