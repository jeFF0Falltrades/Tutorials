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


# typedef struct tagRGBQUAD {
#   BYTE rgbBlue;
#   BYTE rgbGreen;
#   BYTE rgbRed;
#   BYTE rgbReserved;
# } RGBQUAD;
@dataclass
class RGBQUAD:
    SIZE = 4
    FORMAT_STR = "<4B"
    rgbBlue: int
    rgbGreen: int
    rgbRed: int
    rgbReserved: int

    def as_tuple(self):
        return (self.rgbRed, self.rgbGreen, self.rgbBlue)

    @classmethod
    def generate(cls, data):
        try:
            if len(data) == 3:
                data = data + (0,)
            return cls(*data)
        except Exception:
            raise Exception("Error unpacking RGBQUAD")
