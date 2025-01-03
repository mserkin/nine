import logging
from collections import OrderedDict
from typing import Optional

from board import Board
from card import Card
from enums import Rank, Suit
from player import Player


class ComputerPlayer(Player):
    def move(self, board: Board):
        cards: list[Card] = super().get_playable_cards(board)
        card_dict: dict[Card, int] = {card: -100 for card in cards}
        for card in card_dict:
            estimate: int = self.estimate_card(card)
            card_dict[card] = estimate
        cards_ordered: OrderedDict = OrderedDict(sorted(card_dict.items(),
                                                     key=lambda kv: kv[1], reverse=True))
        print("Оценка карт:", end="")
        for card, estimate in cards_ordered.items():
            print(f"{card}:{estimate} ", end="")
        print("")
        if len(cards_ordered) > 0:
            return next(iter(cards_ordered))
        else:
            return None

    def estimate_card(self, card: Card) -> int:
        wing: int = card.rank.get_wing()
        l_estimate: int = -100
        r_estimate: int = -100
        if wing <= 0:
            l_estimate = self.wing_estimation(card, -1)
        elif wing >= 0:
            r_estimate = self.wing_estimation(card, +1)
        return max(l_estimate, r_estimate)

    def have_next(self, card: Card, wing: int) -> tuple[Optional[Card], bool]:
        """
        Является ли эта карта последней в масти, на руке ли следующая карта
        :param card:
        :param wing:
        :return: 1) Следующая карта если есть на руке, иначе None 2) Эта карта последняя в масти
        """
        suit_cards: list[Card] = self.hand.suits[card.suit]
        next_rank: Rank = card.rank.get_prev() if wing < 0 else card.rank.get_next()
        if not next_rank:
            return None, True
        next_card: Card = Card(next_rank, card.suit)
        return next_card if next_card in suit_cards else None, False

    def count_others_cards(self, card: Card, wing: int, last_card: Card) -> int:
        others_cards: int = 0
        next_card: Card = card
        while True:
            next_rank: Rank = next_card.rank.get_prev() if wing < 0 else next_card.rank.get_next()
            next_card: Card = Card(next_rank, card.suit)
            if next_card == last_card:
                break
            if next_card not in self.hand.suits[card.suit]:
                others_cards += 1
        return others_cards

    def wing_estimation(self, card: Card, wing: int) -> int:
        logging.debug(f"Estimating card: {card.to_ascii_str()}")
        separated_found: bool
        count_to_end: int = card.rank.value - Rank.get_min().value if wing < 0 else Rank.get_max().value - card.rank.value
        logging.debug(f"count_to_end: {count_to_end}")
        distance_to_last: int

        next_card: Optional[Card]
        is_last: bool
        next_card, is_last = self.have_next(card, wing)
        logging.debug(f"next_card: {next_card.to_ascii_str() if next_card else 'None'}, is_last: {is_last}")

        if is_last:
            return 0
        last_card: Card = self.hand.get_last(card.suit, wing)
        logging.debug(f"last_card: {last_card.to_ascii_str()}")
        if last_card == card or next_card and last_card == next_card:
            separated_found = False
            distance_to_last = 0
        else:
            separated_found = self.is_separated(last_card, card, wing)
            distance_to_last = card.rank.value - last_card.rank.value if wing < 0 \
                else last_card.rank.value - card.rank.value
        logging.debug(f"separated_found: {separated_found} distance_to_last: {distance_to_last}")

        if separated_found:
            if next_card:
                logging.debug(f"result is distance_to_last: {distance_to_last}")
                return distance_to_last
            else:
                logging.debug(f"result is distance_to_last + 1: {distance_to_last+1}")
                return distance_to_last + 1
        else:
            if next_card:
                logging.debug("result is 0")
                return 0
            else:
                logging.debug(f"result is -count_to_end: {-count_to_end}")
                return -count_to_end

    def is_separated(self, last_card: Card, card: Card, wing: int) -> bool:
        for r in range(card.rank.value, last_card.rank.value, wing):
            c: Card = Card(Rank(r), card.suit)
            if c not in self.hand.suits[card.suit]:
                logging.debug(f"Separation found - the card on someone other's hand {c.to_ascii_str()}")
                return True
        else:
            logging.debug("Separation not found")
            return False
