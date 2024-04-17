#! ./venv/bin/python3
# This is the main file for the project.

### Imports

import tsapp
import os


class UnoCard(tsapp.Sprite):
    """
    Class to manage uno card.
    """

    def __init__(self, color: str, face: str):
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

    def _get_image_path(self) -> str:
        image_path = ""

        if self.face == "skip":
            image_path = os.path.join(
                "assets", "uno_cards", f"uno_card-{self.color}skip.png"
            )

        elif self.face == "reverse":
            image_path = os.path.join(
                "assets", "uno_cards", f"uno_card-{self.color}reverse.png"
            )

        elif self.face == "+2":
            image_path = os.path.join(
                "assets", "uno_cards", f"uno_card-{self.color}draw2.png"
            )

        elif self.face == "+4":
            image_path = os.path.join("assets", "uno_cards", f"uno_card-wilddraw4.png")

        elif self.face == "wild":
            image_path = os.path.join("assets", "uno_cards", f"uno_card-wildchange.png")

        elif int(self.face) in range(0, 10):
            image_path = os.path.join(
                "assets", "uno_cards", f"uno_card-{self.color}{self.face}.png"
            )

        else:
            raise ValueError(f"{self.color}:{self.face} is invalid.")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"image path {image_path} does not exist.")

        return image_path

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

    def can_place_on(self, uno_card) -> bool:
        """
        Method returns whether or not a card can stack on another.
        """

        # Check if a wild or +4
        if self.face in ("wild", "+4"):
            return True

        if self.face == uno_card.face:
            return True

        elif self.color == uno_card.color:
            return True

        else:
            return False

    def __repr__(self) -> str:
        return f"<{self.color}:{self.face}>"

    def __str__(self) -> str:
        return f"{self.color} {self.face}"


def main():
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
    main()
