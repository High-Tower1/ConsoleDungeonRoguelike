from enum import Enum, auto

class GameState(Enum):
    INTRO = auto()
    PLAY = auto()
    WIN = auto()
    LOSE = auto()
    QUIT = auto()

class Turn(Enum):
    Player = auto()
    Enemy = auto()

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()