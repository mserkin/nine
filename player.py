from board import Board
from enums import PlayerKind
from hand import Hand


class Player:
    def __init__(self, _name, _kind=PlayerKind.HUMAN):
        self.name = _name
        self.hand = Hand()
        self.kind = _kind

    def move(self, board: Board):
        pass
