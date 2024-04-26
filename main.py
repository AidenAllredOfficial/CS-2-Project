#! ./venv/bin/python3
# This is the main file for the project.

### Imports

import tsapp
import uno
import os
import utils as u


def display_hand(hand: list[uno.Card]):
    starting_x = 20
    ending_x = WIDTH - 20
    y = HEIGHT - 200

    card_scale = 0.25

    sprites = list()

    for i, card in enumerate(hand):
        sprite = uno.get_card_sprite(card)
        x_offset = ((WIDTH - 40) / len(hand)) * i
        sprite.scale = card_scale
        sprite.x = starting_x + x_offset
        sprite.y = y

        window.add_object(sprite)
        sprites.append(sprite)

    return sprites


# initialization stage
# Create Player hands

player_hands = tuple((uno.gen_player_hand() for _ in range(4)))

window = tsapp.GraphicsWindow()
WIDTH, HEIGHT = window.width, window.height

game_state = {
    "current_player": 0,
    "game_direction": 1,
    "top_card": None,
}

current_hand = 0
hand_sprites = display_hand(player_hands[current_hand])
while window.is_running:
    if tsapp.was_mouse_pressed():
        current_hand = (current_hand + 1) % len(player_hands)
        u.window_remove_list(hand_sprites)
        hand_sprites = display_hand(player_hands[current_hand])

    window.finish_frame()
