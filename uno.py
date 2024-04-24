import os
import tsapp
import random


def get_card_sprite(color, face):
    image_path = ""

    if face == "skip":
        image_path = os.path.join("assets", "uno_cards", f"uno_card-{color}skip.png")

    elif face == "reverse":
        image_path = os.path.join("assets", "uno_cards", f"uno_card-{color}reverse.png")

    elif face == "+2":
        image_path = os.path.join("assets", "uno_cards", f"uno_card-{color}draw2.png")

    elif face == "+4":
        image_path = os.path.join("assets", "uno_cards", "uno_card-wilddraw4.png")

    elif face == "wild":
        image_path = os.path.join("assets", "uno_cards", "uno_card-wildchange.png")

    elif int(face) in range(0, 10):
        image_path = os.path.join("assets", "uno_cards", f"uno_card-{color}{face}.png")

    else:
        raise ValueError(f"{color}:{face} is invalid.")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"image path {image_path} does not exist.")

    return image_path


def card_can_place_on(color_1: str, face_1: str, color_2: str, face_2: str) -> bool:
    """
    Function returns whether or not a card can stack on another.
    """

    # Check if a wild or +4
    if face_1 in ("wild", "+4"):
        return True

    if face_1 == face_2:
        return True

    elif color_1 == color_2:
        return True

    else:
        return False


class UnoCard(tsapp.Sprite):
    """
    Class to manage uno card.
    """

    def __init__(self, color: str, face: str) -> None:
        """
        'face' type of the card. 'color' is the color of the card.

        Valid values for 'color' are: 'red', 'green', 'blue', 'yellow', and 'none'
        Valid values for 'face' are: numbers 0-9, '+2' '+4', 'wild', 'reverse', and 'skip'
        """
        self.color, self.face = color, face

        # Check validity
        if not self._is_valid_color(color):
            raise ValueError(
                f"Card color must be either, red, green, yellow, blue, or none. Recieved {color}"
            )

        if not self._is_valid_face(face):
            raise ValueError(
                f"Card face {face} is invalid, please read the documentation for more info."
            )

        super().__init__(self._get_image_path(), 0, 0)

    def _is_valid_color(self, color: str) -> bool:
        """
        Method returns whether or not the given color is valid.
        """

        return color in ("red", "green", "blue", "yellow", "none")

    def _is_valid_face(self, face: str) -> bool:
        """
        Method returns whether or not the face is a valid face.
        """

        number_cards = (str(i) for i in range(10))
        special_cards = ("+2", "+4", "reverse", "wild", "skip")

        return (face in number_cards) or (face in special_cards)

    def __repr__(self) -> str:
        return f"<{self.color}:{self.face}>"

    def __str__(self) -> str:
        return f"{self.color} {self.face}"

    def get_copy(self):
        """Returns a copy of this uno card"""
        return UnoCard(self.color, self.face)


class Deck:
    def __init__(self) -> None:
        self.cards = list()

        # numbers 1-9
        for color in ("red", "yellow", "green", "blue"):
            for face in tuple(str(i) for i in range(1, 9)) + tuple(
                ("skip", "reverse", "+2")
            ):
                self.cards.append(UnoCard(color, face))
                self.cards.append(UnoCard(color, face))

            self.cards.append(UnoCard(color, "0"))  # Zero Cards

        # Wild and +4
        for _ in range(4):
            self.cards.append(UnoCard("none", "wild"))
            self.cards.append(UnoCard("none", "+4"))

    def draw_cards(self, number: int) -> tuple[UnoCard]:
        pulled_cards: list = list()
        for _ in range(number):
            pulled_cards.append(random.choice(self.cards).get_copy())

        return tuple(pulled_cards)


class Player:
    def __init__(self) -> None:
        self.hand: list[UnoCard] = list()

    def deal_hand(self, deck: Deck) -> None:
        self.hand: list[UnoCard] = list(deck.draw_cards(7))

    def draw_cards(self, deck: Deck, number_of_cards: int) -> None:
        self.hand.extend(list(deck.draw_cards(number_of_cards)))

    def valid_plays(self, top_card: UnoCard, is_drawing: bool) -> tuple[UnoCard]:
        cards = list()
        if not is_drawing:
            for card in self.hand:
                if card.can_place_on(top_card):
                    cards.append(card)

        else:
            if top_card.face == "+2":
                for card in self.hand:
                    if card.face == "+2":
                        cards.append(card)

            elif top_card.face == "+4":
                for card in self.hand:
                    if card.face == "+4":
                        cards.append(card)

        return tuple(cards)
