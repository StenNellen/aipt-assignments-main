def shortest_conflict_set_heuristic(conflict_sets):
    """
    Heuristic: Choose the conflict set with the shortest length.
    """
    if not conflict_sets:
        return None
    return min(conflict_sets, key=len)

def longest_conflict_set_heuristic(conflict_sets):
    """
    Heuristic: Choose the conflict set with the longest length.
    """
    if not conflict_sets:
        return None
    return max(conflict_sets, key=len)

def first_conflict_set_heuristic(conflict_sets):
    """
    Heuristic: Choose the first conflict set in the list.
    """
    if not conflict_sets:
        return None
    return conflict_sets[0]