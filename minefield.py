from random import randrange


class CellClear(Exception):
    pass


class CellFlagged(Exception):
    pass


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
    Game_state = 0
    """
    Game_state: tells the runtime what state is the game in:
    0: off
    1: running
    2: victory
    3: fail
    """

    def set_attributes(self, rows=0, columns=0, mines=0):
        """
        Sets one MineFields attributes,
        :raises ValueError if the parameters are negative, or there are more mines than cells
        """
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
        """sets self.Game_state to 2 (victory) if all non-mine cells are uncovered"""
        for i in range(self.Field_rows):
            for j in range(self.Field_columns):
                if not self.Cell_array[i][j][0] == -1:
                    if self.Cell_array[i][j][1] == 0:
                        return
        self.Game_state = 2

    def game_set_cell_state(self, cell, new_state):
        """
        Sets a given cells state, according to the argument, new_state
        Sets self.Game_state to 3 (fail) if a mine is uncovered
        :raises ValueError if new_state is not a valid action
        :raises CellFlagged when trying to uncover a flagged cell
        :raises CellClear when trying to uncover or flag an already clear cell
        """
        current_cell = self.Cell_array[cell[0]][cell[1]]
        check = self.Game_neighbour_check_tuple
        valid_actions = ["U", "F", "?"]
        if new_state not in valid_actions:
            raise ValueError

        if new_state == "U":
            if current_cell[0] == -1:
                self.Game_state = 3
                return
            if current_cell[1] == (2 or 3):
                raise CellFlagged
            if current_cell[1] == 1:
                raise CellClear
            if current_cell[0] == 0:
                for i in check:
                    if 0 <= cell[0] + i[0] < self.Field_rows and 0 <= cell[1] + i[1] < self.Field_columns:
                        try:
                            self.game_set_cell_state([cell[0] + i[0], cell[1] + i[1]], "U")
                        except (CellClear, CellFlagged):
                            pass
            self.Cell_array[cell[0]][cell[1]][1] = 1
            return
        if current_cell[1] == 1:
            raise CellClear
        if new_state == "F":
            if current_cell[1] in (0, 3):
                self.Cell_array[cell[0]][cell[1]][1] = 2
                return
            if current_cell[1] == 2:
                self.Cell_array[cell[0]][cell[1]][1] = 0

        if new_state == "?":
            if current_cell[1] in (0, 2):
                self.Cell_array[cell[0]][cell[1]][1] = 3
                return
            if current_cell[1] == 3:
                self.Cell_array[cell[0]][cell[1]][1] = 0


# ----------T-E-S-T----------
spam = MineField()
spam.set_attributes(2, 2)
spam.game_generate_cell_array()
spam.game_generate_mines([0, 0])
spam.game_generate_neighbours()
print(spam.Cell_array)
