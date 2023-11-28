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


# Source: https://tid.rctspace.com/csg/csg.html
# TGraphicRecord = packed record
# StartAddress : longword;
# Width, Height, Xoffset, Yoffset : smallint; // signed two byte variables
# Flags : word;
# unused : word // to pad the structure to 16 bytes
# end;
@dataclass
class TGraphicRecord:
    FORMAT_STR = "<L6h"
    SIZE = 16
    StartAddress: int
    Width: int
    Height: int
    xOffset: int
    yOffset: int
    Flags: int
    unused: int

    def __post_init__(self):
        # Only the lower 4 bits of Flags matter
        self.Flags &= 0xF

    @classmethod
    def generate(cls, record_data):
        try:
            return cls(*record_data)
        except Exception:
            raise Exception("Error unpacking TGraphicRecord")
