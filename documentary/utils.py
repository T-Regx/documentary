def first(sequence: list, predicate: callable):
    for item in sequence:
        if predicate(item):
            return item
    return None
