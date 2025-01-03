from enum import Enum
from typing import Optional

RANK_NAMES: list[str] = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "В", "Д", "К", "Т"]
ASCII_RANK_NAMES: list[str] = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


class Rank(Enum):
    RANK_2 = 0
    RANK_3 = 1
    RANK_4 = 2
    RANK_5 = 3
    RANK_6 = 4
    RANK_7 = 5
    RANK_8 = 6
    RANK_9 = 7
    RANK_10 = 8
    RANK_JACK = 9
    RANK_QUEEN = 10
    RANK_KING = 11
    RANK_ACE = 12

    @staticmethod
    def from_input(input_str: str) -> Optional['Rank']:
        if input_str.strip().upper() not in RANK_NAMES:
            return None
        return Rank(RANK_NAMES.index(input_str.strip().upper()))

    @staticmethod
    def count() -> int:
        return len(Rank)

    @staticmethod
    def get_min():
        return Rank.RANK_2

    @staticmethod
    def get_max():
        return Rank.RANK_ACE

    def __cmp__(self, other):
        if self.value == other.value:
            return 0
        if self.value < other.value:
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

    def __str__(self) -> str:
        return RANK_NAMES[self.value]

    def to_ascii_str(self):
        return ASCII_RANK_NAMES[self.value]

    def eval(self) -> int:
        evals = [7, 6, 5, 4, 3, 2, 1, 0, 3, 4, 5, 6, 7]
        return evals[self.value]

    def order(self, wing: int) -> int:
        wing2: list[int] = [0, 1, 2, 3, 4, 5, 6, 7]
        wing_ace: list[int] = [6, 4, 3, 2, 1, 0]
        if wing < 0:
            return wing2[self.value]
        elif wing > 0:
            return wing_ace[self.value - Rank.RANK_9.value]
        else:
            return 0

    def get_prev(self):
        if self.value == 0:
            return None
        return Rank(self.value-1)

    def get_next(self):
        if self.value == 12:
            return None
        return Rank(self.value+1)

    def get_wing(self):
        if self.value < Rank.RANK_9.value:
            return -1
        elif self.value > Rank.RANK_9.value:
            return +1
        else:
            return 0

    def get_common_wing(self, other: 'Rank') -> int:
        if self.value <= Rank.RANK_9.value and other.value <= Rank.RANK_9.value:
            return -1
        elif self.value >= Rank.RANK_9.value and other.value >= Rank.RANK_9.value:
            return +1
        else:
            return 0

    def get_distance(self, target: 'Rank'):
        wing: int = self.get_common_wing(target)
        if wing == 0:
            return 0
        else:
            return self.order(wing) - target.order(wing)



class Suit(Enum):
    SPADES = 0
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    """
        def __eq__(self, other):
            return self.value == other.value
    
        def __ne__(self, other):
            return self.value != other.value
    """
    def __str__(self):
        names: list[str] = ["(П)", "(Т)", "(Б)", "(Ч)"]
        return names[self.value]

    def to_ascii_str(self):
        names: list[str] = ["S", "C", "D", "H"]
        return names[self.value]

    @staticmethod
    def from_input(input_str: str) -> Optional['Suit']:
        first_letters: list[str] = ["П", "Т", "Б", "Ч"]
        if input_str[0].upper() not in first_letters:
            return None
        return Suit(first_letters.index(input_str[0].upper()))

    @staticmethod
    def count() -> int:
        return len(Suit)


class PlayerKind(Enum):
    HUMAN = 0
    COMPUTER = 1
