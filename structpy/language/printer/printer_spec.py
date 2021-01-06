
from structpy import specification


@specification
class PrinterSpec:
    """

    """

    @specification.init
    def PRINTER(Printer):
        """

        """
        printer = Printer()
        return printer

    def call(printer):
        """

        """

        printer('Hello world')

    def mode(printer):
        """

        """
        printer.mode('green')('Check.', end=' ')
        printer('Check.')

        with printer.mode('red'):
            printer('Problems!')
        with printer.mode(printer.colors.blue):
            printer('Good!')
        with printer.mode('red', 'bold'):
            printer('Boom.')


    def set(printer):
        printer.set('bold')
        printer('Bolded!')
        printer.set('blue')
        printer('Bolded blue!')



