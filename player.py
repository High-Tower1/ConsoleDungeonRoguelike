import time

from colorama import Fore
from state import Direction

class Player:
    def __init__(self):
        self.char: str = Fore.YELLOW + '@' + Fore.RESET

        self.max_hp: int = 50
        self.hp: int = self.max_hp
        self.damage: int = 4
        self.x_pos: int = 1
        self.y_pos: int = 1
        self.is_dead: bool = False

    # Show stats
    def show_stats(self):
        print(f"HP: {self.hp}/{self.max_hp} | Damage: {self.damage}")

    # Takes dmg and check if hp below 0
    def take_damage(self, board: list[list[str]], damage: int):
        self.hp -= damage

        if self.hp <= 0 and not self.is_dead:
            self.is_dead = True
            board[self.y_pos][self.x_pos] = " "

    # Sets player position
    def set_position(self, board: list[list[str]]):
        board[self.y_pos][self.x_pos] = self.char

    # Moves the player to given pos
    def move(self, board: list[list[str]], direction: Direction, enemies: list, enemy_count: int):
        # Sets the target pos to current pos
        target_x_pos = self.x_pos
        target_y_pos = self.y_pos

        # Imcrement or decrement target pos based on given direction
        if direction == Direction.UP:
            target_y_pos -= 1
        elif direction == Direction.DOWN:
            target_y_pos += 1
        elif direction == Direction.LEFT:
            target_x_pos -= 1
        elif direction == Direction.RIGHT:
            target_x_pos += 1

        # Checks if there something on the given target pos
        if board[target_y_pos][target_x_pos] == " ":
            board[self.y_pos][self.x_pos] = " "
            self.x_pos = target_x_pos
            self.y_pos = target_y_pos
            
            self.set_position(board)

        # If enemy detected, attacks it
        elif board[target_y_pos][target_x_pos] == Fore.RED + "%" + Fore.RESET:
            for enemy in enemies:
                if enemy.x_pos == target_x_pos and enemy.y_pos == target_y_pos:

                    # If enemy is dead, removes it
                    if enemy.take_damage(board, self.damage):
                        enemies.remove(enemy)
                        enemy_count -= 1

                    print(f"You hit the enemy for {self.damage} damage!")
                    time.sleep(0.4)
                    break

        # If anything else detected, cant move
        else:
            print("Path blocked!")
            time.sleep(0.4)
            