
from inspect import signature
from copy import deepcopy

from structpy.system.specification.test_list import TestList, Report, Printer, capture_stdout


class Spec(TestList):

    def __init__(self, *units, imps=None):
        TestList.__init__(self, *units)
        self.imps = imps

    def __setitem__(self, index, unit):
        unit = TestList.__setitem__(self, index, unit)
        if unit.name.startswith('__') and not unit.name.endswith('__'):
            unit.subunit = True

    def run(self, *imps, output=True, condition=None):
        if not imps:
            imps = self.imps
        if imps:
            for imp in imps:
                imp_param_name = None
                generated_object = [None, None]
                condition = self._condition(condition)
                results = []
                printer = Printer('bold')
                goi = 0 # generated object index
                for unit in self:
                    if condition(unit):
                        if unit.subunit:
                            if goi == 0:
                                copy_object = generated_object[0]
                                generated_object[1] = deepcopy(copy_object)
                            goi = 1
                        else:
                            if goi == 1:
                                generated_object[1] = None
                            goi = 0
                        params = signature(unit.function).parameters
                        param0 = None
                        if params:
                            param0 = next(iter(params))
                            if imp_param_name is None:
                                imp_param_name = param0
                            if param0 == imp_param_name:
                                unit.try_bind_default(imp)
                            elif generated_object[goi] is not None:
                                unit.try_bind_default(generated_object[goi])
                        if output:
                            printer(f'{unit.name}:')
                        stdout_cap = capture_stdout(silence=not output, indent=True)
                        with stdout_cap:
                            result = unit.run(output=output)
                            results.append(result)
                        if param0 and param0 == imp_param_name and result.result is not None:
                            generated_object[goi] = result.result
                        if output:
                            printer()
                report = Report(results)
                if output:
                    report.display()
                return report
        else:
            with self.bind():
                TestList.run(self, output=output, condition=condition)



if __name__ == '__main__':


    def foo(List, blah):
        ls = List((1, 2, 3))
        return ls

    def bar(l):
        print(l)
        assert sum(l) == 6

    def __bat(l):
        l.append(4)
        print(l)
        assert sum(l) == 10

    def baz(l):
        l.append(5)
        print(l)
        assert sum(l) == 11


    spec = Spec(foo, bar, __bat, baz)
    spec.run(list)














