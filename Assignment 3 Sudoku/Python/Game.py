from Field import Field
from Arc import Arc
import heapq
import Sudoku

class Game:

    def __init__(self, sudoku):
        self.sudoku = sudoku

    def show_sudoku(self):
        print(self.sudoku)

    @staticmethod
    def heuristics_first(arcs: list[Arc], left: Field) -> tuple[int, Arc]:
        for i in range(0, len(arcs), -1):
            if arcs[i].left == left:
                return (i, arcs[i])
        return None

    def solve(self, heuristic: callable = heuristics_first) -> bool:
        """
        Implementation of the AC-3 algorithm
        @return: true if the constraints can be satisfied, false otherwise
        """

        arcs: list[Arc] = self.get_constraint_arcs()
        arced_agenda = arcs.copy()
        agenda = []
        for arc in arcs:
            prior = heuristic(arced_agenda, arc.left)
            arced_agenda.remove(prior[1])
            agenda.append(prior)
        
        print(agenda)
        
        
        
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
        return

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


if __name__ == "__main__":
    gam = Game(Sudoku(sudoku_file))
    arcs = gam.get_constraint_arcs()
    print(arcs)
    gam.solve()