#! ./venv/bin/python3
# This is the main file for the project.

# Imports

import tsapp
import uno
import utils as u
import time

# Config

FONT = "assets/fonts/static/OpenSans-Bold.ttf"
NUM_PLAYERS = 4

# Useful functions


def display_hand(hand: list[uno.Card]):
    "Displays a players hand, returns the list of sprites."
    left_pad = 120
    right_pad = 550
    max_width = WIDTH - (left_pad + right_pad)
    y = HEIGHT - 300

    sprites = list()

    card_scale = 0.45
    card_offset = min(140, max_width // len(hand))

    for i, card in enumerate(hand):
        sprite = uno.get_card_sprite(card)
        x_offset = card_offset * i
        sprite.scale = card_scale
        sprite.x = left_pad + x_offset
        sprite.y = y

        window.add_object(sprite)
        sprites.append(sprite)

    return sprites


def display_top_card(card: uno.Card) -> tsapp.Sprite:
    """
    Places top card on the screen and returns the sprite object.
    """
    sprite = uno.get_card_sprite(card)
    sprite.scale = 0.75
    sprite.x = WIDTH - sprite.width - 100
    sprite.y = 100

    window.add_object(sprite)

    return sprite


def get_deck_hovered_card(cards: list[tsapp.Sprite]) -> int:
    """
    Returns the index of the card that is currently being hovered
    Required because of card sprite overlap
    """

    hovering = (u.is_sprite_hover(sprite) for sprite in cards)
    selected = False
    for i, hover in reversed(tuple(enumerate(hovering))):
        if hover and not selected:
            selected = True
            return i

    return -1


def sound_cardflip():
    sound = tsapp.Sound("assets/sound_files/cardflip_sound.mp3")
    sound.play()


def get_color_from_user() -> str:
    set_status("Select a color")
    sprite_scale = 6
    sprite_size = 64 * sprite_scale
    gap = 16
    x_pos = window.center_x
    y_pos = window.center_y

    red_sprite = tsapp.Sprite("assets/buttons/red_button.png", 0, 0)
    green_sprite = tsapp.Sprite("assets/buttons/green_button.png", 0, 0)
    yellow_sprite = tsapp.Sprite("assets/buttons/yellow_button.png", 0, 0)
    blue_sprite = tsapp.Sprite("assets/buttons/blue_button.png", 0, 0)

    red_sprite.scale = sprite_scale
    green_sprite.scale = sprite_scale
    yellow_sprite.scale = sprite_scale
    blue_sprite.scale = sprite_scale

    red_sprite.x = x_pos - sprite_size - (gap // 2)
    red_sprite.y = y_pos - sprite_size - (gap // 2)

    green_sprite.x = x_pos + (gap // 2)
    green_sprite.y = y_pos - sprite_size - (gap // 2)

    yellow_sprite.x = x_pos - sprite_size - (gap // 2)
    yellow_sprite.y = y_pos + (gap // 2)

    blue_sprite.x = x_pos + (gap // 2)
    blue_sprite.y = y_pos + (gap // 2)

    window.add_object(red_sprite)
    window.add_object(green_sprite)
    window.add_object(yellow_sprite)
    window.add_object(blue_sprite)

    window.finish_frame()

    time.sleep(0.25)

    color = None

    # Await user input
    while window.is_running:
        # Return color of clicked square

        if u.sprite_clicked_released(red_sprite):
            color = "red"

        if u.sprite_clicked_released(green_sprite):
            color = "green"

        if u.sprite_clicked_released(yellow_sprite):
            color = "yellow"

        if u.sprite_clicked_released(blue_sprite):
            color = "blue"

        if color is not None:
            break

        # Fancy Animations

        if u.is_sprite_hover(red_sprite):
            red_sprite.scale = u.clamp(
                sprite_scale, red_sprite.scale + 0.1, sprite_scale * 1.1
            )
        else:
            red_sprite.scale = u.clamp(
                sprite_scale, red_sprite.scale - 0.1, sprite_scale * 1.1
            )

        if u.is_sprite_hover(green_sprite):
            green_sprite.scale = u.clamp(
                sprite_scale, green_sprite.scale + 0.1, sprite_scale * 1.1
            )
        else:
            green_sprite.scale = u.clamp(
                sprite_scale, green_sprite.scale - 0.1, sprite_scale * 1.1
            )

        if u.is_sprite_hover(yellow_sprite):
            yellow_sprite.scale = u.clamp(
                sprite_scale, yellow_sprite.scale + 0.1, sprite_scale * 1.1
            )
        else:
            yellow_sprite.scale = u.clamp(
                sprite_scale, yellow_sprite.scale - 0.1, sprite_scale * 1.1
            )

        if u.is_sprite_hover(blue_sprite):
            blue_sprite.scale = u.clamp(
                sprite_scale, blue_sprite.scale + 0.1, sprite_scale * 1.1
            )
        else:
            blue_sprite.scale = u.clamp(
                sprite_scale, blue_sprite.scale - 0.1, sprite_scale * 1.1
            )

        if color is not None:
            break

        window.finish_frame()

    # Clean up

    red_sprite.destroy()
    green_sprite.destroy()
    yellow_sprite.destroy()
    blue_sprite.destroy()

    window.finish_frame()

    return color


def set_status(text):
    player_text.text = text


def animate_hand_frame():
    selected_index = get_deck_hovered_card(hand_sprites)

    # Animate hovering over sprites
    for i, sprite in enumerate(hand_sprites):
        if selected_index == i:
            sprite.scale = u.clamp(0.45, sprite.scale + 0.03, 0.55)
        else:
            sprite.scale = u.clamp(0.45, sprite.scale - 0.03, 0.55)


def next_turn():
    global current_player
    global hand_sprites
    global hand_cards
    global playable_cards
    global can_play
    global next_player_draw

    # Rolls over once it hits either end
    current_player = (current_player + player_increment) % NUM_PLAYERS
    hand_cards = player_hands[current_player]

    # Destroy old sprites
    u.destroy_sprite_list(hand_sprites)

    # Display sprites
    hand_sprites = display_hand(hand_cards)

    # Set player text
    set_status(f"Player #{current_player + 1} color: {top_card.color}")

    # Placed here for performance
    playable_cards = uno.get_playable_cards(hand_cards, top_card, next_player_draw > 0)

    can_play = True
    print(playable_cards)

    # check drawing

    if next_player_draw > 0 and len(playable_cards) == 0:
        set_status(f"Cannot play draw {next_player_draw} cards")
        can_play = False

        # Update Sprites

        new_cards = uno.gen_cards(next_player_draw)
        for card in new_cards:
            player_hands[current_player].append(card)
            u.destroy_sprite_list(hand_sprites)
            hand_cards = player_hands[current_player]
            hand_sprites = display_hand(hand_cards)
            time.sleep(0.2)
            window.finish_frame()

        next_player_draw = 0

    elif next_player_draw > 0 and len(playable_cards) > 0:
        pass
        # The section that handles cards will handle this fine

    elif next_player_draw == 0 and len(playable_cards) == 0:
        set_status(f"{player_text.text} - You have no cards to play. Draw")
        while window.is_running:
            if u.sprite_clicked_released(deck_sprite):
                player_hands[current_player].append(uno.gen_card())
                hand_cards = player_hands[current_player]
                u.destroy_sprite_list(hand_sprites)
                hand_sprites = display_hand(hand_cards)

                # update playable cards
                playable_cards = uno.get_playable_cards(hand_cards, top_card, False)
                can_play = len(playable_cards) > 0

                break
            animate_hand_frame()

            window.finish_frame()


# initialization stage

window = tsapp.GraphicsWindow(1920, 1080)
window.framerate = 30
WIDTH, HEIGHT = window.width, window.height

# Load Background
background_sprite = tsapp.Sprite("./assets/screens/uno-background2.jpg", 0, 0)

# Zoom background
if background_sprite.width / WIDTH < background_sprite.height / HEIGHT:
    background_sprite.scale = WIDTH / background_sprite.width + 0.01
else:
    background_sprite.scale = (HEIGHT / background_sprite.height) + 0.01

# Reset Background Position
background_sprite.center_x = window.center_x
background_sprite.center_y = window.center_y

window.add_object(background_sprite)

# place deck

deck_sprite = tsapp.Sprite("assets/BACK_UNO/deck.png", 0, 0)
deck_sprite.x = 120
deck_sprite.y = 300

window.add_object(deck_sprite)

# Hand init
player_hands = tuple((uno.gen_player_hand() for _ in range(NUM_PLAYERS)))
current_player = -1
hand_cards = player_hands[current_player]
hand_sprites = display_hand(player_hands[current_player])


# Top card init
top_card = uno.gen_card()
top_card_sprite = display_top_card(top_card)

# Player Text init
player_text = tsapp.TextLabel(FONT, 65, 100, 140, 700, "", (255, 255, 255))
window.add_object(player_text)
set_status(f"Player #{current_player + 1} color: {top_card.color}")

# Misc init
player_increment = 1
next_player_button = tsapp.Sprite("assets/buttons/next_player_button.png", 0, 0)
next_player_button.scale = 1.5
next_player_button.x = WIDTH - next_player_button.width - 40
next_player_button.y = HEIGHT - next_player_button.height - 40
window.add_object(next_player_button)
winner = None
next_player_draw = 0
playable_cards = uno.get_playable_cards(hand_cards, top_card, False)
can_play = True
draw_check = False

next_turn()

# Game Loop
while window.is_running:
    selected_index = get_deck_hovered_card(hand_sprites)

    # Animate hovering over sprites
    for i, sprite in enumerate(hand_sprites):
        if selected_index == i:
            sprite.scale = u.clamp(0.45, sprite.scale + 0.03, 0.55)
        else:
            sprite.scale = u.clamp(0.45, sprite.scale - 0.03, 0.55)

    # Player selects a card.
    if (
        u.sprite_clicked_released(hand_sprites[selected_index])
        and (selected_index != -1)
        and can_play
    ):
        selected_card = hand_cards[selected_index]

        # If player selected correctly
        if selected_card in playable_cards:
            can_play = False
            # play sound effect
            sound_cardflip()
            # Change Top Card
            top_card_sprite.destroy()
            top_card = uno.get_card_copy(player_hands[current_player][selected_index])
            top_card_sprite = display_top_card(top_card)

            window.add_object(top_card_sprite)

            # Remove Card from hand
            player_hands[current_player].pop(selected_index)

            # Rerender Card
            u.destroy_sprite_list(hand_sprites)

            # Detect win
            if len(player_hands[current_player]) > 0:
                hand_cards = player_hands[current_player]
                hand_sprites = display_hand(hand_cards)
            else:
                winner = current_player
                break

            # Execute Card Action
            match selected_card.face:
                case "+2":
                    next_player_draw += 2
                case "skip":
                    current_player += 1
                case "reverse":
                    player_increment *= -1
                case "+4":
                    next_player_draw += 4
                    color = get_color_from_user()
                    top_card = uno.Card(color, selected_card.face)
                    set_status(f"Player #{current_player + 1} color: {top_card.color}")
                case "wild":
                    color = get_color_from_user()
                    top_card = uno.Card(color, selected_card.face)
                    set_status(f"Player #{current_player + 1} color: {top_card.color}")

        for i in range(45):
            animate_hand_frame()
            window.finish_frame()

        next_turn()

    # Next player button
    if u.sprite_clicked_released(next_player_button):
        if can_play:
            set_status(f"{player_text.text} - Play a Card!")
        else:
            next_turn()

    window.finish_frame()

# Display Win screen

win_splash = tsapp.Sprite("assets/screens/uno_win_splash.png", 0, 0)

if win_splash.width / WIDTH < win_splash.height / HEIGHT:
    win_splash.scale = WIDTH / win_splash.width + 0.01
else:
    win_splash.scale = (HEIGHT / win_splash.height) + 0.01

win_splash.center = window.center


window.add_object(win_splash)
win_text = tsapp.TextLabel(
    FONT,
    140,
    WIDTH,
    0,
    window.center_y - 70,
    f"YOU WIN PLAYER #{winner + 1}!!",
    (255, 255, 255),
)
win_text.x = 0
win_text.y = HEIGHT - 70
win_text.width = WIDTH
win_text.align = "center"

window.add_object(win_text)

while window.is_running:
    window.finish_frame()
