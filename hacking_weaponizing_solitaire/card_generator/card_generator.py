#!/usr/bin/env python3
#
# Author: jeFF0Falltrades
#
# From the "Reverse Engineering and Weaponizing XP Solitaire" tutorial:
#    GitHub: https://github.com/jeFF0Falltrades/Tutorials/tree/master/hacking_weaponizing_solitaire
#
#    YouTube:
#
# Requires Pillow:
#     python3 -m pip install Pillow
#
# MIT License
#
# Copyright (c) 2022 Jeff Archer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from enum import Enum
from PIL import Image, ImageDraw, ImageFont, ImageOps
from sys import argv

# This palette is used to use 'P' (palette) mode with Pillow below.
#
# This brings our bit depth down to just 8 bpp per image, which is not as low
# as XP solitaire's images, but is the lowest Pillow supports, so it can help
# avoid "Out of Memory" errors by keeping our images smaller.
#
# The palette uses [r,g,b,r,g,b...] format, so respectively, this palette is:
# [black, red, white]
COLOR_PALETTE = [0, 0, 0, 255, 0, 0, 255, 255, 255]


# An enum class for indexing into COLOR_PALETTE
class Color(Enum):
    BLACK = 0
    RED = 1
    WHITE = 2


# Helper class to keep track of data per card suit
#     idx: Preserved ordering of suits as they appear in cards.dll
#     symbol: Unicode character of card suit
#     color: Color of card suit
#     abbr: Abbreviation of card suit name
class CardSuits(Enum):

    def __init__(self, idx, symbol, color, abbr):
        self.idx = idx
        self.symbol = symbol
        self.color = color
        self.abbr = abbr

    CLUB = (0, '\u2663', Color.BLACK.value, 'C')
    DIAMOND = (1, '\u2666', Color.RED.value, 'D')
    HEART = (2, '\u2665', Color.RED.value, 'H')
    SPADE = (3, '\u2660', Color.BLACK.value, 'S')


# Class representing a single card
class Card:
    # Defaults determined by cards.dll
    CARD_WIDTH = 71
    CARD_HEIGHT = 96
    CARD_COLOR = Color.WHITE.value
    # Add a 1-pixel border of the card's color
    CARD_BORDER = (1, 1, 1, 1)

    FONT = "arial"
    FONT_SIZE = 20

    # x,y coordinates of the card character symbols in the two opposite
    # corners of the card, as well as the suit symbol in the center
    UPPER_LEFT = (5, 0)
    BOTTOM_RIGHT = (CARD_WIDTH - 17, CARD_HEIGHT - 22)
    CENTER = ((CARD_WIDTH / 2) - 5, (CARD_HEIGHT / 2) - 10)

    def __init__(self,
                 character=None,
                 id=None,
                 image=None,
                 suit=None,
                 file_path=None):
        self.character = character
        self.id = self.character if id is None else id
        self.image = image
        self.suit = suit
        self.file_path = file_path

    # This function is commented out in the main program below, but can be used
    # to show the image right as it is generated
    def show(self):
        self.image.show()

    # Writes the image to a BMP file with character and suit (e.g. 3_H.bmp for
    # the 3 of Hearts)
    def write_file(self):
        self.file_path = '{}_{}.bmp'.format(self.character, self.suit.abbr)
        self.image.save(self.file_path, bitmap_format='bmp')


# Gets the ID of the selected card, i.e. which BMP slot it will appear in within
# cards.dll
def get_id(desired_char, desired_suit):
    DEFAULT_IDS = {'K': 13, 'Q': 12, 'J': 11, '10': 10, 'A': 1}

    desired_id = DEFAULT_IDS['K']

    # If it is not a face card or a 10, just subtract it from 10 to find the
    # ID (e.g. (ID of 9) == (ID of 10) - 1)
    if desired_char not in DEFAULT_IDS:
        desired_id = DEFAULT_IDS['10'] - (10 - int(desired_char))
    else:
        desired_id = DEFAULT_IDS[desired_char]

    # Add 13 for each suit we have to traverse to get to the desired suit
    desired_id += 13 * desired_suit.idx
    return desired_id


# Given a string of text, a list of desired card characters, and a list of
# desired suits, generates 1 card for each character of the text, assigned the
# suit and character given by its index in the character and suit lists
def generate_cards(text='K', desired_char_list=None, desired_suit_list=None):
    DEFAULT_CHAR_LIST = [
        'A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2'
    ]
    char_list = DEFAULT_CHAR_LIST if (
        desired_char_list is None
        or len(desired_char_list) == 0) else desired_char_list

    DEFAULT_SUIT_LIST = [suit for suit in CardSuits]
    suit_list = DEFAULT_SUIT_LIST if (
        desired_suit_list is None
        or len(desired_suit_list) == 0) else desired_suit_list

    cards = []
    for idx, character in enumerate(text.upper()):
        # Use modulo here to restart at beginning of suit list if we have
        # more characters than suits
        cur_suit = suit_list[idx % len(suit_list)]

        # We do not use modulo with the character list, because we will
        # overwrite already-written characters
        desired_id = get_id(char_list[idx], cur_suit)

        # Create a new Pillow Image in palette (P) mode
        card_image = Image.new('P', (Card.CARD_WIDTH, Card.CARD_HEIGHT),
                               color=Card.CARD_COLOR)
        # We have to create the Image before assigning it a palette, so now
        # we go ahead and assign it (the previous assigned color will be mapped
        # to the new palette)
        card_image.putpalette(COLOR_PALETTE)
        font = ImageFont.truetype(f'{Card.FONT}.ttf', Card.FONT_SIZE)
        draw = ImageDraw.Draw(card_image)
        draw.text(Card.UPPER_LEFT, character, cur_suit.color, font=font)
        draw.text(Card.BOTTOM_RIGHT, character, cur_suit.color, font=font)
        draw.text(Card.CENTER, cur_suit.symbol, cur_suit.color, font=font)
        card_image = ImageOps.expand(card_image,
                                     border=Card.CARD_BORDER,
                                     fill=cur_suit.color)

        # Add the new Card to our list of cards
        cards.append(Card(character, desired_id, card_image, cur_suit))
    return cards


# Generates the Resource file (.rc) file that will be compiled to our RES file
# (e.g. windres cards.rc  -o cards.res)
def generate_rc_file(cards):
    with open('cards.rc', 'w', encoding='utf-8') as o:
        for card in cards:
            o.write(f'{card.id} BITMAP "{card.file_path}"\n')


# Sample input
# Note that if all the cards need to be one character (like K), you can use
#
# chars = ['K' * len(text)]
#
# and for all cards to be one suit, you can just use
#
# suits = ['D'] as suits will be applied with modulus ops to the cards
text = 'jeFF0Falltrades'
chars = [
    'A', 'A', 'A', 'A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3'
]
suits = []

# Use the text specified via command line, if given, else use the hardcoded text
if len(argv) > 1:
    if argv[1] in ['-h', '--help']:
        print(
            'Usage: card_generator.py\nEdit script to select text, characters, and suits'
        )
        raise SystemExit(0)
    text = argv[1]

# Generate and save cards, then generate the .rc file
cards = generate_cards(text, chars, suits)
for card in cards:
    # card.show()
    card.write_file()
generate_rc_file(cards)