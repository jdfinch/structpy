

class Spec(type):

    def __new__(cls, name, bases, fields):
        return super().__new__(cls, name, bases, fields)



