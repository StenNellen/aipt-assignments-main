from Field import Field
from Arc import Arc
import Sudoku
from queue import PriorityQueue

class Game:

    def __init__(self, sudoku):
        self.sudoku = sudoku

    def show_sudoku(self):
        print(self.sudoku)

    def heuristics_first(self, arcs: list[Arc], left: Field = None) -> list[tuple[int, Arc]] | tuple[int, Arc]:
        if left == None:
            self.first_counter = len(arcs) - 1
            return list(enumerate(arcs))
        for arc in arcs:
            if arc.left == left:
                self.first_counter += 1
                return (self.first_counter, arc)
        return None

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
        
        # Main algorithm loop
        while True:
            # Get the next arc on the agenda
            _, arc = agenda.get()

            # TODO AC-3

            # Algorithm done if the queue (agenda) is empty
            if agenda.empty():
                break
        
        
        
        return True


    def get_constraint_arcs(self) -> list[Arc]:
        """
        Get all constraint arcs in the sudoku
        @return: list of all arcs (tuples of Fields)
        """
        grid: list[list[Field]] = self.sudoku.board
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