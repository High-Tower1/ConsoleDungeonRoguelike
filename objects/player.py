import time

from colorama import Fore
from state import Direction

class Player:
    def __init__(self):
        self.char: str = Fore.CYAN + '@' + Fore.RESET

        self.max_hp: int = 30
        self.hp: int = self.max_hp
        self.damage: int = 5
        self.x_pos: int = 1
        self.y_pos: int = 1
        self.is_dead: bool = False

    # Show stats
    def show_stats(self):
        print(f"HP: {self.hp}/{self.max_hp} | Damage: {self.damage}")

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
        
        
    # Heals the player
    def heal(self, heal_amount: int):
        if self.hp == self.max_hp:
            print("You are already at max health!")
            return False
        
        # If hp and healed amount more than max hp, adapt to it
        if self.hp + heal_amount > self.max_hp:
            heal_amount = self.max_hp - self.hp
            self.hp += heal_amount
            print(f"You healed for {heal_amount}hp!")
        else:
            self.hp += heal_amount
            print(f"You healed for {heal_amount}hp!")

        return True

    # Sets player position
    def set_pos(self, board: list[list[str]]):
        board[self.y_pos][self.x_pos] = self.char

    # Moves the player to given pos
    def move(self, board: list[list[str]], direction: Direction, enemies: list, hp_pots: list):

        # Sub def to update player pos
        def update_pos():
            board[self.y_pos][self.x_pos] = " "
            self.x_pos = target_x_pos
            self.y_pos = target_y_pos
            
            self.set_pos(board)

        # Sets the target pos to current pos
        target_x_pos = self.x_pos
        target_y_pos = self.y_pos

        # Imcrement or decrement target pos based on given direction
        match direction:
            case Direction.UP: target_y_pos -= 1
            case Direction.DOWN: target_y_pos += 1
            case Direction.LEFT: target_x_pos -= 1
            case Direction.RIGHT: target_x_pos += 1

        # Checks if there something on the given target pos
        if board[target_y_pos][target_x_pos] == " ":
            update_pos()

        # If enemy detected in the target pos, attacks it
        elif any(enemy.x_pos == target_x_pos and enemy.y_pos == target_y_pos for enemy in enemies): # Loops through enemies to check any enemy in the target pos
            for enemy in enemies:
                if enemy.x_pos != target_x_pos or enemy.y_pos != target_y_pos:
                    continue

                # If enemy is dead, removes it
                if enemy.take_damage(board, self.damage):
                    enemies.remove(enemy)
                    update_pos()

                    print(f"You hit the enemy for {self.damage} damage and killed it!")
                    time.sleep(0.4)
                    return

                print(f"You hit the enemy for {self.damage} damage!")
                time.sleep(0.4)
                return

        elif any(hp_pot.x_pos == target_x_pos and hp_pot.y_pos == target_y_pos for hp_pot in hp_pots):
            for hp_pot in hp_pots:
                if hp_pot.x_pos != target_x_pos or hp_pot.y_pos != target_y_pos:
                    continue

                if self.heal(hp_pot.heal_amount):
                    hp_pots.remove(hp_pot)

                    update_pos()
                    return

        # If anything else detected, cant move
        else:
            print("Path blocked!")
            time.sleep(0.4)
            