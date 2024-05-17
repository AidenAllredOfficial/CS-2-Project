import os
import random
from dataclasses import dataclass

import tsapp



@dataclass
class Card:
    color: str
    face: str


def pick_card_easy(player_hand: list[Card], playable_cards: list[Card]) -> int:
    """
    Returns a randomly picked card from a list of playable cards
    Should not be called with an empty list of playable cards.
    """
    if len(playable_cards) == 0:
        raise ValueError("List of playable cards is empty!")
    else:
        return find_matching_card(random.choice(playable_cards), player_hand)


def find_matching_card(card, cards) -> int:
    for i, c in enumerate(cards):
        if card_match(c, card):
            return i

    return -1


def card_match(card_1: Card, card_2: Card) -> bool:
    if (card_1.color == card_2.color and card_1.face == card_2.face):
        return True
    else:
        return False


def pick_card_medium(hand: list[Card], top_card: Card, playable_cards: list[Card]) -> Card:
    """
    Picks a card from a list of playable card with some slight strategy
    attempts to change the color when it is running out of cards to play.
    """
    output = None
    if len(playable_cards) == 0:
        raise ValueError("List of playable cards is empty!")

    if len(playable_cards) <= 2:  # Attempt to change color if has less than playable cards.
        # If it can change the color
        color_change_cards = filter(lambda card: (card.color != top_card.color), playable_cards)
        if len(color_change_cards) > 0:
            output = random.choice(color_change_cards)
        else:
            output = random.choice(playable_cards)

    else:  # Keep the color the same
        output = random.choice(filter(lambda card: card.color == top_card.color))

    return find_matching_card(output, hand)

# TODO
# def pick_card_hard(hand: list[Card], top_card: Card, playable_cards: list[Card]) -> Card:


def get_card_sprite_back() -> tsapp.Sprite:
    return tsapp.Sprite("assets/BACK_UNO/BACK_UNO.png", 0, 0)


def get_image_path(card) -> str:
    """
    Returns the path to the image file for a Card
    """
    image_path = ""

    match card.face:
        case "skip":
            image_path = os.path.join( "assets", "uno_cards", f"uno_card-{card.color}skip.png")

        case "reverse":
            image_path = os.path.join( "assets", "uno_cards", f"uno_card-{card.color}reverse.png")

        case "+2":
            image_path = os.path.join( "assets", "uno_cards", f"uno_card-{card.color}draw2.png")

        case "+4":
            image_path = os.path.join("assets", "uno_cards", "uno_card-wilddraw4.png")

        case "wild":
            image_path = os.path.join("assets", "uno_cards", "uno_card-wildchange.png")

        case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
            image_path = os.path.join("assets", "uno_cards", f"uno_card-{card.color}{card.face}.png")

        case _:
            raise ValueError(f"{card.color}:{card.face} is invalid.")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"image path {image_path} does not exist.")

    return image_path


def get_card_sprite(card: Card) -> tsapp.Sprite:
    return tsapp.Sprite(get_image_path(card), 0, 0)

def get_playable_cards(cards: list[Card], top_card: Card, is_drawing: bool) -> list[Card]:
    playable_cards = list()

    if is_drawing:
        for card in cards:
            if top_card.face == "+4" and card.face == "+4":
                playable_cards.append(get_card_copy(card))

            elif top_card.face == "+2" and card.face == "+2":
                playable_cards.append(get_card_copy(card))

    else:
        for card in cards:
            if card_can_place_on(top_card, card):
                playable_cards.append(get_card_copy(card))

    return playable_cards


def card_can_place_on(card_1, card_2) -> bool:
    """
    Function returns whether or not a card can stack on another.
    """

    # Check if a wild or +4
    if card_2.face in ("wild", "+4"):
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
        face = random.choice(( "0", "1", "1", "2", "2", "3", "3", "4", "4", "5", "5", "6", "6", "7", "7", "8", "8", "9", "9", "reverse", "reverse", "+2", "+2", "skip", "skip"))
        color = random.choice(("red", "yellow", "blue", "green"))

        return Card(color=color, face=face)

def gen_numeric_card() -> Card:
    """
    Generates only numeric cards. Used for the first card of the game.
    """
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
        )
    )
    color = random.choice("red", "green", "yellow", "blue")
    return Card(face, color)

def gen_cards(number_of_cards: int) -> tuple[Card, ...]:
    """Generates a specified number of new cards."""
    return tuple((gen_card() for _ in range(number_of_cards)))


def gen_player_hand() -> list[Card]:
    """Generates a standard player hand"""
    return list(gen_cards(7))

def get_card_copy(card: Card) -> Card:
    return Card(card.color, card.face)
