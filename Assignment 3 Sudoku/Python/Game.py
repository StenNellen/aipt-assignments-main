from Field import Field
from Arc import Arc
import Sudoku
from queue import PriorityQueue
from copy import deepcopy

class Game:

    def __init__(self, sudoku):
        self.sudoku: Sudoku = sudoku

    def show_sudoku(self):
        print(self.sudoku)

    def heuristics_first(self, arcs: list[Arc], find: Field = None) -> list[tuple[int, Arc]] | tuple[int, Arc]:
        """
        Simple heuristic that prioritizes arcs based on the left field's number of possible values
        @param arcs: list of arcs to prioritize
        @param left: if provided, only return the next arc with this left field
        @return: list of prioritized arcs or the next arc with the given left field
        """
        if find == None:
            self.first_counter = len(arcs) - 1
            return list(enumerate(arcs))
        arc_list = []
        for arc in arcs:
            if arc.right == find:
                self.first_counter += 1
                arc_list.append((self.first_counter, arc))
        return arc_list

    def solve(self, heuristic: callable = None) -> bool:
        """
        Implementation of the AC-3 algorithm
        @return: true if the constraints can be satisfied, false otherwise
        """
        # Default heuristic
        if heuristic == None: heuristic = self.heuristics_first

        # Define empty queue
        agenda = PriorityQueue()

        # Get all arcs and fill the agenda
        arcs: list[Arc] = self.get_constraint_arcs()
        priority_arc_items = heuristic(arcs)
        for arc in priority_arc_items:
            agenda.put(arc)
        
        # Main algorithm loop is done if the queue (agenda) is empty
        while not agenda.empty():
            # Get the next arc on the agenda
            _, arc = agenda.get()
            left_value = arc.left.get_value()
            right_value = arc.right.get_value()

            # Check if it is necessary
            if left_value == 0:

                # Check if right has a value
                if right_value > 0:

                    # Prune left
                    revised = None
                    try:
                        before_len = arc.left.get_domain_size()
                        arc.left.remove_from_domain(right_value)
                        revised = before_len > arc.left.get_domain_size()
                    except: pass

                    # Add left back to the agenda through every right-side arc if it was pruned
                    if revised:
                        for new_arc in heuristic(arcs, arc.left):
                            if not any(new_arc[1] == right for _, right in agenda.queue):
                                agenda.put(new_arc)

            # Fail if both sides have the same value
            elif left_value == right_value:
                return False

        return True

    def get_constraint_arcs(self) -> list[Arc]:
        """
        Get all constraint arcs in the sudoku
        @return: list of all arcs (tuples of Fields)
        """
        grid: list[list[Field]] = self.sudoku.get_board()
        arcs: list[Arc] = []

        for row in grid:
            for field in row:
                for neighbour in field.neighbours:
                    neighbour: Field
                    arcs.append(Arc(field, neighbour))
        return arcs

    def valid_solution(self) -> bool:
        """
        Checks the validity of a sudoku solution
        @return: true if the sudoku solution is correct
        """
        grid: list[list[Field]] = self.sudoku.board

        for row in grid:
            for field in row:
                if not field.is_finalized():
                    return False
                for neighbour in field.neighbours:
                    if field.value == neighbour.value:
                        return False
                
        return True

class BacktrackingGame(Game):

    def __init__(self, sudoku):
        super().__init__(sudoku)
    
    def get_smallest_domain(self) -> Field:
        fields = []
        for row in self.sudoku.get_board():
            fields.extend([field for field in row])
        filtered_fields = [field for field in fields if len(field.get_domain()) > 1]
        return min(filtered_fields, key=lambda x:len(x.get_domain()))                    

    
    def solve(self, heuristic = None):
        """
        Backtracking implementation of the AC-3 algorithm
        @return: true if the constraints can be satisfied, false otherwise
        """
        if not super().solve():
            return False

        # Check if valid solution was found deterministically
        if self.valid_solution():
            return True
        
        field = self.get_smallest_domain()
            
        # Try every value for the field (DFS)
        for j in range(len(field.get_domain())):

            # Retrieve the chosen value
            field = self.get_smallest_domain()
            value = field.get_domain()[j]

            # Save a copy
            save_state = deepcopy(self.sudoku)
            field.set_value(value)
            field.domain = [value]

            # Attempt to solve the branch
            self.solve()
            
            # Recursively solve and check if solved
            if self.valid_solution():
                return True
            
            # Otherwise revert to current state
            else:
                self.sudoku = save_state
                
        # No solution found
        return False
    