from typing import Optional

from card import Card
from enums import Suit, Rank
from player import Player
from board import Board


class HumanPlayer(Player):
    def ask_card(self) -> Optional[Suit]:
        while True:
            card_str: str = input("Введите масть карты: П - пики, Т - трефы, Б - буби, Ч - черви, "
                                  "0 - пропустить ход И достоинство карты: число от 2 до 10, или В - валет, Д - дама, К - король, Т - туз>")

            if len(card_str) == 0:
                print("Повторите!")
                continue

            if card_str[0] == '0':
                return None            

            card_str = card_str.strip()
            suit: Suit = Suit.from_input(card_str[0])

            rank = Rank.from_input(card_str[1:3])
            if not rank or not suit:
                print("Увы, вы ввели что-то не то. Попробуйте снова")
                continue

            return Card(rank, suit)    


    def input_suit(self) -> Optional[Suit]:
        while True:
            suit_str: str = input("Введите масть карты: П - пики, Т - трефы, Б - буби, Ч - черви, "
                                  "0 - пропустить ход >")
            if len(suit_str) == 0:
                print("Повторите!")
                continue

            if suit_str[0] == '0':
                return None

            suit: Suit = Suit.from_input(suit_str)
            if suit:
                return suit
            else:
                print("Увы, вы ввели что-то не то. Попробуйте снова.")

    def input_rank(self) -> Optional[Rank]:
        while True:
            rank_str = input(
                "Введите достоинство карты: число от 2 до 10, или В - валет, Д - дама, К - король, Т - туз >")
            rank = Rank.from_input(rank_str)
            if rank:
                return rank
            print("Увы, вы ввели что-то не то. Попробуйте снова")

    def input_card(self) -> Optional[Card]:
        return self.ask_card()

    def move(self, board: Board):
        print("Каким будет ваш ход?")
        while True:
            card: Optional[Card] = self.input_card()
            if not card:
                cards: list[Card] = super().get_playable_cards(board)
                if cards:
                    print("Пропускаете ход? Странно, вроде бы у вас есть карта, чтобы выложить на стол...")
                    print("Попробуйте еще раз и даже не пытайтесь хитрить")
                    continue

                print("Пропуск хода")

            if card and (card.suit not in self.hand.suits or card not in self.hand.suits[card.suit]):
                print("Хмммм, жульничать изволите? Да у вас нет такой карты!")
                print("Попробуйте снова и не пытайтесь больше достать карту из рукова. Всё вижу!")
                continue

            if card and not board.fits_card(card):
                print("Ни к селу, ни к городу... Вашу карту нельзя выложить на стол")
                print("  Попробуйте снова и больше не пытайтесь пришивать кобыле хост.")
                continue

            return card
