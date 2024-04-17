#! ./venv/bin/python3
from main import UnoCard
import tsapp


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


def test_render_cards():
    window = tsapp.GraphicsWindow()
    card_list = list()

    for y, color in enumerate(("red", "green", "yellow", "blue")):
        for x, face in enumerate((str(i) for i in range(10))):
            print(x, y)

            card = UnoCard(color, face)
            card.scale = 0.25
            card.x = x * 100
            card.y = y * 140
            card_list.append(card)

    for card in card_list:
        window.add_object(card)

    while window.is_running:
        window.finish_frame()


if __name__ == "__main__":
    test_render_cards()
