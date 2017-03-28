# makes sure cell choice is ok
def validate_cell_choice(input_string, board_size):
    columns = [chr(c) for c in range(ord('a'), (ord('a') + board_size))]
    input_list = input_string.split(" ")

    if len(input_list) != 2:
        raise ValueError(
            "Incorrect number of arguments."
            "You need a space between row and column")

    if input_list[0] not in columns:
        raise ValueError(
            "First argument must be a letter between A and {}.".format(
                columns[-1].upper()))

    try:
        if int(input_list[1]) not in range(1, board_size + 1):
            raise ValueError(
                "Second argument must be between 1 and {}".format(
                    board_size))
    except ValueError as ve:
        raise ValueError(
            "Second argument must be an number between 1 and {}".format(
                board_size))

# checks to see vertical or horizontal is selected
def validate_orientation(input_string):
    if input_string not in ['h', 'v']:
        raise ValueError(
            "Ships must be either [V]ertically or [H]orizontally.")

# check if the player has guessed cell
def validate_guess(guess, player):
    made_guesses = set(player.hits + player.misses)
    if guess in made_guesses:
        raise ValueError("You've already tried that on. Try again.")

# ensure that a ship is placed on board with no overlap
def validate_ship_placement(origin, orientation, ship,
                            ship_list, board_size):

    column, row = origin
    check = 0

    if orientation == 'h':
        check = column + ship.length - 1
        for col in range(column, column + ship.length):
            validate_ship_cell((col, row), ship, ship_list)
    elif orientation == 'v':
        check = row + ship.length - 1
        for r in range(row, row + ship.length):
            validate_ship_cell((column, r), ship, ship_list)

    if check > board_size:
        raise ValueError(
            "ERROR: Your {} must be placed on the board.".format(
                ship.name))

# checks to make ships placed don't overlap
def validate_ship_cell(cell, ship, ship_list):
    for existing_ship in ship_list:
        if existing_ship.cells:
            if cell in existing_ship.cells.keys():
                raise ValueError("ERROR: Your {} overlaps with your {} at"
                                 "cell [{} {}]. Try again.".format(
                                     ship.name, existing_ship.name,
                                     cell[0], cell[1]))
