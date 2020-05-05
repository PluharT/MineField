from random import randrange


class MineField:
    current_cell = [0, 0]
    Cell_array = []
    Field_rows = 0
    Field_columns = 0
    Field_mines = 0
    Game_neighbour_check_tuple = (
        [-1, -1],
        [-1, 0],
        [-1, 1],
        [0, -1],
        [0, 1],
        [1, -1],
        [1, 0],
        [1, 1]
    )

    def set_attributes(self, rows=0, columns=0, mines=0):
        """Sets one MineFields attributes, raises ValueError if the parameters are negative"""
        if (rows or columns or mines) < 0:
            raise ValueError
        if mines > (rows * columns):
            raise ValueError
        if not rows == 0:
            self.Field_rows = rows
        if not columns == 0:
            self.Field_columns = columns
        if not mines == 0:
            self.Field_mines = mines

    def game_generate_cell_array(self):
        """Generates the field by creating a two dimensional list, returns if self.rows or self.columns are 0"""
        if (self.Field_columns or self.Field_rows) == 0:
            return
        for i in range(self.Field_rows):
            temp_list = []
            for j in range(self.Field_columns):
                temp_list.append([0, 0])
            self.Cell_array.append(temp_list)

    def game_generate_mines(self, *cells):
        """
        generates mines in the Cell_array, by setting the first variable to -1
        returns if there are more mines than cells
        can set specific cells as mines, with cells
        :type cells: list
        """
        rows = self.Field_rows
        columns = self.Field_columns
        mines = self.Field_mines
        if cells:
            for i in cells:
                try:
                    self.Cell_array[i[0]][i[1]][0] = -1
                except:
                    continue
        elif mines > rows * columns:
            return
        else:
            i = 0
            while True:
                if i == mines:
                    break
                current_cell = [randrange(0, rows), randrange(0, columns)]
                if not self.Cell_array[current_cell[0]][current_cell[1]][0] == -1:
                    self.Cell_array[current_cell[0]][current_cell[1]][0] = -1
                    i += 1

    def game_generate_neighbours(self):
        """
        Goes through each cell, and counts how many of it's neighbouring cells are mines, if itself is not a mine
        Stores the counted value
        """
        rows = self.Field_rows
        columns = self.Field_columns
        check = self.Game_neighbour_check_tuple
        for i in range(rows):
            for j in range(columns):
                if self.Cell_array[i][j][0] == -1:
                    continue
                temp_n_mines = 0
                for k in check:
                    if 0 <= i + k[0] < rows and 0 <= j + k[1] < columns:
                        temp_n_mines += 1 if self.Cell_array[i + k[0]][j + k[1]][0] == -1 else 0
                self.Cell_array[i][j][0] = temp_n_mines

    def game_victory_check(self):
        """returns True if all non-mine cells are uncovered, otherwise returns False"""
        for i in range(self.Field_rows):
            for j in range(self.Field_columns):
                if not self.Cell_array[i][j][0] == -1:
                    if self.Cell_array[i][j][1] == 0:
                        return False
            return True


# ----------T-E-S-T----------
lol = MineField()
lol.set_attributes(1, 1)
lol.game_generate_cell_array()
lol.game_generate_mines()
lol.game_generate_neighbours()
print(lol.Cell_array)
print(lol.game_victory_check())
