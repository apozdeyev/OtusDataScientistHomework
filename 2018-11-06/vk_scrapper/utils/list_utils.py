def lmap(func, sequence, *sequence_1):
    """list(map(...))"""
    return list(map(func, sequence, *sequence_1))


def lflatten(list_of_list):
    """list(flatten(...))"""
    return list((x for y in list_of_list for x in y))
