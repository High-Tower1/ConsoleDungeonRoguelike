import time
import random

from colorama import Fore

class Enemy:
    def __init__(self):
        self.char: str = Fore.RED + "%" + Fore.RESET

        self.max_hp: int = 10
        self.hp: int = self.max_hp
        self.damage: int = 3
        self.x_pos: int
        self.y_pos: int
        self.is_dead: bool = False

    # Takes dmg and check if hp below 0
    def take_damage(self, board: list[list[str]], damage: int):
        self.hp -= damage

        if self.hp <= 0 and not self.is_dead:
            self.is_dead = True
            board[self.y_pos][self.x_pos] = " "

            print("You killed the enemy!")

            return self.is_dead

    # Sets enemy position
    def set_position(self, board: list[list[str]]):
        board[self.y_pos][self.x_pos] = self.char

    def move(self, board: list[list[str]]):
        # Sets the target pos to current pos
        target_pos_x = self.x_pos
        target_pos_y = self.y_pos

        # Randomly choose a direction
        direction = random.choice(["up", "down", "left", "right"])

        match direction:
            case "up": target_pos_y -= 1
            case "down": target_pos_y += 1
            case "left": target_pos_x -= 1
            case "right": target_pos_x += 1

        # Checks if there something on the given target pos
        if board[target_pos_y][target_pos_x] != " " != "%":
            return
        else:
            board[self.y_pos][self.x_pos] = " "
            self.x_pos = target_pos_x
            self.y_pos = target_pos_y
            
            self.set_position(board)