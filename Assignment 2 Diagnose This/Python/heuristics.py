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

def middle_set_heuristic(conflict_sets):
    """
    Heuristic: Choose the middle conflict set in the list.
    """
    if not conflict_sets:
        return None
    return conflict_sets[round((len(conflict_sets)-1)/2)]

def most_common_set_heuristic(conflict_sets):
    """
    Heuristic: Choose the conflict set with the most common element in the conflict sets.
    """
    counter = {}
    for setthing in conflict_sets:
        for item in setthing:
            counter[item] = counter.get(item, 0) + 1
    

    sorted_dict = dict(sorted(counter.items(), key=lambda item: item[1], reverse=True))
    for setthingy in conflict_sets:
        if list(sorted_dict.keys())[0] in setthingy:
            return setthingy
