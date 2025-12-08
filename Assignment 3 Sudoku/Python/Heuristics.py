from Arc import Arc
from Field import Field

def heuristics_first(arcs: list[Arc], find: Field = None, first_counter: int = 0) -> list[tuple[int, Arc]] | tuple[int, Arc]:
    """
    Simple heuristic that prioritizes arcs based on the left field's number of possible values
    @param arcs: list of arcs to prioritize
    @param left: if provided, only return the next arc with this left field
    @param first_counter: the current state of the counter from the Game
    @return: (list of prioritized arcs, new_counter_value)
    """
    if find == None:
        first_counter = len(arcs) - 1
        return list(enumerate(arcs)), first_counter
    arc_list = []
    for arc in arcs:
        if arc.right == find:
            first_counter += 1
            arc_list.append((first_counter, arc))
    return arc_list, first_counter

def heuristics_somethingelse(arcs: list[Arc], find: Field = None, first_counter: int = 0) -> list[tuple[int, Arc]] | tuple[int, Arc]:
    """
    Description
    @param arcs: list of arcs to prioritize
    @param left: if provided, only return the next arc with this left field
    @param first_counter: the current state of the counter from the Game
    @return: (list of prioritized arcs, new_counter_value)
    """
    # Moet first_counter gebruiken als tiebreaker (incrementen in de code en returnen)
    return (("priority", first_counter), "arc"), first_counter