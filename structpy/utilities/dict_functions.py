
def fill(container, values, default=None):
    """
    Takes a dictionary `container` and updates it
    with dictionary `values`, but only for values that
    are `default` or don't exist in `container`.
    """
    for k, v in values:
        if k not in container or container[k] == default:
            container[k] = v
    return container