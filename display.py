import check as validator


class Display:

    VERTICAL_SHIP = '|'
    HORIZONTAL_SHIP = '-'
    EMPTY = 'O'
    MISS = '.'
    HIT = '*'
    SUNK = '#'

    """It contains the methods for choosing names, printing the board,
        and user ineractions with the console"""

    def __init__(self, board_size=10):
        self.BOARD_SIZE = board_size

    # prompt to create names for only 2 players
    def prompt_for_names(self):
        self.clear_screen()

        players = []
        num = 1

        while len(players) < 2:
            confirm_name = 'n'

            while confirm_name != 'y':
                player_name = input("What is player {}'s name? ".format(num))
                confirm_name = input("Thanks {}! Is this correct?"
                                     "[Y/N]".format(player_name)).lower()
            players.append(player_name)
            num += 1

            self.clear_screen()
        return players

    # prompt to place ships
    def prompt_for_ship_placement(self, ship_to_place):
        print("Next ship: {}, length: {}".format(ship_to_place.name,
                                                 ship_to_place.length))

        done = False

        while not done:
            try:
                origin = self.get_cell_input(
                    "Which cell should the ship go to (ex A 9, G 5 etc)? ")
            except ValueError as exc:
                print(exc)
                continue

            done = True

        while done:
            orientation = input("[H]orizontal or [Vertical]? ").lower()

            try:
                validator.validate_orientation(orientation)
            except ValueError as exc:
                print(exc)
                continue

            done = False

        return(origin, orientation)

    # prompt to allow guess
    def prompt_guess(self):

        guessed = False

        while not guessed:
            try:
                guess = self.get_cell_input("Guess a cell. ")
            except ValueError as ve:
                print(ve)
                continue

            guessed = True
        return guess

    # Get cell info of choice
    def get_cell_input(self, message):
        cell_choice = input(message).lower()
        validator.validate_cell_choice(cell_choice, self.BOARD_SIZE)
        cell_list = cell_choice.split(' ')

        column = ord(cell_list[0]) - ord('a') + 1
        return (column, int(cell_list[1]))

    # clears screen
    def clear_screen(self):
        print("\033c", end="")

    # print's letter's on top of board
    def print_board_heading(self):
        print("   " + " ".join([chr(c) for c in range(ord('A'),
                                ord('A') + self.BOARD_SIZE)]))

    # print's board
    def print_board(self, board):
        self.print_board_heading()

        row_num = 1
        for row in board:
            print(str(row_num).rjust(2) + " " + (" ".join(row)))
            row_num += 1

        print()

    # constructs player board that shows player and opponent ships
    def construct_player_board(self, player, opponent, show_ships=True):
        board = []

        for row in range(1, self.BOARD_SIZE + 1):
            output = []
            for col in range(1, self.BOARD_SIZE + 1):
                field = self.EMPTY
                if show_ships:

                    for ship in player.ships:
                        if (col, row) in ship.cells.keys():
                            if ship.is_sunk():
                                field = self.SUNK
                            elif (col, row) in opponent.hits:
                                field = self.HIT
                            else:
                                if ship.is_horizontal:
                                    field = self.HORIZONTAL_SHIP
                                else:
                                    field = self.VERTICAL_SHIP
                        else:
                            if (col, row) in opponent.misses:
                                field = self.MISS
                else:
                    for ship in opponent.ships:
                        if (col, row) in ship.cells.keys():
                            if ship.is_sunk():
                                field = self.SUNK
                            elif (col, row) in player.hits:
                                field = self.HIT
                        else:
                            if (col, row) in player.misses:
                                field = self.MISS
                output.append(field)
            board.append(output)
        return board

    # let's players know when to switch
    def prompt_switch(self, opponent):
        input("Now it's {}'s turn. Press [ENTER] when ready ".format(opponent))
