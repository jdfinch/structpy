
class MyThing:

    def __len__(self):
        return 0

m = MyThing()

if m:
    print('Nope')
else:
    print('Yup') # Yes, __nonzero__ is auto setup from __len__