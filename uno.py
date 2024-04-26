import os
import tsapp
import random
from dataclasses import dataclass


@dataclass
class Card:
    color: str
    face: str


def get_image_path(card) -> str:
    """
    Returns the path to the image file for a Card
    """
    image_path = ""

    if card.face == "skip":
        image_path = os.path.join(
            "assets", "uno_cards", f"uno_card-{card.color}skip.png"
        )

    elif card.face == "reverse":
        image_path = os.path.join(
            "assets", "uno_cards", f"uno_card-{card.color}reverse.png"
        )

    elif card.face == "+2":
        image_path = os.path.join(
            "assets", "uno_cards", f"uno_card-{card.color}draw2.png"
        )

    elif card.face == "+4":
        image_path = os.path.join("assets", "uno_cards", "uno_card-wilddraw4.png")

    elif card.face == "wild":
        image_path = os.path.join("assets", "uno_cards", "uno_card-wildchange.png")

    elif int(card.face) in range(0, 10):
        image_path = os.path.join(
            "assets", "uno_cards", f"uno_card-{card.color}{card.face}.png"
        )

    else:
        raise ValueError(f"{card.color}:{card.face} is invalid.")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"image path {image_path} does not exist.")

    return image_path


def get_card_sprite(card: Card) -> tsapp.Sprite:
    return tsapp.Sprite(get_image_path(card), 0, 0)


def card_can_place_on(card_1, card_2) -> bool:
    """
    Function returns whether or not a card can stack on another.
    """

    # Check if a wild or +4
    if card_1.face in ("wild", "+4"):
        return True

    if card_1.face == card_2.face:
        return True

    elif card_1.color == card_2.color:
        return True

    else:
        return False


def gen_card() -> Card:
    """Generates a random new Card"""
    if 1 <= random.randint(1, 100) <= 8:
        face = random.choice(("wild", "+4"))
        return Card(color="none", face=face)
    else:
        face = random.choice(
            (
                "0",
                "1",
                "1",
                "2",
                "2",
                "3",
                "3",
                "4",
                "4",
                "5",
                "5",
                "6",
                "6",
                "7",
                "7",
                "8",
                "8",
                "9",
                "9",
                "reverse",
                "reverse",
                "+2",
                "+2",
            )
        )
        color = random.choice(("red", "yellow", "blue", "green"))

        return Card(color=color, face=face)


def gen_cards(number_of_cards: int) -> tuple[Card, ...]:
    """Generates a specified number of new cards."""
    return tuple((gen_card() for _ in range(number_of_cards)))


def gen_player_hand() -> list[Card]:
    """Generates a standard player hand"""
    return list(gen_cards(7))
