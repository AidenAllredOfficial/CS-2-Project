import tsapp
import uno
import os

def clamp(m, v, mx):
    return min(mx, max(m, v))

def destroy_sprite_list(sprites: list[tsapp.Sprite]):
    """Destroys a list of sprites"""
    for sprite in sprites:
        sprite.destroy()


def is_sprite_hover(sprite: tsapp.Sprite) -> bool:
    """
    Returns whether or not a sprite is being hovered on.
    """
    mouse_x, mouse_y = tsapp.get_mouse_position()
    if sprite.x <= mouse_x <= (sprite.x + sprite.width) and sprite.y <= mouse_y <= (
        sprite.y + sprite.height
    ):
        return True
    else:
        return False


def sprite_clicked_released(sprite: tsapp.Sprite) -> bool:
    """
    Returns whether or not a sprite was clicked on last frame (mouse released).
    """
    if tsapp.was_mouse_released() and is_sprite_hover(sprite):
        return True
    else:
        return False


def sprite_clicked_down(sprite: tsapp.Sprite) -> bool:
    """
    Returns whether or not a sprite was clicked on last frame (mouse pressed down).
    """
    if tsapp.is_mouse_down() and is_sprite_hover(sprite):
        return True
    else:
        return False


def is_numeric(string: str) -> bool:
    """Returns True if a string is consists of only numeric characters 0-9"""
    numeric = True
    for char in string:
        if char not in "1234567890":
            numeric = False
            break

    return numeric


def choose_card_prompt(playable_cards: list[uno.Card]) -> uno.Card:
    """Prompts the user to choose a card from the list."""
    while True:
        print("The cards you can play are:")
        print_cards(list(playable_cards))
        chosen_card_index: str = input(
            f"Choose a playable card, 1-{len(playable_cards)}: "
        )

        if not is_numeric(chosen_card_index):
            print("Not a number")
            continue

        elif not (0 <= int(chosen_card_index) <= len(playable_cards)):
            print("Invalid number, try again")
            continue

        chosen_card: uno.Card = playable_cards[int(chosen_card_index) - 1]

        # Make player try again if they pick an incorrect card.
        if chosen_card not in playable_cards:
            print("INVALID CARD, Try again")
            input()
            os.system("cls" if os.name == "nt" else "clear")
            continue

        else:
            return chosen_card


def choose_color_prompt() -> str:
    """Prompts the user for a color and parses it"""
    color = ""
    while True:
        color = input("Choose a color: ").strip().lower()
        if color not in ("red", "green", "blue", "yellow") or color == "":
            print("Invalid Color: try again")

        else:
            break

    return color


def print_cards(hand: list[uno.Card]) -> None:
    """Prints a list of cards to the console nicely"""
    for card in hand:
        print(f"{card.color} {card.face}", end="")
    print()
