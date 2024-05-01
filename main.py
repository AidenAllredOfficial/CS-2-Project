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

# Load Background
background_sprite = tsapp.Sprite("./assets/screens/uno-background2.jpg", 0, 0)

# Zoom background
if background_sprite.width / WIDTH < background_sprite.height / HEIGHT:
    background_sprite.scale = WIDTH / background_sprite.width
else:
    background_sprite.scale = (HEIGHT / background_sprite.height) + 0.05

# Reset Background Position
background_sprite.center_x = window.center_x
background_sprite.center_y = window.center_y

window.add_object(background_sprite)


game_state = {
    "current_player": 0,
    "game_direction": 1,
    "top_card": None,
}

current_hand = 0
hand_sprites = display_hand(player_hands[current_hand])
while window.is_running:
    for sprite in hand_sprites:
        if u.is_sprite_hover(sprite):
            sprite.scale = 0.3
        else:
            sprite.scale = 0.25

    window.finish_frame()
