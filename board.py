from card import Card
from enums import Rank, Suit
from hand import Hand


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

    def fits_card(self, card: Card):
        if card.rank == Rank.RANK_9:
            return True
        if card.suit not in self.suits:
            return False
        suit_cards: list[Card] = self.suits[card.suit]
        first_board_card: Card = suit_cards[0]
        last_board_card: Card = suit_cards[len(suit_cards) - 1]
        return card.rank.value == first_board_card.rank.value - 1 \
            or card.rank.value == last_board_card.rank.value + 1
