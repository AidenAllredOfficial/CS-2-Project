#! ./venv/bin/python3
# This is the main file for the project.

### Imports

import tsapp


class UnoCard:
    """
    Class to manage uno card.

    'face' type of the card. 'color' is the color of the card.

    Valid values for 'color' are: 'red', 'green', 'blue', 'yellow', and 'none'
    Valid values for 'face' are: numbers 0-9, '+2' '+4', 'wild', 'reverse', and 'skip'
    """

    def __init__(self, color: str, face: str):
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


def main():
    window = tsapp.GraphicsWindow()

    while window.is_running:
        window.finish_frame()


if __name__ == "__main__":
    main()
