import check as validator


class Player():
    """This class contains the player control methods with checks to make sure the
        user is inputing legal information into the game"""

    def __init__(self, name):
        self.name = name
        self.ships = []
        self.hits = []
        self.misses = []

    # Makes sure all ships are on board based on ships in list
    def ready(self, ship_number):
        return len(self.ships) == ship_number

    # goes through ship list for board placement
    def add_ship(self, ship_to_add):
        if ship_to_add.name not in [ship.name for ship in self.ships]:
            self.ships.append(ship_to_add)
        else:
            raise Exception("That ship is already in player's list.")

    # method to place ship on the board via x,y axis
    def place_ship(self, ship, orgin, orientation, board_size):
        try:
            validator.validate_ship_placement(orgin, orientation, ship,
                                              self.ships, board_size)
        except ValueError as ve:
            raise ve

        column, rows = orgin

        ship_cells = []
        is_horizontal = True

        if orientation == 'h':
            ship_cells.extend([(col, rows)
                               for col in range(column, column + ship.length)])
        elif orientation == 'v':
            ship_cells.extend([(column, row)
                               for row in range(rows, rows + ship.length)])
        is_horizontal = False

        ship.set_cells(ship_cells, is_horizontal)

    # guess sheip and see if it his or sinks ship
    def make_guess(self, guess, opponent):
        try:
            validator.validate_guess(guess, self)
        except ValueError as ve:
            raise ve

        response = ''

        for ship in opponent.ships:
            if guess in ship.cells.keys():
                self.hits.append(guess)
                ship.cells[guess] = False

                if ship.is_sunk():
                    response = "You sunk {}'s {}".format(opponent.name,
                                                         ship.name)
                return True, response

        self.misses.append(guess)
        return False, response
