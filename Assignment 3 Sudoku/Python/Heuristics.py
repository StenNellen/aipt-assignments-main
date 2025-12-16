from typing import Any

from Arc import Arc
from Field import Field

def heuristic_helper(arcs, find, sorted_arcs, first_counter: int = 0) -> tuple[list[Any], int]:
    """"
    A helper function that does the repeatable code in all the heuristics
    @param arcs: list of arcs to prioritize
    @param find: if provided, only return the next arc with this right field
    @param sorted_arcs: list of arcs to prioritize
    @param first_counter: the current state of the counter from the Game
    @return: (list of prioritized arcs, new_counter_value)
    """
    arc_list = []
    if find is None:
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

def heuristics_first(arcs: list[Arc], find: Field = None, first_counter: int = 0) -> tuple[list[Any], int]:
    """
    A heuristic function that prioritizes arcs based on the order that arcs are created in.
    @param arcs: list of arcs to prioritize
    @param find: if provided, only return the next arc with this right field
    @param first_counter: the current state of the counter from the Game
    @return: (list of prioritized arcs, new_counter_value)
    """
    if find is None:
        first_counter = len(arcs) - 1
        return list(enumerate(arcs)), first_counter

    arc_list = []
    for arc in arcs:
        if arc.right == find:
            first_counter += 1
            arc_list.append((first_counter, arc))
    return arc_list, first_counter

def heuristics_smallestdomain(arcs: list[Arc], find: Field = None, first_counter: int = 0) -> tuple[
    list[Any], int]:
    """
    A heuristic function that prioritizes arcs based on the smallest length of the domain on the right side.
    @param arcs: list of arcs to prioritize
    @param find: if provided, only return the next arc with this right field
    @param first_counter: the current state of the counter from the Game
    @return: (list of prioritized arcs, new_counter_value)
    """
    sorted_arcs = sorted(arcs, key=lambda sort_arc: len(sort_arc.right.get_domain()))
    arc_list, first_counter = heuristic_helper(arcs, find, sorted_arcs, first_counter)
    return arc_list, first_counter

def heuristics_largestdomain(arcs: list[Arc], find: Field = None, first_counter: int = 0) -> tuple[
    list[Any], int]:
    """
    A heuristic function that prioritizes arcs based on the longest length of the domain on the right side.
    @param arcs: list of arcs to prioritize
    @param find: if provided, only return the next arc with this right field
    @param first_counter: the current state of the counter from the Game
    @return: (list of prioritized arcs, new_counter_value)
    """
    sorted_arcs = sorted(arcs, key=lambda sort_arc: len(sort_arc.right.get_domain()), reverse=False)
    arc_list, first_counter = heuristic_helper(arcs, find, sorted_arcs, first_counter)
    return arc_list, first_counter

def heuristic_lowestfirstdomainfield(arcs: list[Arc], find: Field = None, first_counter: int = 0):
    """
    A heuristic function that prioritizes arcs based on domain with the smallest first element.
    @param arcs: list of arcs to prioritize
    @param find: if provided, only return the next arc with this right field
    @param first_counter: the current state of the counter from the Game
    @return: (list of prioritized arcs, new_counter_value)
    """
    def sort_helper(x):
        if len(x.right.get_domain()) == 0:
            return 10
        else:
            return x.right.get_domain()[0]

    arc_list = []
    sorted_arcs = sorted(arcs, key=sort_helper)
    if find is None:
        first_counter = len(arcs) - 1
        for arc in sorted_arcs:
            first_counter += 1
            # first counter is appended as a tiebreaker, for when two items have the same domain length
            if len(arc.right.get_domain()) != 0:
                arc_list.append(((arc.right.get_domain()[0], first_counter), arc))
        return arc_list, first_counter

    for arc in sorted_arcs:
        if arc.right == find:
            first_counter += 1
            if len(arc.right.get_domain()) != 0:
                arc_list.append(((arc.right.get_domain()[0], first_counter), arc))
    return arc_list, first_counter