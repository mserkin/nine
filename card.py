from typing import Optional

from enums import Rank, Suit


class Card:
    def __init__(self, _rank: Rank, _suit: Suit):
        self.rank = _rank
        self.suit = _suit

    def __cmp__(self, other):
        if self.suit.value != other.suit.value:
            raise Exception("Cannot compare cards of different suits")

        if self.rank == other.rank:
            return 0
        if self.rank.value < other.rank.value:
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

    def __hash__(self) -> int:
        return self.suit.value*100 + self.rank.value

    def __str__(self):
        return str(self.rank)+str(self.suit)

    def get_prev(self):
        prev_rank: Optional[Rank] = self.rank.get_prev()
        if not prev_rank:
            return None
        return Card(prev_rank, self.suit)

    def get_next(self):
        next_rank: Optional[Rank] = self.rank.get_next()
        if not next_rank:
            return None
        return Card(next_rank, self.suit)
