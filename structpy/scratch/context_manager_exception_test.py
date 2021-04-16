

ls = []

class Em:

    def __enter__(self):
        ls.append('(')

    def __exit__(self, exc_type, exc_val, exc_tb):
        ls.append(')')


if __name__ == '__main__':

    with Em() as _:
        try:
            with Em() as _:
                print('Before exception:')
                print(ls)
                raise Exception()
                print('Nope')
        except Exception:
            print('Exception triggered!')
            print(ls)

    print(ls)