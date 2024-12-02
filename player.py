from board import Board
from enums import PlayerKind
from hand import Hand
from card import Card

class Player:
    def __init__(self, _name, _kind=PlayerKind.HUMAN):
        self.name = _name
        self.hand = Hand()
        self.kind = _kind

    def get_playable_cards(self, board: Board) -> list[Card]:
        playable_cards: list[Card] = []
        for suit, suit_cards in self.hand.suits.items():
            for card in suit_cards:
                if board.fits_card(card):
                    playable_cards.append(card)
        return playable_cards

    def move(self, board: Board):
        pass
