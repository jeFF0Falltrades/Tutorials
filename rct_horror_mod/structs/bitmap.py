# Author: jeFF0Falltrades

# From the video "Modding RollerCoaster Tycoon into a Peele Horror Film":

#    GitHub: https://github.com/jeFF0Falltrades/Tutorials/tree/master/rct_horror_mod

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
    FLAG_DIRECT = 0x1
    FLAG_COMPACT = 0x5
    FLAG_PALETTE = 0x8
    MODE_RGB = "RGB"
    width: int
    height: int
    data: List[Tuple[int, int, int]]
    filename: str

    @classmethod
    def generate(cls, tgrecord, palette, color_table_data):
        generators = {
            BITMAP.FLAG_PALETTE: BITMAP.generate_palette,
            BITMAP.FLAG_COMPACT: BITMAP.generate_compact,
            BITMAP.FLAG_DIRECT: BITMAP.generate_direct,
        }
        try:
            return generators[tgrecord.Flags](tgrecord, palette, color_table_data)
        except KeyError:
            raise Exception(f"Error unpacking BITMAP: Unknown flag {tgrecord.Flags}")

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
            """
            Corrected multi-segment 8bpp RLE sprite unpacker.

            Why key changes exist:
            - Each scanline may contain multiple RLE segments.
            - MSB of meta byte indicates LAST segment (stop).
            - Decoder must walk segments until the MSB=1 segment.
            """
            TRANSPARENT_ELEMENT = (0, 0, 0)

            # Read 2 bytes per row offset
            header_start = tgrecord.StartAddress
            header_end = header_start + (2 * tgrecord.Height)
            table_header = color_table_data[header_start:header_end]

            # Build list of row-relative offsets
            table_row_offsets = [off[0] for off in iter_unpack("<H", table_header)]

            data = []  # final image pixel array

            # Decode each row
            for row_offset in table_row_offsets:
                scan_line = [TRANSPARENT_ELEMENT] * tgrecord.Width

                # Pointer to first segment of this row
                ptr = tgrecord.StartAddress + row_offset

                while True:
                    meta = color_table_data[ptr]
                    size = meta & 0x7F
                    last_segment = (meta & 0x80) != 0  # stop when 1

                    left = color_table_data[ptr + 1]  # horizontal offset
                    pixel_start = ptr + 2
                    pixel_end = pixel_start + size
                    segment_pixels = color_table_data[pixel_start:pixel_end]

                    # Paint non-transparent segment into row
                    for i, color_idx in enumerate(segment_pixels):
                        scan_line[left + i] = palette[color_idx]

                    # Advance pointer by segment length
                    ptr = pixel_end

                    if last_segment:
                        break

                # Completed scanline → append to output buffer
                data.extend(scan_line)

            # Return constructed image object
            return cls(
                tgrecord.Width,
                tgrecord.Height,
                data,
                f"{tgrecord.StartAddress}_{hex(tgrecord.StartAddress)}.bmp",
            )

        except Exception as e:
            raise Exception(f"Error unpacking compact BITMAP: {e}")

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
                palette_data[tgrecord.xOffset + idx] = RGBQUAD.generate(tup).as_tuple()
            return cls(
                PALETTE_SIZE[0],
                PALETTE_SIZE[1],
                palette_data,
                f"{tgrecord.StartAddress}_{hex(tgrecord.StartAddress)}.bmp",
            )
        except Exception:
            raise Exception("Error unpacking palette BITMAP")
