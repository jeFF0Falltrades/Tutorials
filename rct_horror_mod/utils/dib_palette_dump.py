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
import logging
from pprint import pformat
from utils.process_dumper import ProcessDumper


# Offset to the BITMAPINFO struct pointer following the DIB
OFFSET_PTR_BITMAPINFO = 0x88
# Virtual address of the pointer to the DIB pointer
PTR_PTR_DIB = 0x008BCDC4

# Virtual address of the current window resolution
PTR_RESOLUTION_X = 0x00C3E2E4
PTR_RESOLUTION_Y = PTR_RESOLUTION_X + 0x570
TARGET_PROCESS = "RCT.EXE"


# Show or extract the current DIB and color palette from an active RCT process
def dib_palette_dump(args):
    show = args.command == "show"
    path_palette = args.path_palette if "path_palette" in args else None
    path_dib = args.path_dib if "path_dib" in args else None

    # Pass in relevant data to the ProcessDumper class
    rct_process_dumper = ProcessDumper(
        TARGET_PROCESS,
        PTR_PTR_DIB,
        OFFSET_PTR_BITMAPINFO,
        PTR_RESOLUTION_X,
        PTR_RESOLUTION_Y,
    )

    # Read back the data collected by ProcessDumper
    logging.info(f"DIB Located at: {hex(rct_process_dumper.ptr_dib)}\n")
    logging.info(
        f"BITMAPINFO located at: {hex(rct_process_dumper.ptr_bitmapinfo)}\n"
    )
    logging.info(
        "Parsed the following"
        f" BITMAPINFOHEADER:\n{pformat(vars(rct_process_dumper.bitmap_info_header))}\n"
    )
    logging.info(
        f"Color Table located at: {hex(rct_process_dumper.ptr_color_table)}\n"
    )
    logging.info(
        f"Resolution: {rct_process_dumper.resolution_x} x"
        f" {rct_process_dumper.resolution_y}\n"
    )

    # Generate the active color palette and DIB
    logging.info("Generating palette...\n")
    rct_process_dumper.generate_color_palette(
        show_only=show, save_path=path_palette
    )
    logging.info("Generating DIB...\n")
    rct_process_dumper.generate_dib(show_only=show, save_path=path_dib)
