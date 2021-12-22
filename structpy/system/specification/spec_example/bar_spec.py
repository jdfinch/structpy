
import structpy.system.specification.spec as spec


def bar():
    assert 3

def bat():
    assert False

def baz():
    for i in range(10**8):
        if i % 10**7 == 0:
            print('.', end='')


if __name__ == '__main__':

    # Verify all specs encoded by __main__ module and any submodules
    spec.verify()