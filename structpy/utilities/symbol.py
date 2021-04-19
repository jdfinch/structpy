

class Symbol:

    def __init__(self, label=None):
        self.label = label

    def __str__(self):
        return f'Symbol({self.label if self.label is not None else ""}'