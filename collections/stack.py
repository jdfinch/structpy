
class Stack(list, object):

    add = list.append

    def top(self):
        return list.__getitem__(-1)

    def __hash__(self):
        return id(self)
