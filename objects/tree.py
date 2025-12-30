import time
import random

from colorama import Fore

class Tree:
    def __init__(self):
        self.char: str = Fore.GREEN + "&" + Fore.RESET
        self.x_pos: int
        self.y_pos: int

    def set_pos(self, board: list[list[str]]):
        board[self.y_pos][self.x_pos] = self.char

    