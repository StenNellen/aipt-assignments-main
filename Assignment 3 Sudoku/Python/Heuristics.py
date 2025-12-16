from typing import Any

from Arc import Arc
from Field import Field


def heuristics_first(arcs: list[Arc], find: Field = None, first_counter: int = 0) -> tuple[list[Any], int]:
    """
    Simple heuristic that prioritizes arcs based on the left field's number of possible values
    @param arcs: list of arcs to prioritize
    @param left: if provided, only return the next arc with this left field
    @param first_counter: the current state of the counter from the Game
    @return: (list of prioritized arcs, new_counter_value)
    """
    if not find:
        first_counter = len(arcs) - 1
        return list(enumerate(arcs)), first_counter

    arc_list = []
    for arc in arcs:
        if arc.right == find:
            first_counter += 1
            arc_list.append((first_counter, arc))
    print(arc_list, first_counter)
    return arc_list, first_counter


def heuristics_smallestdomain(arcs: list[Arc], find: Field = None, first_counter: int = 0) -> tuple[
    list[Any], int]:
    """
    Description
    @param arcs: list of arcs to prioritize
    @param left: if provided, only return the next arc with this left field
    @param first_counter: the current state of the counter from the Game
    @return: (list of prioritized arcs, new_counter_value)
    """
    arc_list = []
    sorted_arcs = sorted(arcs, key=lambda sort_arc: len(sort_arc.right.get_domain()))
    if not find:
        first_counter = len(arcs) - 1
        for arc in sorted_arcs:
            first_counter += 1
            domain_len = len(arc.right.get_domain())
            # first counter is appended as a tiebreaker, for when two items have the same domain length
            arc_list.append(((domain_len, first_counter), arc))
        return arc_list, first_counter

    for arc in sorted_arcs:
        if arc.right == find:
            first_counter += 1
            domain_len = len(arc.right.get_domain())
            arc_list.append(((domain_len, first_counter), arc))
    return arc_list, first_counter

def heuristic_finilizedfield(arcs: list[Arc], find: Field = None, first_counter: int = 0):
    high_priority_arc_list = []
    low_priority_arc_list = []

    for arc in arcs:
        if len(arc.right.get_domain()) == 1:
            high_priority_arc_list.append(arc)
        else:
            low_priority_arc_list.append(arc)
    arc_list = []
    arc_list.extend(list(enumerate(high_priority_arc_list)))
    arc_list.extend(list(enumerate(low_priority_arc_list)))
    return arc_list, first_counter
