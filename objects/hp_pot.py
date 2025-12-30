from colorama import Fore

class HpPot:
    def __init__(self):
        self.char: str = Fore.RED + "+" + Fore.RESET
        self.heal_amount: int = 8

        self.x_pos: int
        self.y_pos: int

    def set_pos(self, board: list[list[str]]):
        board[self.y_pos][self.x_pos] = self.char