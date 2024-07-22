from enums import Rank, Suit


class Card:
    def __init__(self, _rank: Rank, _suit: Suit):
        self.rank = _rank
        self.suit = _suit

    def __cmp__(self, other):
        if self.suit == other.suit and self.rank == other.rank:
            return 0
        if self.suit.value < other.suit.value \
                or self.suit.value == other.suit.value and self.rank.value < other.rank.value:
            return -1
        return 1

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __str__(self):
        return str(self.rank)+str(self.suit)