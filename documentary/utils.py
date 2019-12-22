def first(sequence: list, predicate: callable):
    for item in sequence:
        if predicate(item):
            return item
    return None


def interlace(parts: list, value) -> list:
    if len(parts) <= 1:
        return parts
    values = [(value, x) for x in parts]
    return [x for value in values for x in value][1:]
