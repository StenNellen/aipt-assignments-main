class Game:

    def __init__(self, sudoku):
        self.sudoku = sudoku

    def show_sudoku(self):
        print(self.sudoku)

    def solve(self) -> bool:
        """
        Implementation of the AC-3 algorithm
        @return: true if the constraints can be satisfied, false otherwise
        """
        # TODO: implement AC-3
        return True

    def valid_solution(self) -> bool:
        """
        Checks the validity of a sudoku solution
        @return: true if the sudoku solution is correct
        """
        horizontal = None
        vertical = None
        blockical = None

        #setup matrix:
        board_matrix: list[list[int]] = [[0 for _ in range(9)] for _ in range(9)]

        for i, row in enumerate(self.sudoku.board):
            for j, field in enumerate(row):
                board_matrix[i][j] = field.get_value()
        board_transposed: list[list[int]] = [list(row) for row in zip(*board_matrix)]

        blocks = []
        # block
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                blocks.append(board_matrix[i][j:j + 3] + board_matrix[i + 1][j:j + 3] + board_matrix[i + 2][j:j + 3])

        # horizontal solve
        for row in board_matrix:
            if set(row) != {1, 2, 3, 4, 5, 6, 7, 8, 9}:
                horizontal = False
                break
            horizontal = True

        #vertical solve
        for col in board_transposed:
            if set(col) != {1, 2, 3, 4, 5, 6, 7, 8, 9}:
                vertical = False
                break
            vertical = True

        #block solve
        for block in blocks:
            if set(block) != {1, 2, 3, 4, 5, 6, 7, 8, 9}:
                blockical = False
                break
            blockical = True

        if horizontal and vertical and blockical:
            return True
        return False