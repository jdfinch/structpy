


def update(data, values, which=None):
    if isinstance(data, dict) and isinstance(values, dict):
        valuekeys = set(values)
        common = set(data) & valuekeys
        for key in common:
            data[key] = update(data[key], values[key], which)
        for key in set(valuekeys) - common:
            data[key] = values[key]
    elif isinstance(data, list) and hasattr(values, '__iter__'):
        pass
    elif isinstance(data, set) and hasattr(values, '__iter__'):
        pass
    else:
        return values
    return data


class Data:

    default = None
    updates = {}



if __name__ == '__main__':

    class Foo(Data):

        def __init__(self, bar=None, bat=None, baz=None):
            self.bar = bar
            self.bat = bat
            self.baz = baz

        def update(self, bar=None, bat=None, baz=None):
            self.bar.update(bar)
