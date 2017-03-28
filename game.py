from display import Display
from player import Player
from ship import Ship


class Battleship:
    BOARD_SIZE = 10

    SHIP_INFO = [
        ("Aircraft Carrier", 5),
        ("Battleship", 4),
        ("Submarine", 3),
        ("Cruiser", 3),
        ("Dinghy", 2)]

    """Contains the game handling methods and the entry point into the game as well"""

    def __init__(self):
        self.display = Display(self.BOARD_SIZE)
        players = self.display.prompt_for_names()
        self.player1 = Player(players[0])
        self.player2 = Player(players[1])

    def ready(self):
        """ checks to see if player's have both properly assigned their ships
        returns a bool if they are all the same length"""
        return len(self.player1.ships) == len(
            self.player2.ships) == len(self.SHIP_INFO)

    def game_over(self):
        "checks to see if the game has ended and ships have been sunk"

        for player in [self.player1, self.player2]:
            for ship in player.ships:
                if not ship.is_sunk():
                    return False
        else:
            return True

    def lost(self, player):
        "checks to see when a player loses"

        for ship in player.ships:
            if not ship.is_sunk():
                return False
        return True

    def setup_game(self, player, opponent):
        """Prompts a single player to place their ships"""

        self.display.clear_screen()

        ship_index = 0

        while not player.ready(len(self.SHIP_INFO)):
            # prints the currrent board
            board = self.display.construct_player_board(player, opponent, True)
            self.display.print_board(board)

            ship_name, ship_length = self.SHIP_INFO[ship_index]
            ship_to_add = Ship(ship_name, ship_length)

            try:
                player.add_ship(ship_to_add)
            except Exception as e:
                ship_to_add = player.ships[ship_index]

            origin, orientation = self.display.prompt_for_ship_placement(
                ship_to_add)

            try:
                player.place_ship(ship_to_add, origin, orientation,
                                  self.BOARD_SIZE)
            except ValueError as ve:
                self.display.clear_screen()
                print(ve)
                print()
                continue

            self.display.clear_screen()
            ship_index += 1
        self.display.prompt_switch(opponent.name)

    def play(self):
        """Let's you take turns"""

        player1_turn = True

        while True:
            if player1_turn:
                self.player_turn(self.player1, self.player2)
                if self.lost(self.player2):
                    print("Game Over!! You sank {}'s ships!".format(
                        self.player2.name))
                    break
                player1_turn = False
            else:
                self.player_turn(self.player2, self.player1)
                if self.lost(self.player1):
                    print("Game Over!! You sank {}'s ships!".format(
                        self.player1.name))
                    break
                player1_turn = True

    def player_turn(self, player, opponent):
        "Captures, checks and runs a single player's guess"

        self.display.clear_screen()

        guess_made = False

        while not guess_made:
            print("Opponent's Board")
            board = self.display.construct_player_board(player,
                                                        opponent, False)
            self.display.print_board(board)
            print("Your board {}.".format(player.name))
            board = self.display.construct_player_board(player, opponent, True)
            self.display.print_board(board)

            guess = self.display.prompt_guess()

            try:
                success, message = player.make_guess(guess, opponent)
            except Exception as ve:
                self.display.clear_screen()
                print(ve)
                print()
                continue

            guess_made = True

        if success:
            print("You got a hit!")
            if message != '':
                print(message)
        else:
            print("You missed.")
        self.display.prompt_switch(opponent.name)


if __name__ == '__main__':
    start = Battleship()

    while not start.ready():
        start.setup_game(start.player1, start.player2)
        start.setup_game(start.player2, start.player1)

    start.play()
