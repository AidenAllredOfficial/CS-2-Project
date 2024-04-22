#! ./venv/bin/python3
# This is the main file for the project.

### Imports

import uno
import os


def main():
    # Initialization
    player1 = uno.Player()
    player2 = uno.Player()
    player3 = uno.Player()
    player4 = uno.Player()

    players = [player1, player2, player3, player4]

    deck = uno.Deck()

    # Deal out cards
    for player in players:
        player.deal_hand(deck)

    top_card = deck.draw_cards(1)[0]

    # Game loop
    player_index: int = 0
    player_increment: int = 1

    next_player_draw_amount: int = 0
    winning_player: int = -1
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(next_player_draw_amount)

        while True:
            player = players[player_index]
            print(f"### PLAYER {player_index +  1}")
            print(f"The top card is: {top_card}")
            print("Your cards are: ", end="")
            print_cards(list(player.hand))

            playable_cards = player.valid_plays(top_card, next_player_draw_amount > 0)

            has_drawn = False

            # Handle case where player has no playable cards.
            if len(playable_cards) == 0 and next_player_draw_amount == 0:
                print("You have to draw a card because you have no playable cards.")
                player.draw_cards(deck, 1)
                print_cards(player.hand)
                has_drawn = True
                break

            # Handle case that player can play the drawn card.
            if has_drawn:
                drawn_card: uno.UnoCard = player.hand[-1]
                print(f"You drew a {drawn_card}")
                if drawn_card.can_place_on(top_card):
                    print("You can play that card")
                    player.hand.remove(drawn_card)
                    top_card = drawn_card
                    input()
                    break
                else:
                    print("Sorry sucker, you can't play this turn.'")
                    input()
                    break

            # Make player draw cards if they cannot stack and need to draw
            if len(playable_cards) == 0 and next_player_draw_amount > 0:
                print(f"You have to draw {next_player_draw_amount} cards")
                player.draw_cards(deck, next_player_draw_amount)
                print_cards(player.hand)
                input()
                next_player_draw_amount = 0
                break

            chosen_card = choose_card_prompt(list(playable_cards))

            # Card guaranteed to be playable after this point.

            player.hand.remove(chosen_card)
            top_card = chosen_card

            if len(player.hand) <= 0:
                winning_player = player_index
                break

            if chosen_card.face == "skip":
                input()
                player_index += 1
                break

            elif chosen_card.face == "reverse":
                input()
                player_increment *= -1
                break

            elif chosen_card.face == "wild":
                wild_card_color: str = choose_color_prompt()
                top_card.color = wild_card_color
                input()
                break

            elif chosen_card.face == "+4":
                draw_4_color: str = choose_color_prompt()
                top_card.color = draw_4_color
                next_player_draw_amount += 4
                input()
                break

            elif chosen_card.face == "+2":
                next_player_draw_amount += 2
                input()
                break

            else:
                input()
                break

        if winning_player != -1:
            os.system("cls" if os.name == "nt" else "clear")
            print("PLAYER {winning_player + 1} WON!!!!!")
            break

        # Increment counter and roll over once it hits the end.
        player_index += player_increment
        player_index %= len(players)

    print("GAME OVER")


def is_numeric(string: str) -> bool:
    numeric = True
    for char in string:
        if char not in "1234567890":
            numeric = False
            break

    return numeric


def choose_card_prompt(playable_cards: list[uno.UnoCard]) -> uno.UnoCard:
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

        chosen_card: uno.UnoCard = playable_cards[int(chosen_card_index) - 1]

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


def print_cards(hand: list[uno.UnoCard]) -> None:
    print(*hand, sep=", ")


if __name__ == "__main__":
    main()
