import tkinter as tk
from random import randint
from enum import Enum
from colorama import Fore
from colorama import Style


class States(Enum):
    GAME_OFF = 1
    GAME_RUNNING = 2
    GAME_FAIL = 3
    GAME_VICTORY = 4


class CellAlreadyClear(Exception):
    pass


class CellFlagged(Exception):
    pass


def add(x, y):  # adds two numbers together
    return x + y


class MineField:
    game_state = States.GAME_OFF
    Mine_array = []  # stores integers which are representing the mines
    Mine_count = 13  # how many armed mines should be armed from the field
    Field_rows = 5  # how many rows the field has
    Field_columns = 5  # how many columns the field has
    Mine_n_check_dict = {
        "NW": [[0, 1], [1, 1], [1, 0]],
        "NE": [[0, -1], [1, -1], [1, 0]],
        "SW": [[-1, 0], [-1, 1], [0, 1]],
        "SE": [[0, -1], [-1, -1], [-1, 0]],
        "N": [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1]],
        "S": [[0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]],
        "W": [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0]],
        "E": [[-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0]],
        "M": [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    }  # used in neighbour calculation
    Mine_n_corner_dict = {
        "NW": [0, 0],
        "NE": [0, -1],
        "SW": [-1, 0],
        "SE": [-1, -1]
    }  # used in neighbour calculation for the corners
    Mine_n_horizontal_dict = {
        "N": 0,
        "S": -1
    }  # used in neighbour calculation for the horizontal lines
    Mine_n_vertical_dict = {
        "W": 0,
        "E": -1
    }  # used in neighbour calculation for the vertical lines
    Mine_empty_dict = {
        "corner":
            {(0, 0): "NW",
             (0, Field_columns - 1): "NE",
             (Field_rows - 1, 0): "SW",
             (Field_rows - 1, Field_columns - 1): "SE", },
        "vertical":
            {0: "N",
             Field_rows - 1: "S"},
        "horizontal":
            {0: "W",
             Field_columns - 1: "E"}
    }
    player_prefix = f"{Fore.GREEN}\nplayer> {Style.RESET_ALL}"
    sys_prefix = f"{Fore.YELLOW}minefield>{Style.RESET_ALL}"

    def set_attributes(self, rows=5, columns=5, mine_count=13, ):  # sets the attributes of an instance of this class
        self.Field_rows = rows
        self.Field_columns = columns
        self.Mine_count = mine_count

    def generate_array(self):
        """fills up the self.Mine_array variable with lists, who's members are:
        [0]: how many neighbouring cells are mines, or said cell is a mine or not
            -1: mine
            0-9: how many neighbouring cells are mines, if the cell itself is not a mine
        [1]: the visual state of the cell:
            -1: neighbours uncalculated
            0: covered
            1: uncovered
            2: flagged
            3: ?flagged"""
        for i in range(0, self.Field_rows):
            temp_mine_column = []
            for j in range(0, self.Field_columns):
                temp_mine_column.append([0, -1])
            self.Mine_array.append(temp_mine_column)

    def generate_mines(self):
        """makes random mines from self.Mine_array armed (via setting its [0] to -2)
        according to the self.Mine_count variable, raises ValueError if there are more armed mines than actual cells"""
        if self.Mine_count > (self.Field_rows * self.Field_columns):
            raise ValueError
        if not self.Mine_array:
            self.generate_array()
        else:
            i = 0
            while True:
                if i == self.Mine_count:
                    break
                rand_row = randint(0, add(self.Field_rows, -1))
                rand_column = randint(0, add(self.Field_columns, -1))
                if not self.Mine_array[rand_row][rand_column][0] == -2:
                    self.Mine_array[rand_row][rand_column][0] = -1
                    i += 1

    def generate_neighbours(self):
        """calculates, out of given mine's neighbours, how many of them is armed,
        and stores it in it's armed variable"""
        if not self.Mine_array:
            self.generate_array()
        else:
            for i in self.Mine_n_corner_dict:
                temp_n_armed = 0
                if not self.Mine_array[self.Mine_n_corner_dict[i][0]][self.Mine_n_corner_dict[i][1]][0] == -1:
                    for j in self.Mine_n_check_dict[i]:
                        temp_n_armed += 1 if self.Mine_array[self.Mine_n_corner_dict[i][0] + j[0]] \
                                                 [self.Mine_n_corner_dict[i][1] + j[1]][0] == -1 else 0
                    self.Mine_array[self.Mine_n_corner_dict[i][0]][self.Mine_n_corner_dict[i][1]] = [temp_n_armed, 0]
                else:
                    self.Mine_array[self.Mine_n_corner_dict[i][0]][self.Mine_n_corner_dict[i][1]][1] = 0

            if self.Mine_array[0][1][1] == -1:
                for i in self.Mine_n_horizontal_dict:
                    for j in range(1, add(self.Field_columns, -1)):
                        if not self.Mine_array[self.Mine_n_horizontal_dict[i]][j][0] == - 1:
                            temp_n_armed = 0
                            for k in self.Mine_n_check_dict[i]:
                                temp_n_armed += 1 if self.Mine_array[self.Mine_n_horizontal_dict[i] + k[0]][
                                                         j + k[1]][0] == - 1 else 0
                            self.Mine_array[self.Mine_n_horizontal_dict[i]][j] = [temp_n_armed, 0]
                        else:
                            self.Mine_array[self.Mine_n_horizontal_dict[i]][j][1] = 0

            if self.Mine_array[1][0][1] == -1:
                for i in self.Mine_n_vertical_dict:
                    for j in range(1, add(self.Field_rows, -1)):
                        if not self.Mine_array[j][self.Mine_n_vertical_dict[i]][0] == -1:
                            temp_n_armed = 0
                            for k in self.Mine_n_check_dict[i]:
                                temp_n_armed += 1 if self.Mine_array[j + k[0]][
                                                         self.Mine_n_vertical_dict[i] + k[1]][0] == -1 else 0
                            self.Mine_array[j][self.Mine_n_vertical_dict[i]] = [temp_n_armed, 0]
                        else:
                            self.Mine_array[j][self.Mine_n_vertical_dict[i]][1] = 0

            if self.Mine_array[1][1][1] == -1:
                for i in range(1, add(self.Field_rows, -1)):
                    for j in range(1, add(self.Field_columns, -1)):
                        if not self.Mine_array[i][j][0] == -1:
                            temp_n_armed = 0
                            for k in self.Mine_n_check_dict["M"]:
                                temp_n_armed += 1 if self.Mine_array[i + k[0]][j + k[1]][0] == -1 else 0
                            self.Mine_array[i][j] = [temp_n_armed, 0]
                        else:
                            self.Mine_array[i][j][1] = 0

    def return_armed(self):  # TEST, returns all the .armed variables from self.Mine_array
        temp_array = []
        for i in range(0, self.Field_rows):
            temp_temp_array = []
            for j in range(0, self.Field_columns):
                temp_temp_array.append(self.Mine_array[i][j][0])
            temp_array.append(temp_temp_array)
        return temp_array

    def clear_array(self):  # clears the entire Mine_array
        self.Mine_array = []

    def clear_mines(self):  # sets back each value to -1
        if not self.Mine_array:
            return
        for i in range(0, add(self.Field_rows, -1)):
            for j in range(0, add(self.Field_rows, -1)):
                self.Mine_array[i][j][1] = -1

    def cli(self, prefix):  # runs a game of minefield using the command line interface
        if not self.game_state == States.GAME_OFF:
            return
        try:
            self.cli_initialize(prefix)
            temp_cell = []
            while True:
                if self.game_state == States.GAME_FAIL:
                    self.game_show_all_mines()
                    self.cli_draw_field()
                    print(prefix, " Game over! The cell at [", str(temp_cell[0]), ":", str(temp_cell[1]),
                          "] was a mine!")
                    break
                if self.game_victory_check():
                    self.cli_draw_field()
                    print(prefix, " Congratulations! You've won!")
                    break
                self.cli_draw_field()
                while True:
                    temp_input = input(prefix + " Next cell, and action:" + self.player_prefix)
                    if not temp_input.__len__() == 5:
                        print(prefix, ' Wrong syntax, try again! (correct syntax: "column,row action")')
                        break
                    if not any((i == int(temp_input[0])) for i in range(1, add(self.Field_rows, 1))):
                        print(prefix, ' Wrong syntax, try again! (correct syntax: "column,row action")')
                        break
                    if not any((i == int(temp_input[2])) for i in range(1, add(self.Field_columns, 1))):
                        print(prefix, ' Wrong syntax, try again! (correct syntax: "column,row action")')
                        break
                    if not any((i == temp_input[4].upper()) for i in ["U", "F", "?"]):
                        print(prefix, ' Wrong syntax, try again! (correct syntax: "column,row action")')
                        break
                    temp_action = temp_input[4]
                    temp_cell = [int(temp_input[0]), int(temp_input[2])]

                    try:
                        self.game_set_cell_state(temp_cell, temp_action)
                    except CellFlagged:
                        print(prefix, " That cell is flagged!")
                    except CellAlreadyClear:
                        print(prefix, " That cell is already clear!")
                    finally:
                        break

        except KeyboardInterrupt:
            print("\nGoodbye!")

    def cli_initialize(self, prefix):
        if not self.game_state == States.GAME_OFF:
            return
        else:
            self.game_state = States.GAME_RUNNING
            temp_rows = 0
            temp_columns = 0
            temp_mines = 0
            print(prefix, f"Welcome to:")
            print(" ___ ___  ____  ____     ___  _____  ____    ___  _      ___   \n"
                  "|   |   ||    ||    \   /  _]|     ||    |  /  _]| |    |   \  \n"
                  "| _   _ | |  | |  _  | /  [_ |   __| |  |  /  [_ | |    |    \ \n"
                  "|  \_/  | |  | |  |  ||    _]|  |_   |  | |    _]| |___ |  D  |\n"
                  "|   |   | |  | |  |  ||   [_ |   _]  |  | |   [_ |     ||     |\n"
                  "|   |   | |  | |  |  ||     ||  |    |  | |     ||     ||     |\n"
                  "|___|___||____||__|__||_____||__|   |____||_____||_____||_____|\n"
                  "                                                               ")
            print(prefix,
                  f"Gameplay: select one cell, and one of the three actions ('U': uncover, 'F': flag, '?': ?flag")
            print(prefix, "Example: '3,3 u'")
            while True:
                try:
                    temp_rows = int(input(prefix + f" Please enter the number of {Fore.RED}rows{Style.RESET_ALL} (min: "
                                                   "2, max: 9): " + self.player_prefix))
                except ValueError:
                    continue
                if 2 <= temp_rows <= 9:
                    break

            while True:
                try:
                    temp_columns = int(
                        input(prefix + f" Please enter the number of {Fore.RED}columns{Style.RESET_ALL} (min: 2, max: "
                                       "9): " + self.player_prefix))
                except ValueError:
                    continue
                if 2 <= temp_columns <= 9:
                    break

            while True:
                try:
                    temp_mines = int(input(prefix + f" Please enter the number of {Fore.RED}mines{Style.RESET_ALL} "
                                                    f"(min 2, max: " + str(temp_rows * temp_columns) + "): "
                                           + self.player_prefix))
                except ValueError:
                    continue
                if 2 <= temp_mines <= (temp_rows * temp_columns):
                    break

            self.set_attributes(temp_rows, temp_columns, temp_mines)
            self.generate_array()
            self.generate_mines()
            self.generate_neighbours()
            self.update_empty_dict()
            print(prefix, " Let the game begin!")

    def cli_draw_field(self):
        print(" ")
        temp_draw = ""
        temp_top_row = ""
        temp_top_row += f"   {Fore.BLUE}"
        for i in range(1, add(self.Field_columns, 1)):
            temp_top_row += str(i) + " "
        temp_top_row += f"{Style.RESET_ALL}\n"
        temp_draw += temp_top_row
        for i in range(0, self.Field_rows):
            x = i
            x += 1
            temp_row = f"{Fore.BLUE} " + str(x) + f"{Style.RESET_ALL} "
            for j in range(0, self.Field_columns):
                if self.Mine_array[i][j][1] == 0:
                    temp_row += "# "
                elif self.Mine_array[i][j][1] == 1:
                    if self.Mine_array[i][j][0] == -1:
                        temp_row += f"{Fore.RED}M {Style.RESET_ALL}"
                    elif self.Mine_array[i][j][0] == 0:
                        temp_row += "  "
                    else:
                        temp_row += f"{Fore.GREEN}" + str(self.Mine_array[i][j][0]) + f"{Style.RESET_ALL} "
                elif self.Mine_array[i][j][1] == 2:
                    temp_row += f"{Fore.RED}F {Style.RESET_ALL}"
                elif self.Mine_array[i][j][1] == 3:
                    temp_row += f"{Fore.YELLOW}? {Style.RESET_ALL}"
            temp_draw += temp_row + "\n"
        print(temp_draw)

    def game_set_cell_state(self, cell, state):
        cell_row = cell[1] - 1
        cell_column = cell[0] - 1
        state = state.upper()
        if not 0 <= cell_row < self.Field_rows:
            raise ValueError
        if not 0 <= cell_column < self.Field_columns:
            raise ValueError
        if not any((i == state) for i in ["U", "F", "?"]):
            raise ValueError

        if state == "U":
            if self.Mine_array[cell_row][cell_column][0] == -1:
                self.game_state = States.GAME_FAIL
                return
            elif self.Mine_array[cell_row][cell_column][1] == 0:
                self.Mine_array[cell_row][cell_column][1] = 1
                if self.Mine_array[cell_row][cell_column][0] == 0:
                    self.game_uncover_empty([cell_row, cell_column])
                return
            elif self.Mine_array[cell_row][cell_column][1] == 1:
                raise CellAlreadyClear
            else:
                raise CellFlagged

        if state == "F":
            if self.Mine_array[cell_row][cell_column][1] == 1:
                raise CellAlreadyClear
            elif self.Mine_array[cell_row][cell_column][1] == 2:
                self.Mine_array[cell_row][cell_column][1] = 0
                return
            else:
                self.Mine_array[cell_row][cell_column][1] = 2

        if state == "?":
            if self.Mine_array[cell_row][cell_column][1] == 1:
                raise CellAlreadyClear
            elif self.Mine_array[cell_row][cell_column][1] == 3:
                self.Mine_array[cell_row][cell_column][1] = 0
                return
            else:
                self.Mine_array[cell_row][cell_column][1] = 3

    def game_victory_check(self):
        for i in self.Mine_array:
            for j in i:
                if not j[0] == -1:
                    if not j[1] == 1:
                        return False
        else:
            return True

    def game_show_all_mines(self):
        for i in self.Mine_array:
            for j in i:
                if j[0] == -1:
                    j[1] = 1

    def update_empty_dict(self):
        self.Mine_empty_dict = {
            "corner":
                {(0, 0): "NW",
                 (0, self.Field_columns - 1): "NE",
                 (self.Field_rows - 1, 0): "SW",
                 (self.Field_rows - 1, self.Field_columns - 1): "SE", },
            "vertical":
                {0: "N",
                 self.Field_rows - 1: "S"},
            "horizontal":
                {0: "W",
                 self.Field_columns - 1: "E"}
        }

    def game_uncover_empty(self, cell):
        empty_dict = self.Mine_empty_dict
        check_dict = self.Mine_n_check_dict
        for i in empty_dict["corner"]:
            if cell == list(i):
                for j in check_dict[empty_dict["corner"][i]]:
                    self.Mine_array[cell[0] + j[0]][cell[1] + j[1]][1] = 1
                    if self.Mine_array[cell[0] + j[0]][cell[1] + j[1]][0] == 0:
                        self.game_uncover_empty([cell[0] + j[0], cell[1] + j[1]])
                return
        for i in empty_dict["vertical"]:
            if cell[0] == i:
                for j in check_dict[empty_dict["vertical"][i]]:
                    self.Mine_array[cell[0] + j[0]][cell[1] + j[1]][1] = 1
                    if self.Mine_array[cell[0] + j[0]][cell[1] + j[1]][0] == 0:
                        self.game_uncover_empty([cell[0] + j[0], cell[1] + j[1]])
                return
        for i in empty_dict["horizontal"]:
            if cell[1] == i:
                for j in check_dict[empty_dict["horizontal"][i]]:
                    self.Mine_array[cell[0] + j[0]][cell[1] + j[1]][1] = 1
                    if self.Mine_array[cell[0] + j[0]][cell[1] + j[1]][0] == 0:
                        self.game_uncover_empty([cell[0] + j[0], cell[1] + j[1]])
                return
        for j in check_dict["M"]:
            self.Mine_array[cell[0] + j[0]][cell[1] + j[1]][1] = 1


# ----------T-E-S-T----------


lol = MineField()
lol.cli(lol.sys_prefix)
