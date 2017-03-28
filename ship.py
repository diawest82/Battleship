
class Ship:
    """This class contains methods for setting ships on the board
        and for also determining if the ship has sunk"""

    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.cells = {}
        self.is_set = False

    # method to set cells for the player
    def set_cells(self, cells, is_horizontal=True):

        for cell in cells:
            self.cells[cell] = True

        self.is_horizontal = is_horizontal
        self.is_set = True

    # method to detirmine if a ship has been sunk
    def is_sunk(self):
        if True in self.cells.values():
            return False
        else:
            return True
