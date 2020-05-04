class MineField:
    current_cell = [0, 0]
    Cell_array = []
    Field_rows = 0
    Field_columns = 0
    Field_mines = 0

    def set_attributes(self, rows=0, columns=0, mines=0):
        """Sets one MineFields attributes, raises ValueError if the parameters are negative"""
        if rows or columns or mines < 0:
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
        if self.Field_columns or self.Field_rows == 0:
            return
        for i in range(self.Field_rows):
            temp_list = []
            for j in range(self.Field_columns):
                temp_list.append([0, 0])
            self.Cell_array.append(temp_list)
