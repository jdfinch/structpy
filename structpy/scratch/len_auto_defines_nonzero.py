
class MyCollection:

    def __init__(self, true):
        self.true = true

    def __len__(self):
        return int(self.true)


if __name__ == '__main__':
    mc = MyCollection(True)
    print(bool(mc))