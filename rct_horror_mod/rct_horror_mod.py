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
import logging

from argparse import ArgumentParser
from utils.bitmap_extract import bitmap_extract
from utils.dib_palette_dump import dib_palette_dump
from utils.rct_horror_patcher import patch


def parse_args():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser with arguments for 'bitmaps' command
    arg_bitmaps = subparsers.add_parser(
        "bitmaps",
        help=(
            "Given a palette file, CSG1.dat file, and CSG1i.dat file, parse"
            " bitmaps from CSG1.dat and save them to disk"
        ),
    )
    arg_bitmaps.add_argument("path_palette", help="Path to palette file")
    arg_bitmaps.add_argument("path_csg1", help="Path to CSG1.dat file")
    arg_bitmaps.add_argument("path_csg1i", help="Path to CSG1i.dat file")
    arg_bitmaps.add_argument(
        "path_outdir", help="Directory to output extracted bitmaps to"
    )

    # Subparser with arguments for 'dump' command
    arg_dump = subparsers.add_parser(
        "dump",
        help=(
            "Dump palette and DIB data from an active RCT process (WARNING:"
            " Must be run in Windowed mode)"
        ),
    )
    arg_dump.add_argument("path_palette", help="Path to save palette file")
    arg_dump.add_argument("path_dib", help="Path to save DIB file")

    # Subparser with arguments for 'patch' command
    arg_patch = subparsers.add_parser(
        "patch", help='Patch the RCT executable to enable "horror mode"'
    )
    arg_patch.add_argument(
        "-i",
        "--infile",
        default="RCT.EXE",
        help="Path to the RCT executable to modify",
    )
    arg_patch.add_argument(
        "-o",
        "--outfile",
        default="RCT_PATCHED.EXE",
        help=(
            "Path to the patched output executable (NOTE: The default value is"
            " appended with '_PATCHED' to avoid accidental overwriting of"
            " RCT.exe in the same directory; You should specify a different"
            " path or rename the patched executable to 'RCT.exe' to avoid"
            " conflicts in running the game)"
        ),
    )
    # Defaults for these two args are set to the same used in the tutorial video
    arg_patch.add_argument(
        "-b",
        "--selected_bitmap_offset",
        default="b94a0",
        help=(
            'Hex offset to the bitmap/animation to play (default is "Skelly" @'
            " b94a0) instead of an explosion"
        ),
    )
    arg_patch.add_argument(
        "-t",
        "--selected_track",
        default=(
            "C:\Program Files (x86)\Hasbro Interactive\RollerCoaster"
            " Tycoon\Data\CSS25.DAT"
        ),
        help=(
            "Path to the DAT/WAV track to play upon modification (default is"
            " CSS25.DAT at its default Windows location)"
        ),
    )

    # Subparser for 'show' command (requires no arguments)
    subparsers.add_parser(
        "show",
        help=(
            "Display, but don't save, palette and DIB data from an active RCT"
            " process (WARNING: Must be run in Windowed mode)"
        ),
    )

    return parser.parse_args()


# Since all of the calling functions share a similar format, use a Python
# dict to send the args to the correct function based on the command used
FUNC_DISPATCH = {
    "bitmaps": lambda args: bitmap_extract(args),
    "dump": lambda args: dib_palette_dump(args),
    "patch": lambda args: patch(args),
    "show": lambda args: dib_palette_dump(args),
}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        args = parse_args()
        FUNC_DISPATCH[args.command](args)
    except Exception as e:
        logging.exception(e)
