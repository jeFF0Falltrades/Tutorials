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
import structs.bitmap as bitmap
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from os import mkdir
from os.path import isdir, join
from PIL import Image
from struct import iter_unpack
from structs.tgraphicrecord import TGraphicRecord


# Thread-safe function for extracting a single bitmap given its record data from
# CSG1i.dat, a color palette to interpret the bitmap's colors, an output path
# to write the resulting bitmap, and the color entry data from CSG1.dat
def bitmap_dump_thread_safe(bmp_record, palette, path_output, raw_csg1_data):
    try:
        bmp = bitmap.BITMAP.generate(bmp_record, palette, raw_csg1_data)
        img = Image.new(bitmap.MODE_RGB, (bmp.width, bmp.height))
        img.putdata(bmp.data)
        img.save(join(path_output, bmp.filename))
        return True
    except Exception as e:
        logging.exception(
            f"Error unpacking bitmap at {bmp_record.StartAddress}\n{e}"
        )
        return False


# Extract bitmaps, given the relevant data from CSG1.dat and CSG1i.dat and an
# output directory
def bitmap_extract(args):
    if not isdir(args.path_outdir):
        logging.info(
            f"No directory found at {args.path_outdir}, so we made one..."
        )
        mkdir(args.path_outdir)

    # Open and parse the color palette file
    logging.info(f"Parsing palette from {args.path_palette}...")
    img = Image.open(args.path_palette).convert("RGB")
    palette = list(img.getdata())

    # Load bitmap records from CSG1i.dat into a list
    logging.info(f"Parsing TGraphicRecords from {args.path_csg1i}...")
    with open(args.path_csg1i, "rb") as infile:
        bitmap_records = [
            TGraphicRecord.generate(record_data)
            for record_data in iter_unpack(
                TGraphicRecord.FORMAT_STR, infile.read()
            )
        ]

    logging.info(f"Extracting bitmaps from {args.path_csg1}...")
    with open(args.path_csg1, "rb") as infile:
        raw_csg1_data = infile.read()

    success_count = 0

    # Start a new thread calling bitmap_dump_thread_safe() for each record
    # WARNING: There are ~70K bitmaps packed into the RCT Gold Edition
    # CSG1i.dat file, so this can be time-/resource-intensive
    with ThreadPoolExecutor() as pool:
        success_count = len(
            [
                result
                for result in pool.map(
                    partial(
                        bitmap_dump_thread_safe,
                        palette=palette,
                        path_output=args.path_outdir,
                        raw_csg1_data=raw_csg1_data,
                    ),
                    bitmap_records,
                )
                if result
            ]
        )

    logging.info(
        f"Successfully extracted {success_count} bitmaps to {args.path_outdir}"
    )
