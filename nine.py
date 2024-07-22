import sys
from random import randrange
from typing import Optional

from board import Board
from card import Card
from computer_player import ComputerPlayer
from enums import Suit, Rank, PlayerKind
from hand import Hand
from human_player import HumanPlayer
from player import Player

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
    player_count = int(input("Сколько игроков будет играть? >"))
    for i in range(player_count):
        player_type_str: str = input(f"Игрок №{i + 1} человек? Да - Д, Нет - Н >")
        player_name: str = input(f"Введите имя игрока {i + 1} >")
        if player_type_str[0].upper() == "Д":
            player_list.append(HumanPlayer(player_name, PlayerKind.HUMAN))
        else:
            player_list.append(ComputerPlayer(player_name, PlayerKind.COMPUTER))
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
            print("\n" * 40)
            input(f"Теперь настала очередь ходить игроку {player.name}. Нажмите Enter")
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

            card = player.move(board)

            suits: dict[Suit, list[Card]] = player.hand.suits
            suit_cards: list[Card] = suits[card.suit]
            suit_cards.remove(card)
            if len(suit_cards) == 0:
                del suits[card.suit]
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
