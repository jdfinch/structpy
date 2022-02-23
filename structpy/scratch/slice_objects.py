
class MySlicer:

    def __getitem__(self, item):
        if hasattr(item, '__iter__'):
            for e in item:
                print('   ', e)
        return item


s = MySlicer()
print(s[0])
print(s['hello'])
print(s[0, 1, 2])
print(s[(0, 1, 2)])
print(s[[0, 1, 2]])
print(s[0:2])
print(s[0:2:1])
print(s[0:2, 1:3, 0:4, 2:4])
print()