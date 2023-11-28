# Author: jeFF0Falltrades

# From the video "Modding RollerCoaster Tycoon into a Peele Horror Film":

#    GitHub: https://github.com/jeFF0Falltrades/Tutorials/tree/main/rct_horror_mod

#    YouTube: https://www.youtube.com/watch?v=1MOrjGZ4hbo

# MIT License

# Copyright (c) 2023 Jeff Archer

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from dataclasses import dataclass
from struct import iter_unpack
from structs.rgbquad import RGBQUAD
from typing import List, Tuple

FLAG_DIRECT = 0x1
FLAG_COMPACT = 0x5
FLAG_PALETTE = 0x8
MODE_RGB = "RGB"


# The structure of bitmaps used by RCT was sourced from:
# https://tid.rctspace.com/csg/csg.html
#
# Handles extracting the 3 types of bitmaps used by RollerCoaster Tycoon:
# 1. Direct bitmaps consisting of color palette entries
# 2. Compact bitmaps consisting of "scan line" rows of both transparent and
#    color pixels
# 3. Color palettes consisting of RGBQUAD structures
@dataclass
class BITMAP:
    width: int
    height: int
    data: List[Tuple[int, int, int]]
    filename: str

    @classmethod
    def generate(cls, tgrecord, palette, color_table_data):
        generators = {
            FLAG_PALETTE: BITMAP.generate_palette,
            FLAG_COMPACT: BITMAP.generate_compact,
            FLAG_DIRECT: BITMAP.generate_direct,
        }
        try:
            return generators[tgrecord.Flags](
                tgrecord, palette, color_table_data
            )
        except KeyError:
            raise Exception(
                f"Error unpacking BITMAP: Unknown flag {tgrecord.Flags}"
            )

    # Extract direct bitmaps, which simply consist of indices into the color
    # palette
    @classmethod
    def generate_direct(cls, tgrecord, palette, color_table_data):
        try:
            color_data = color_table_data[
                tgrecord.StartAddress : tgrecord.StartAddress
                + (tgrecord.Width * tgrecord.Height)
            ]
            return cls(
                tgrecord.Width,
                tgrecord.Height,
                [palette[idx] for idx in color_data],
                f"{tgrecord.StartAddress}_{hex(tgrecord.StartAddress)}.bmp",
            )
        except Exception:
            raise Exception("Error unpacking direct BITMAP")

    # Extract compact bitmaps, which consist of a table of "scan line" rows
    # and their elements
    @classmethod
    def generate_compact(cls, tgrecord, palette, color_table_data):
        TRANSPARENT_ELEMENT = (0, 0, 0)
        try:
            # Read the header containing the offsets to each scan line row
            # This is 2 x the height of the image as each offset is 2 bytes
            table_header = color_table_data[
                tgrecord.StartAddress : tgrecord.StartAddress
                + (2 * tgrecord.Height)
            ]
            # iter_unpack returns a tuple, of which we only need the first
            # element
            table_row_offsets = [
                offset[0] for offset in iter_unpack("<H", table_header)
            ]
            data = []
            last_element = True
            scan_line = []
            # For each scan line
            for offset in table_row_offsets:
                # If we have reached the last element, write the current scan
                # line's elements to data, and create a new, blank scan line
                # of transparent elements
                if last_element:
                    data.extend(scan_line)
                    scan_line = [TRANSPARENT_ELEMENT] * tgrecord.Width
                element_start = tgrecord.StartAddress + offset
                # The first byte of the scan line data is a meta byte, whose
                # most-significant bit (MSB) indicates this is the last element
                # if it is set, and the remainder indicates the size of this
                # scan line, i.e. how many non-transparent elements it contains
                meta_byte = color_table_data[element_start]
                element_size = meta_byte & 0x7F
                # Add 2 here to skip over meta byte and offset-from-left byte
                element_end = element_start + 2 + element_size
                # The byte after the meta byte is an offset from the left edge
                # of the bitmap, i.e. how many transparent elements should
                # precede the first non-transparent element
                offset_from_left = color_table_data[element_start + 1]
                element_data = color_table_data[element_start + 2 : element_end]
                for element_idx, color_idx in enumerate(element_data):
                    # Index into the input palette to decide which color this
                    # element will have
                    scan_line[offset_from_left + element_idx] = palette[
                        color_idx
                    ]
                # Check if this is the last element in this scan line by
                # checking the MSB of the meta byte
                last_element = meta_byte & 0x80
            return cls(
                tgrecord.Width,
                tgrecord.Height,
                data,
                f"{tgrecord.StartAddress}_{hex(tgrecord.StartAddress)}.bmp",
            )

        except Exception:
            raise Exception("Error unpacking compact BITMAP")

    # Extract palette bitmaps, which are made up of RGB color triads in
    # "Blue, Green, Red" order, applied to an identity palette
    @classmethod
    def generate_palette(cls, tgrecord, _, color_table_data):
        BGR_TRIAD_SIZE = 3
        # We will render palette bitmaps in a nice 16x16 square
        PALETTE_SIZE = (16, 16)
        # Build an identity palette
        palette_data = [
            RGBQUAD.generate((i, i, i)).as_tuple()
            for i in range(PALETTE_SIZE[0] * PALETTE_SIZE[1])
        ]
        try:
            palette_entries = color_table_data[
                tgrecord.StartAddress : tgrecord.StartAddress
                + (BGR_TRIAD_SIZE * tgrecord.Width)
            ]
            # Turn palette_entries into a list of [(B,G,R), (B,G,R)..], then
            # convert to RGBQUAD structs
            for idx, tup in enumerate(list(zip(*[iter(palette_entries)] * 3))):
                palette_data[tgrecord.xOffset + idx] = RGBQUAD.generate(
                    tup
                ).as_tuple()
            return cls(
                PALETTE_SIZE[0],
                PALETTE_SIZE[1],
                palette_data,
                f"{tgrecord.StartAddress}_{hex(tgrecord.StartAddress)}.bmp",
            )
        except Exception:
            raise Exception("Error unpacking palette BITMAP")
