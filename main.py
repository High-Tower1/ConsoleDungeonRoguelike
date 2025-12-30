import os
import time
import random

from state import GameState, Turn, Direction
from objects.player import Player
from objects.enemy import Enemy
from objects.tree import Tree
from objects.hp_pot import HpPot

class Game:
    def __init__(self):
        self.game_state: GameState = GameState.PLAY
        self.turn: Turn = Turn.Player
        self.direction: Direction

        self.rows: int
        self.cols: int
        self.enemy_spawn_amount: int
        self.tree_spawn_amount: int
        self.hp_pots_spawn_amount: int

        # row is vertical (|)
        # col is horizontal (-)

        # for row: creates 12 list inside its own list
        # for col: creates 12 space chars inside for row's list
        # So it creates 12*12 = 144 spaces total

        self.board: list[list[str]] = []
        self.player: Player = None
        self.enemies: list[Enemy] = []
        self.trees: list[Tree] = []
        self.hp_pots: list[HpPot] = []

    def run(self):
        if self.game_state == GameState.INTRO:
            self.clear_console()
            self.intro()
            self.game_state = GameState.PLAY

        # Game loop
        while True:
            if self.game_state == GameState.PLAY:
                self.clear_console()
                self.init_game()

                while True:
                    # Play loop
                    if self.game_state == GameState.PLAY:
                        self.print_game_ui()
                        
                        # Player turn
                        if self.turn == Turn.Player:
                            if self.get_player_input():
                                break # When q pressed

                            # Checks if all enemy dead
                            if len(self.enemies) <= 0:
                                time.sleep(0.5)

                                self.game_state = GameState.WIN
                                break

                            self.turn = Turn.Enemy

                        self.print_game_ui()
                        
                        # Enemy turn
                        if self.turn == Turn.Enemy:
                            for enemy in self.enemies:
                                enemy.move(self.board, self.player)

                            # Checks if player dead
                            if self.player.is_dead:
                                time.sleep(0.5)

                                self.game_state = GameState.LOSE
                                break
                            
                            self.turn = Turn.Player

            # When win
            elif self.game_state == GameState.WIN:
                self.print_game_ui()
                print("You won!")

                input("Press enter to continue...\n")
                time.sleep(1)
                self.clear_console()
                self.game_state = GameState.PLAY
                
            # When lose
            elif self.game_state == GameState.LOSE:
                self.print_game_ui()
                print("You lost!")

                input("Press enter to continue...\n")
                time.sleep(1)
                self.clear_console()
                self.game_state = GameState.PLAY

            # When quit
            elif self.game_state == GameState.QUIT:
                time.sleep(0.5)
                self.clear_console()
                break
            
        print("Thanks for playing!")
        time.sleep(0.5)
        quit()

    # Creates the board
    def create_board(self):
        if self.board:
            self.board.clear()

        self.rows = 12
        self.cols = 12
        print(f"Rows: {self.rows} | Cols: {self.cols}")
        self.board = [[" " for col in range(self.cols)] for row in range(self.rows)]

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

    # Prints the ui
    def print_game_ui(self):
        time.sleep(0.5)
        self.clear_console()
        self.print_board()
        self.player.show_stats()

    # init player
    def init_player(self):
        if self.player:
            del self.player

        self.player = Player()

        #self.player.reset_player(self.board)
        self.player.set_pos(self.board)

    # init enemies
    def init_enemies(self):
        if self.enemies:
            self.enemies.clear()

        self.enemy_spawn_amount = random.randint(3, 5)
        self.enemies = [Enemy() for i in range(self.enemy_spawn_amount)]

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
                    enemy.set_pos(self.board)
                    break
                
            enemy.update_char(self.board, enemy.get_player_dist(self.board, self.player))

    # Init trees
    def init_trees(self):
        if self.trees:
            self.trees.clear()

        self.tree_spawn_amount = random.randint(10, 18)
        self.trees = [Tree() for i in range(self.tree_spawn_amount)]

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
                    tree.set_pos(self.board)
                    break

    # Init hp pots
    def init_hp_pots(self):
        if self.hp_pots:
            self.hp_pots.clear()

        self.hp_pots_spawn_amount = random.randint(1, 2)
        self.hp_pots = [HpPot() for i in range(self.hp_pots_spawn_amount)]

        # Creates trees on random valid positions
        for pot in self.hp_pots:
            while True:
                # Generates random pos from 1 to 10
                rand_x = random.randint(1, self.cols - 2)
                rand_y = random.randint(1, self.rows - 2)

                # Checks if the random pos is empty
                if self.board[rand_y][rand_x] == " ":
                    pot.x_pos = rand_x
                    pot.y_pos = rand_y
                    pot.set_pos(self.board)
                    break

    # init the whole game
    def init_game(self):
        time.sleep(0.5)
        print("Initiating the board...")
        self.create_board()

        time.sleep(0.5)
        self.print_board()

        time.sleep(0.8)
        self.clear_console()
        
        time.sleep(0.5)
        print("Initiating the player, enemy and objects...")
        self.init_player()
        self.init_enemies()
        self.init_trees()
        self.init_hp_pots()

        time.sleep(0.5)
        self.print_board()
        time.sleep(0.5)

    # Tutorial
    def intro(self):
        print("<--- CONSOLE DUNGEON ROGUELIKE --->\n")

        input("Press enter to continue...\n")
        time.sleep(0.5)

        print("----- Tutorial -----")
        print("Objects: ")
        print(f"'{Player().char}' - Player/You (Character that you control)")
        print(f"'{Enemy().char}' - Enemy (Chases and attacks you if you get too close)")
        print(f"'{HpPot().char}' - Health Potion (Heals back your hp)")
        print(f"'{Tree().char}' - Tree (Blocks your path)\n")

        time.sleep(1)

        print("Player Input: ")
        print("Press 'w' to move up")
        print("Press 'a' to move left")
        print("Press 's' to move down")
        print("Press 'd' to move right")
        print("Press 'f' to skip current turn")
        print("Press 'q' to quit\n")

        time.sleep(1)

        print("Objective: Defeat all enemies in each floor to ascend to the next floor, and reach the last floor!")

        print("--------------------\n")
    
        input("Press enter to continue...\n")
        return

    # Get player input
    def get_player_input(self) -> bool:
            while True:
                player_input: str = input("Press your move: ").strip().lower()

                match player_input:
                    case "w": self.player.move(self.board, Direction.UP, self.enemies, self.hp_pots); return False
                    case "a": self.player.move(self.board, Direction.LEFT, self.enemies, self.hp_pots); return False
                    case "s": self.player.move(self.board, Direction.DOWN, self.enemies, self.hp_pots); return False
                    case "d": self.player.move(self.board, Direction.RIGHT, self.enemies, self.hp_pots); return False
                    case "f": self.turn = Turn.Enemy; return False
                    case "q": self.game_state = GameState.QUIT; return True
                    case _: 
                        print("Invalid move!")
                        self.print_game_ui()

    # Clears the terminal/console
    def clear_console(self):
        # 'cls' if on windows (code name 'nt')
        # 'clear' if on mac or linux
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    game = Game()
    game.run()