
from unittest import TestSuite, TextTestRunner
from traceback import print_exc
from sys import stderr

class SpecList:

    def __init__(self, init_spec, specs):
        self.init = init_spec
        self.specs = list(specs)

    def verify(self, Implementation):
        """
        Verify that the `Implementation` satisfies all the tests in the
        spec list.
        """
        suite = TestSuite()
        specs = []
        construction_error = False
        self.init.set_object(Implementation)
        try:
            instance = self.init.run_test()
        except Exception as e:
            err_msg = """
======================================================================
SPEC INIT ERROR: {}
----------------------------------------------------------------------""".format(str(self.init))
            print(err_msg, file=stderr)
            print_exc()
            instance = None
            construction_error = True
        if not construction_error:
            msg = """
======================================================================
SPEC LIST: {}
----------------------------------------------------------------------""".format(str(self.init))
            for spec in self.specs:
                if spec.type() == 'definition':
                    spec.set_object(instance)
                    specs.append(spec)
                elif spec.type() == 'test':
                    spec.set_object(instance)
                    specs.append(spec)
                else:
                    spec.set_object(Implementation)
                    specs.append(spec)
            suite.addTests(specs)
        print('----------------------------------------------------------------------', file=stderr)
        print('\n', file=stderr)
        TextTestRunner().run(suite)
