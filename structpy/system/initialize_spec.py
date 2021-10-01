
from structpy import specxxx
from structpy.system.initialize import initialize


def auto_params(initialize):
    class Car:
        @initialize
        def __init__(self):
            self.make = None
            self.model = None
    car = Car()
    assert (car.make, car.model) == (None, None)
    car = Car('ford')
    assert (car.make, car.model) == ('ford', None)
    car = Car(model='mustang')
    assert (car.make, car.model) == (None, 'mustang')
    car = Car('ford', 'mustang')
    assert (car.make, car.model) == ('ford', 'mustang')


if __name__ == '__main__':
    specxxx.verify(initialize)