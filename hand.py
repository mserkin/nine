from card import Card
from enums import Suit


class Hand:
    def __init__(self):
        self.suits = {}

    def is_in_hand(self, card: Card):
        if card.suit in self.suits:
            for c in self.suits[card.suit]:
                if c == card:
                    return True
            else:
                return False

    def add(self, card: Card):
        if card.suit in self.suits:
            suit_cards: list[Card] = self.suits[card.suit]
            index: int
            for index in range(len(suit_cards)):
                if card > suit_cards[index]:
                    continue
                else:
                    suit_cards.insert(index, card)
                    break
            else:
                suit_cards.append(card)
        else:
            self.suits[card.suit] = [card]

    def __str__(self):
        str = ""
        for s in Suit:
            if s in self.suits:
                str += s.__str__() + ':'
                for c in self.suits[s]:
                    str += c.rank.__str__() + ','
                str = str.removesuffix(',') + ';'
                str += "\n"
        return str

    def is_empty(self):
        return len(self.suits) == 0
