def rfind(indexable, item):
    """
    Iterates through the collection in reverse order and returns the index of
    an item
    """
    length = len(indexable)
    for i in range(length - 1, -1, -1):
        if indexable[i] == item:
            return i
    return - 1
    
def empty_generator():
        return
        yield

def both(generator_one, generator_two):
    yield from generator_one
    yield from generator_two