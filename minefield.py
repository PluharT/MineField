import sys
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
    help_text = "Welcome to MineField!\n" \
                "Your goal is to uncover all cells, which are not mines!\n" \
                "The Field looks like this:\n\n" \
                "   1 2 3 4 5\n" \
                " 1         1\n" \
                " 2       2 F\n" \
                " 3     1 F X\n" \
                " 4     1 X X\n" \
                " 5     X X X\n" \
                "\n" \
                "Syntax of the input: row column action\n" \
                "For example: 3 4 U\n" \
                "Valid actions:\n" \
                "U: Uncover a cell\n" \
                "F: Flag a cell, or remove a flag from a cell\n" \
                "?: ?Flag a cell or remove a ?flag from a cell"
    about_text = "Thank you for playing my game!\n" \
                 "Programed by: Pluhár Tamás, 2020\n"
    greet_text = ("\n"
                  " ___ ___  ____  ____     ___  _____  ____    ___  _      ___   \n"
                  "|   |   ||    ||    \   /  _]|     ||    |  /  _]| |    |   \  \n"
                  "| _   _ | |  | |  _  | /  [_ |   __| |  |  /  [_ | |    |    \ \n"
                  "|  \_/  | |  | |  |  ||    _]|  |_   |  | |    _]| |___ |  D  |\n"
                  "|   |   | |  | |  |  ||   [_ |   _]  |  | |   [_ |     ||     |\n"
                  "|   |   | |  | |  |  ||     ||  |    |  | |     ||     ||     |\n"
                  "|___|___||____||__|__||_____||__|   |____||_____||_____||_____|\n"
                  "                                                               \n")
    angry_text = "You do you"
    cli_valid_actions = ("U", "F", "?")

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
            self.Cell_array[cell[0]][cell[1]][1] = 1
            if current_cell[0] == 0:
                for i in check:
                    if 0 <= cell[0] + i[0] < self.Field_rows and 0 <= cell[1] + i[1] < self.Field_columns:
                        try:
                            self.game_set_cell_state([cell[0] + i[0], cell[1] + i[1]], "U")
                        except (CellClear, CellFlagged):
                            continue
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

    def game_uncover_all_mines(self):
        """Used in a case of loss, to show all the mines, the wrong, and the correct flags"""
        for i in range(self.Field_rows):
            for j in range(self.Field_columns):
                current_cell = self.Cell_array[i][j]
                if current_cell[0] == -1 and current_cell[1] == 0:
                    self.Cell_array[i][j][1] = 1
                elif current_cell[0] == -1 and current_cell[1] == 2:
                    self.Cell_array[i][j][1] = 4
                elif (not current_cell[0] == -1) and current_cell[1] == 2:
                    self.Cell_array[i][j][1] = 5

    def runtime_cli(self):
        """
        Starts the game, using the command line interface
        """
        try:
            if not self.Game_state == 0:
                return
            self.Game_state = 1
            actions_dict = {
                "PLAY": self.cli_play,
                "HELP": self.cli_help,
                "ABOUT": self.cli_about,
                "NO": self.cli_no,
                "NEM": self.cli_no
            }
            print(self.greet_text)
            print('Type "Play" to play!')
            while not 0 == self.Game_state:
                user_in = input()
                if not user_in.strip().upper() in actions_dict:
                    print("Invalid action!")
                    continue
                actions_dict[user_in.strip().upper()]()
        except (KeyboardInterrupt, EOFError):
            pass

    def runtime_cli_draw_field(self):
        """Prints out the current state of the minefield"""
        temp_draw_field = ""
        temp_row_beginning = "  " if self.Field_rows < 9 else "    "
        temp_top_row = temp_row_beginning
        cells = self.Cell_array
        if self.Field_columns < 9:
            for i in range(1, self.Field_columns + 1):
                temp_top_row += str(i) + " "
        else:
            for i in range(1, self.Field_columns + 1):
                if i < 10:
                    temp_top_row += "  "
                else:
                    temp_top_row += str(i // 10) + " "
            temp_top_row += "\n" + temp_row_beginning
            counter = 0
            for i in range(1, self.Field_columns + 1):
                if i % 10 == 0:
                    counter += 10
                temp_top_row += str(i - counter) + " "
        temp_top_row += "\n"
        temp_draw_field += temp_top_row
        for i in range(0, self.Field_rows):
            if self.Field_rows < 9:
                temp_column = " " + str(i + 1) + " "
            else:
                if i < 9:
                    temp_column = "  " + str(i + 1) + " "
                else:
                    temp_column = " " + str(i + 1) + " "
            for j in range(0, self.Field_columns):
                if cells[i][j][1] == 0:
                    temp_column += "X "
                elif cells[i][j][1] == 2:
                    temp_column += "F "
                elif cells[i][j][1] == 3:
                    temp_column += "? "
                elif cells[i][j][1] == 4:
                    temp_column += "C "
                elif cells[i][j][1] == 5:
                    temp_column += "W "
                elif cells[i][j][0] == -1:
                    temp_column += "M "
                elif cells[i][j][0] == 0:
                    temp_column += "  "
                else:
                    temp_column += str(cells[i][j][0]) + " "
            temp_column += "\n"
            temp_draw_field += temp_column
        print(temp_draw_field)

    def cli_help(self):
        """Prints out the help text"""
        print(self.help_text)

    def cli_about(self):
        """Prints out the about text"""
        print(self.about_text)

    def cli_no(self):
        """Exist the program... lol"""
        print(self.angry_text)
        sys.exit()

    def cli_play(self):
        invalid = "Invalid value!"
        while True:
            rows = int(input("Please set the number of rows (min 1, max 20)\n").strip())
            if 1 <= rows <= 20:
                break
            else:
                print(invalid)
        while True:
            columns = int(input("Please set the number of columns (min 1, max 20)\n").strip())
            if 1 <= columns <= 20:
                break
            else:
                print(invalid)
        while True:
            mines = int(input("Please set the number of mines (min 1, max " + str(rows * columns) + ")\n").strip())
            if 1 <= mines <= (rows * columns):
                break
            else:
                print(invalid)
        self.set_attributes(rows, columns, mines)
        self.game_generate_cell_array()
        self.game_generate_mines()
        self.game_generate_neighbours()
        while True:
            self.game_victory_check()
            if self.Game_state == 3:
                self.game_uncover_all_mines()
            self.runtime_cli_draw_field()
            if self.Game_state == 2:
                print("Congratulations, You've won!")
                self.Game_state = 0
                break
            if self.Game_state == 3:
                print("You've lost!")
                self.Game_state = 0
                break
            while True:
                temp_next_action = input("Next cell, and action: \n").strip().upper()
                temp_row = ""
                temp_column = ""
                temp_action = ""
                progress = 0
                if temp_action.strip().upper() == "HELP":
                    self.cli_help()
                    spam = input("Press enter to continue")
                    break
                for i in temp_next_action:
                    if progress == 0 and i == " ":
                        progress = 1
                        continue
                    if progress == 0:
                        temp_column += i
                    if progress == 1:
                        temp_row += i
                    if progress == 1 and i == " ":
                        progress = 2
                        continue
                    if progress == 2:
                        temp_action += i

                try:
                    temp_row = int(temp_row) - 1
                except:
                    print("Invalid row!")
                    continue

                try:
                    temp_column = int(temp_column) - 1
                except:
                    print("Invalid column!")
                    continue

                if temp_action not in self.cli_valid_actions:
                    print("Invalid action!")
                    continue
                break
            try:
                self.game_set_cell_state([temp_row, temp_column], temp_action)
            except CellClear:
                print("That cell is already clear!")
            except CellFlagged:
                print("That cell is already flagged!")

    def runtime_gui(self):
        pass

# ----------T-E-S-T----------
spam = MineField()
"""
spam.set_attributes(4, 4)
spam.game_generate_cell_array()
spam.game_generate_mines([0, 0])
spam.game_generate_neighbours()
spam.game_set_cell_state([0, 0], "F")
spam.game_set_cell_state([1, 2], "F")
spam.game_set_cell_state([3, 3], "U")
spam.game_uncover_all_mines()
spam.runtime_cli_draw_field()
"""
spam.runtime_cli()
