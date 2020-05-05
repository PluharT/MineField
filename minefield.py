from random import randrange


class MineField:
    current_cell = [0, 0]
    Cell_array = []
    Field_rows = 0
    Field_columns = 0
    Field_mines = 0

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
        for i in range(0, self.Field_rows):
            temp_list = []
            for j in range(0, self.Field_columns):
                temp_list.append([0, 0])
            self.Cell_array.append(temp_list)

    def game_generate_mines(self, *cells):
        """
        generates mines in the Cell_array, by setting the first variable to -1
        returns if there are more mines than cells
        can set specific cells as mines, with args
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


# ----------T-E-S-T----------
lol = MineField()
lol.set_attributes(3, 3, 3)
lol.game_generate_cell_array()
lol.game_generate_mines()
print(lol.Cell_array)
