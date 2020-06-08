
from structpy.language._specification.unit import unit, Unit
from structpy.language._specification.result import ResultList


class UnitSequence(list):

    def test(self):
        obj = None
        results = ResultList()
        for unit in self:
            result = unit.test(obj)
            if result.obj is not None:
                obj = result.obj
            results.append(result)
        return results


if __name__ == '__main__':

    @unit()
    def test_one():
        assert True


    @unit(time_requirement=0.005)
    def test_two():
        i = 0
        for i in range(1000000):
            i += 1
        assert True


    @unit()
    def test_three():
        assert False


    @unit(time_requirement=1)
    def test_four():
        return [1, 2, 3]


    @unit()
    def test_five(o):
        assert o == [1, 2, 3]


    unit_sequence = UnitSequence([
        test_one, test_two, test_three, test_four, test_five
    ])

    print(unit_sequence.test())