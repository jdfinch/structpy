def rfind(indexable, item):
    """
    Iterates through the collection in reverse order and returns the index of
    an item
    """
    length = len(indexable)
    for i in range(length - 1, -1, -1):
        if indexable[i] == item:
            return i
    return -1