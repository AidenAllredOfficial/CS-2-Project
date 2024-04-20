#! ./venv/bin/python3
import tsapp
from uno import Deck, Player, UnoCard


def test_stack_check():
    cards = [
        UnoCard("green", "1"),
        UnoCard("green", "2"),
        UnoCard("yellow", "3"),
        UnoCard("red", "4"),
        UnoCard("none", "wild"),
        UnoCard("none", "+4"),
    ]

    for card_1 in cards:
        for card_2 in cards:
            print(f"{card_1} - {card_2}: {card_2.can_place_on(card_1)}")

    window = tsapp.GraphicsWindow()
    card_list = Deck().cards


def test_render_deck(deck):
    window = tsapp.GraphicsWindow(1000, 1000)

    for i, card in enumerate(deck.cards):
        x = i % 10
        y = i // 10

        card.scale = 0.25
        card.x = x * 90
        card.y = y * 90

    for card in deck.cards:
        window.add_object(card)

    while window.is_running:
        window.finish_frame()


def print_deck(deck):
    for card in deck.cards:
        print(str(card))


def render_player_hand(deck: Deck) -> None:
    window = tsapp.GraphicsWindow()
    player = Player()
    player.deal_hand(deck)

    for x, card in enumerate(player.hand):
        card.scale = 0.3
        card.x = x * 120
        window.add_object(card)

    while window.is_running:
        window.finish_frame()


if __name__ == "__main__":
    deck = Deck()
    render_player_hand(deck)
