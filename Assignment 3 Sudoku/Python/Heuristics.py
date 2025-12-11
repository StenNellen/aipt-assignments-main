from Arc import Arc
from Field import Field

def has_empty_domain(arc) -> bool:
    return arc.left.value != 0

def heuristics_first(arcs: list[Arc], find: Field = None, first_counter: int = 0) -> tuple[list[tuple[int, Arc]], int] | tuple[tuple[int, Arc], int]:
    """
    Simple heuristic that prioritizes arcs based on the left field's number of possible values
    @param arcs: list of arcs to prioritize
    @param left: if provided, only return the next arc with this left field
    @param first_counter: the current state of the counter from the Game
    @return: (list of prioritized arcs, new_counter_value)
    """
    if find == None:
        res_arcs = list(filter(has_empty_domain, arcs))
        first_counter = len(res_arcs) - 1

        return list(enumerate(res_arcs)), first_counter
    arc_list = []
    for arc in arcs:
        if arc.right == find and arc.left.value != 0:
            first_counter += 1
            arc_list.append((first_counter, arc))
    return arc_list, first_counter

def heuristics_somethingelse(arcs: list[Arc], find: Field = None, first_counter: int = 0) -> tuple[list[tuple[int, Arc]], int]:
    """
    Description
    @param arcs: list of arcs to prioritize
    @param left: if provided, only return the next arc with this left field
    @param first_counter: the current state of the counter from the Game
    @return: (list of prioritized arcs, new_counter_value)
    """
    # Moet first_counter gebruiken als tiebreaker (incrementen in de code en returnen)
    if find == None:
        res_arcs: list[Arc] = list(filter(has_empty_domain, arcs))
        first_counter = len(res_arcs) - 1
        tuple_list = []
        for i in range(len(res_arcs)):
            tuple_list.append(((len(res_arcs[i].left.domain), i), res_arcs[i]))
            
        return tuple_list, first_counter
    
    arc_list = []
    priority_arcs = sorted(arcs, key=lambda arc: len(arc.left.domain))

    for arc in priority_arcs:
        if arc.right == find and arc.left.value != 0:
            first_counter += 1
            arc_list.append(((len(arc.left.domain), first_counter), arc))

    return arc_list, first_counter