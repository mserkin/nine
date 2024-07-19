import sys
from enum import Enum
from random import randrange
from typing import Optional

RANK_NAMES: list[str] = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "В", "Д", "К", "Т"]


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

    def __str__(self) -> str:
        return RANK_NAMES[self.value]

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

    @staticmethod
    def from_input(input_str: str) -> Optional['Rank']:
        if input_str not in RANK_NAMES:
            return None
        return Rank(RANK_NAMES.index(input_str))

    @staticmethod
    def count() -> int:
        return len(Rank)


class Suit(Enum):
    SPADES = 0
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3

    def __str__(self):
        names: list[str] = ["♤", "♧", "♢", "♡"]
        return names[self.value]

    @staticmethod
    def from_input(input_str: str) -> Optional['Suit']:
        first_letters: list[str] = ["П", "Т", "Б", "Ч"]
        if input_str[0] not in first_letters:
            return None
        return Suit(first_letters.index(input_str[0]))

    @staticmethod
    def count() -> int:
        return len(Suit)


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


class Board(Hand):
    def __str__(self):
        result: str = ""
        for s in Suit:
            if s in self.suits:
                suit_cards = self.suits[s]
                result += s.__str__() + ':'
                for rank in Rank:
                    card_str = "  "
                    if Card(rank, s) in suit_cards:
                        card_str = rank.__str__().rjust(2, ' ')
                    result += card_str + ' '
                result += "\n"
        return result


class PlayerKind(Enum):
    HUMAN = 0
    COMPUTER = 1


class Player:
    def __init__(self, _name, _kind=PlayerKind.HUMAN):
        self.name = _name
        self.hand = Hand()
        self.kind = _kind


player_list: list[Player] = []
board: Board = Board()


def deal(deck: Hand):
    for i in range(Suit.count() * Rank.count()):
        player_index = i % len(player_list)
        suit: Suit
        while True:
            suit = Suit(randrange(Suit.count()))
            if suit in deck.suits:
                break
        suit_cards: list[Card] = deck.suits[suit]
        card_index = randrange(len(suit_cards))
        card = suit_cards.pop(card_index)
        if len(suit_cards) == 0:
            del deck.suits[suit]
        player_list[player_index].hand.add(card)


def init():
    player_count = int(input("Сколько людей будет играть? >"))
    for i in range(player_count):
        player_list.append(Player(input(f"Введите имя игрока {i + 1} >"), PlayerKind.HUMAN))
    # player_list.append(Player('Компьютер', PlayerKind.COMPUTER))
    deck: Hand = Hand()
    for s in Suit:
        for r in Rank:
            deck.add(Card(r, s))
    deal(deck)


def get_ranks_in_hand_between(hand: Hand, one: Card, other: Card) -> int:
    if one.suit != other.suit:
        return -1
    wing: int = one.rank.get_common_wing(other.rank)
    if wing == 0:
        return -1
    suit_cards: list[Card] = hand.suits[one.suit]
    first_index: int = suit_cards.index(one)
    other_index: int = suit_cards.index(other)
    return abs(other_index - first_index) - 1


def fits_board(card: Card):
    if card.rank == Rank.RANK_9:
        return True
    if card.suit not in board.suits:
        return False
    suit_cards: list[Card] = board.suits[card.suit]
    first_board_card: Card = suit_cards[0]
    last_board_card: Card = suit_cards[len(suit_cards) - 1]
    return card.rank.value == first_board_card.rank.value - 1 \
        or card.rank.value == last_board_card.rank.value + 1


def play():
    global board
    board = Board()
    turn_of_player: int = -1
    card: Optional[Card] = None
    while True:
        turn_of_player += 1
        if turn_of_player == len(player_list):
            turn_of_player = 0
        player = player_list[turn_of_player]
        if player.kind == PlayerKind.HUMAN:
            input(f"Теперь настала очередь ходить игроку {player.name}. Нажмите Enter")
            print("\n" * 40)
            if card:
                print(f"Предыдущий игрок сделал ход: {card.__str__()}")
            elif not board.is_empty():
                print("Предыдущий игрок пропустил ход")

            while True:
                if not board.is_empty():
                    print("Карты на столе: ")
                    print(board)
                else:
                    print("Карт на столе пока нет.")

                if player.kind == PlayerKind.COMPUTER:
                    print(f"Сейчас ход компьютерного игрока под именем {player.name}")
                else:
                    print(f"{player.name}, вот ваши карты:")
                    print(player.hand)

                suit: Suit
                rank: Rank

                print("Каким будет ваш ход?")
                while True:
                    suit_str: str = input("Введите масть карты: П - пики, Т - трефы, Б - буби, Ч - черви, "
                                          "0 - пропустить ход >")
                    suit = Suit.from_input(suit_str)
                    if suit:
                        break
                    if suit_str[0] == '0':
                        break
                    else:
                        print("Увы, вы ввели что-то не то. Попробуйте снова.")

                if not suit:
                    card = None
                    print("Вы пропустили ход.")
                    break

                while True:
                    rank_str = input(
                        "Введите достоинство карты: число от 2 до 10, или В - валет, Д - дама, К - король, Т - туз >")
                    rank = Rank.from_input(rank_str)
                    if rank:
                        break
                    print("Увы, вы ввели что-то не то. Попробуйте снова")

                card = Card(rank, suit)
                if suit not in player.hand.suits or card not in player.hand.suits[suit]:
                    print("Хмммм, жульничать изволите? Да у вас нет такой карты!")
                    print("Попробуйте снова и не пытайтесь больше достать карту из рукова. Всё вижу!")
                    continue

                if not fits_board(card):
                    print("Ни к селу, ни к городу... Вашу карту нельзя выложить на стол")
                    print("Попробуйте снова и больше не пытайтесь пришивать кобыле хост.")
                    continue

                suits: dict[Suit, list[Card]] = player.hand.suits
                suit_cards: list[Card] = suits[suit]
                suit_cards.remove(card)
                if len(suit_cards) == 0:
                    del suits[suit]
                board.add(card)
                if len(suits) == 0:
                    print(f"{player.name} победил, у него не осталось карт!")
                    print("Итоговое расположение карт на столе")
                    print(board)
                    print("Игра закончена!")
                    sys.exit(0)
                break


if __name__ == '__main__':
    init()
    play()
