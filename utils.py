def first(sequence: list, predicate):
    for item in sequence:
        if predicate(item):
            return item
    return None
