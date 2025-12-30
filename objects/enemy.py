import time
import random

from colorama import Fore

class Enemy:
    def __init__(self):
        self.char: str = Fore.YELLOW + "%" + Fore.RESET

        self.max_hp: int = 10
        self.hp: int = self.max_hp
        self.damage: int = 69
        self.detect_range: int = 3

        self.x_pos: int
        self.y_pos: int
        self.is_dead: bool = False

    # Takes dmg and check if hp below 0
    def take_damage(self, board: list[list[str]], damage: int):
        if self.hp - damage < 0:
            damage = self.hp
            self.hp -= damage
        else:
            self.hp -= damage

        if self.hp <= 0 and not self.is_dead:
            self.is_dead = True
            board[self.y_pos][self.x_pos] = " "

            return self.is_dead

    # Sets enemy position
    def set_pos(self, board: list[list[str]]):
        board[self.y_pos][self.x_pos] = self.char

    def get_player_dist(self, board: list[list[str]], player: object) -> int:
        player_dist: int = abs(player.x_pos - self.x_pos) + abs(player.y_pos - self.y_pos)
        return player_dist
    
    def update_char(self, board: list[list[str]], player_dist: int):
        if player_dist <= self.detect_range:
            self.char = Fore.RED + "%" + Fore.RESET
            self.set_pos(board)
        else:
            self.char = Fore.YELLOW + "%" + Fore.RESET
            self.set_pos(board)

    def move(self, board: list[list[str]], player: object):

        # Sub def to update enemy pos
        def update_pos():
            board[self.y_pos][self.x_pos] = " "
            self.x_pos = target_pos_x
            self.y_pos = target_pos_y
            
            self.set_pos(board)

        # Calculates the player dist
        player_dist: int = self.get_player_dist(board, player)

        # Enters chase state if player in range
        if player_dist <= self.detect_range:
            self.update_char(board, player_dist)

            # Sets the delta pos
            dx: int = player.x_pos - self.x_pos
            dy: int = player.y_pos - self.y_pos

            # Checks deltas to determine farthest x/y dist and prioritizes it
            if abs(dx) > abs(dy):
                directions = ["right" if dx > 0 else "left", "down" if dy > 0 else "up"]
            else:
                directions = ["down" if dy > 0 else "up", "right" if dx > 0 else "left"]

            # Adds the remaining directions as fallback when prior direction blocked
            for d in ["up", "down", "left", "right"]:
                if d not in directions:
                    directions.append(d)

        else: # When player is not in range
            self.update_char(board, player_dist)

            # Shuffles the directions
            directions = ["up", "down", "left", "right"]
            random.shuffle(directions)

        for direction in directions:
            # Sets the target pos to current pos
            target_pos_x = self.x_pos
            target_pos_y = self.y_pos

            match direction:
                case "up": target_pos_y -= 1
                case "down": target_pos_y += 1
                case "left": target_pos_x -= 1
                case "right": target_pos_x += 1

            # Checks if there something on the given target pos
            if board[target_pos_y][target_pos_x] == " ":
                update_pos()
                return

            # If player detected, attacks it
            elif board[target_pos_y][target_pos_x] == player.char:
                if player.x_pos != target_pos_x or player.y_pos != target_pos_y:
                    return

                if player.take_damage(board, self.damage):
                    print(f"Enemy hits you for {self.damage} damage, and killed you!")
                    time.sleep(0.4)
                    update_pos()
                    return

                print(f"Enemy hits you for {self.damage} damage!")
                time.sleep(0.4)
                return