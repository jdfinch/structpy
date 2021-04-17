
def catches(expected_exception, received_exception):
    try:
        raise received_exception
    except expected_exception:
        return True
    except:
        return False