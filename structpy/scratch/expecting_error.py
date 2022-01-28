
class ContextManager:

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class expecting(ContextManager):

    def __init__(self, expected_error=Exception):
        self.expected_error = expected_error

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            raise exc_type
        except self.expected_error:
            return True
        except:
            return False


if __name__ == '__main__':

    with expecting(KeyError):
        l = [1, 2, 3]
        e = l[5]
        print(e)

    print('OK!')