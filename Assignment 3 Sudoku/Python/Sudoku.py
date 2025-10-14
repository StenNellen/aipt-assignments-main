from Field import Field


class Sudoku:

    def __init__(self, filename):
        self.board = self.read_sudoku(filename)

    def __str__(self):
        output = "╔═══════╦═══════╦═══════╗\n"
        # iterate through rows
        for i in range(9):
            if i == 3 or i == 6:
                output += "╠═══════╬═══════╬═══════╣\n"
            output += "║ "
            # iterate through columns
            for j in range(9):
                if j == 3 or j == 6:
                    output += "║ "
                output += str(self.board[i][j]) + " "
            output += "║\n"
        output += "╚═══════╩═══════╩═══════╝\n"
        return output

    @staticmethod
    def read_sudoku(filename):
        """
        Read in a sudoku file
        @param filename: Sudoku filename
        @return: A 9x9 grid of Fields where each field is initialized with all its neighbor fields
        """
        assert filename is not None and filename != "", "Invalid filename"
        # Setup 9x9 grid
        grid = [[Field for _ in range(9)] for _ in range(9)]

        try:
            with open(filename, "r") as file:
                for row, line in enumerate(file):
                    for col_index, char in enumerate(line):
                        if char == '\n':
                            continue
                        if int(char) == 0:
                            grid[row][col_index] = Field()
                        else:
                            grid[row][col_index] = Field(int(char))

        except FileNotFoundError:
            print("Error opening file: " + filename)

        Sudoku.add_neighbours(grid)
        return grid

    @staticmethod
    def add_neighbours(grid):
        """
        Adds a list of neighbors to each field.
        For each field in the 9x9 grid, find all fields that are in the same row, column, or 3x3 block, and set them as neighbours.
        @param grid: 9x9 list of Fields
        """

        # Go over every field
        for row in range(9):
            for column in range(9):

                # Define empty neighbour set
                neighbours = set()

                # Add fields in the same row
                for i in range(9):
                    # Check if it is not the field itself
                    if i != column:
                        neighbours.add(grid[row][i])

                # Add fields in the same column
                for i in range(9):
                    # Check if it is not the field itself
                    if i != row:
                        neighbours.add(grid[i][column])
                
                # Find the 3x3 sub grid the field is in
                sub_grid_origin_r = row // 3 * 3
                sub_grid_origin_c = column // 3 * 3
                for i in range(sub_grid_origin_r, sub_grid_origin_r+3):
                    for j in range(sub_grid_origin_c, sub_grid_origin_c+3):

                        # Add all fields except for the field itself
                        if i != row and j != column:
                            neighbours.add(grid[i][j])
                
                # Save the neighbours
                grid[i][j].set_neighbours(list(neighbours))
                

    def board_to_string(self):

        output = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                output += self.board[row][col].get_value()
            output += "\n"
        return output

    def get_board(self):
        return self.board
