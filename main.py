import os
import time
import random

from state import GameState, Direction
from player import Player
from enemy import Enemy
from tree import Tree

class Game:
    def __init__(self):
        self.game_state: GameState = GameState.INTRO
        self.direction: Direction

        self.rows: int = 12
        self.cols: int = 12
        self.enemy_spawn_amount: int = random.randint(1, 1)
        self.tree_spawn_amount: int = random.randint(6, 12)

        # row is vertical (|)
        # col is horizontal (-)

        # for row: creates 12 list inside its own list
        # for col: creates 12 space chars inside for row's list
        # So it creates 12*12 = 144 spaces total

        self.board: list[list[str]] = [[" " for col in range(self.cols)] for row in range(self.rows)]
        self.player = Player()
        self.enemies = [Enemy() for i in range(self.enemy_spawn_amount)]
        self.trees = [Tree() for i in range(self.tree_spawn_amount)]

    def run(self):
        if self.game_state == GameState.INTRO:
            self.intro()
            self.init_game()
            self.game_state = GameState.PLAY

        while True:
            if self.game_state == GameState.PLAY:
                print(f"enemy count: {self.enemy_spawn_amount}")
                print(f"enemies: {self.enemies}")
                self.print_board()
                self.player.show_stats()
                self.get_player_input()
                
                for enemy in self.enemies:
                    enemy.move(self.board)

                # Checks if enemy or player dead
                if len(self.enemies) <= 0:
                    time.sleep(0.5)
                    self.clear_console()

                    self.game_state = GameState.WIN
                    continue # Continue to the next loop

                elif self.player.is_dead:
                    time.sleep(0.5)
                    self.clear_console()

                    self.game_state = GameState.LOSE
                    continue

                time.sleep(0.5)
                self.clear_console()

            elif self.game_state == GameState.WIN:
                print("You won!")
                break

            elif self.game_state == GameState.LOSE:
                print("You lost!")
                break

            elif self.game_state == GameState.QUIT:
                time.sleep(0.5)
                self.clear_console()
                break

        print("Thanks for playing!")
        time.sleep(0.5)
        quit()

    # Creates the board
    def create_board(self):
        # Loop starts at index 0 and ends at the board[0] len
        for col in range(len(self.board[0])):
            # Acceses first row (0)
            self.board[0][col] = "-"

            # Accesses last row (-1)
            self.board[-1][col] = "-"

        # Loop starts at index 1 and ends at the board len - 1
        for row in range(1, len(self.board) - 1): # 1, 10
            # Acceses first col (0)
            self.board[row][0] = "|"

            # Accesses last col (-1)
            self.board[row][-1] = "|"

    # Prints the board
    def print_board(self):
        for row in self.board:
            # Turns the row into str and add spaces betweens
            print(" ".join(row))

    def init_game(self):
        # Creates board
        self.clear_console()
        time.sleep(0.5)
        print("Initiating the board...")
        self.create_board()
        time.sleep(0.5)
        self.print_board()

        time.sleep(0.8)
        self.clear_console()
        
        time.sleep(0.5)
        print("Initiating the player, enemy and objects...")
        # Creates player
        self.player.set_position(self.board)
        
        # Creates enemies on random valid positions
        for enemy in self.enemies:
            while True:
                # Generates random pos from 1 to 10
                rand_x = random.randint(1, self.cols - 2)
                rand_y = random.randint(1, self.rows - 2)

                # Checks if the random pos is empty
                if self.board[rand_y][rand_x] == " ":
                    enemy.x_pos = rand_x
                    enemy.y_pos = rand_y
                    enemy.set_position(self.board)
                    break

        # Creates trees on random valid positions
        for tree in self.trees:
            while True:
                # Generates random pos from 1 to 10
                rand_x = random.randint(1, self.cols - 2)
                rand_y = random.randint(1, self.rows - 2)

                # Checks if the random pos is empty
                if self.board[rand_y][rand_x] == " ":
                    tree.x_pos = rand_x
                    tree.y_pos = rand_y
                    tree.set_position(self.board)
                    break

        time.sleep(0.5)
        self.print_board()

        time.sleep(0.5)
        self.clear_console()

    # Tutorial
    def intro(self):
        print("<--- TERMINAL DUNGEON CRAWLING GAME --->\n")

        input("Press enter to continue...\n")
        time.sleep(0.5)

        print("----- Tutorial -----")
        print("Objects: ")
        print("'@' - Player/You")
        print("'%' - Enemy")
        print("'+' - Health Potion")
        print("'#' - Wall\n")

        time.sleep(1)

        print("Player Input: ")
        print("Press 'w' to move up")
        print("Press 'a' to move left")
        print("Press 's' to move down")
        print("Press 'd' to move right")
        print("Press 'q' to quit\n")

        time.sleep(1)

        print("Objective: Defeat all enemies in each floor to ascend to the next floor, and reach the last floor!")

        print("--------------------\n")
    
        input("Press enter to continue...\n")
        return


    # Get player input
    def get_player_input(self):
            player_input: str = input("Press your move: ").strip().lower()

            match player_input:
                case "w": self.player.move(self.board, Direction.UP, self.enemies, self.enemy_spawn_amount)
                case "a": self.player.move(self.board, Direction.LEFT, self.enemies, self.enemy_spawn_amount)
                case "s": self.player.move(self.board, Direction.DOWN, self.enemies, self.enemy_spawn_amount)
                case "d": self.player.move(self.board, Direction.RIGHT, self.enemies, self.enemy_spawn_amount)
                case "q": self.game_state = GameState.QUIT
                case _: print("Invalid move!")

    # Clears the terminal/console
    def clear_console(self):
        # 'cls' if on windows (code name 'nt')
        # 'clear' if on mac or linux
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    game = Game()
    game.run()