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
import struct

from structs.bitmap import MODE_RGB
from structs.bitmapinfoheader import BITMAPINFOHEADER
from PIL import Image
from structs.rgbquad import RGBQUAD
from structs.windows_process import WindowsProcess


# Helper class to handle parsing graphics data from an active RCT process
class ProcessDumper:
    # 16x16 gives us a nice square bitmap of the active palette
    PALETTE_SIZE = (16, 16)

    def __init__(
        self,
        process_name,
        ptr_ptr_dib,
        offset_to_ptr_bitmapinfo,
        ptr_resolution_x,
        ptr_resolution_y,
    ) -> None:
        # Open the process and unpack values for the DIB and BITMAPINFOHEADER
        # pointers
        self.target_process = WindowsProcess(process_name)
        self.ptr_ptr_dib = self.unpack_from_proc_memory(ptr_ptr_dib)
        self.ptr_dib = self.unpack_from_proc_memory(self.ptr_ptr_dib)
        self.ptr_bitmapinfo = self.unpack_from_proc_memory(
            self.ptr_ptr_dib + offset_to_ptr_bitmapinfo
        )

        # Extract the BITMAPINFOHEADER struct
        self.bitmap_info_header = BITMAPINFOHEADER.generate(
            self.unpack_from_proc_memory(
                self.ptr_bitmapinfo,
                BITMAPINFOHEADER.SIZE,
                BITMAPINFOHEADER.FORMAT_STR,
            )
        )
        # Extract the color table pointer
        self.ptr_color_table = self.ptr_bitmapinfo + BITMAPINFOHEADER.SIZE

        # Build the color palette and DIB
        self.color_palette = self.build_color_palette()
        self.resolution_x, self.resolution_y = self.unpack_from_proc_memory(
            ptr_resolution_x
        ), self.unpack_from_proc_memory(ptr_resolution_y)
        self.dib = self.build_dib()

    # Build the active color palette as a list of RGBQUAD tuples
    def build_color_palette(self):
        color_table_size = (
            self.bitmap_info_header.biClrUsed
            if self.bitmap_info_header.biClrUsed != 0
            else 2**self.bitmap_info_header.biBitCount
        )
        return [
            RGBQUAD.generate(tup).as_tuple()
            for tup in self.unpack_from_proc_memory(
                self.ptr_color_table,
                color_table_size * RGBQUAD.SIZE,
                RGBQUAD.FORMAT_STR,
                True,
            )
        ]

    # Build the DIB by reading in the color indices and mapping them within the
    # active color palette
    def build_dib(self):
        dib_data = self.target_process.read_memory(
            self.ptr_dib,
            (
                self.bitmap_info_header.biWidth
                * self.bitmap_info_header.biHeight
                * -1
            ),
        )
        return [self.color_palette[idx] for idx in dib_data]

    # Generate a bitmap image of the active color palette
    def generate_color_palette(self, save_path="palette.bmp", show_only=False):
        self.generate_img(
            ProcessDumper.PALETTE_SIZE,
            self.color_palette,
            save_path=save_path,
            show_only=show_only,
        )

    # Generate a bitmap image of the active DIB being displayed
    def generate_dib(self, save_path="dib.bmp", show_only=False):
        # Crop needed here to crop out negative space
        self.generate_img(
            (
                self.bitmap_info_header.biWidth,
                self.bitmap_info_header.biHeight * -1,
            ),
            self.dib,
            crop=(0, 0, self.resolution_x, self.resolution_y),
            save_path=save_path,
            show_only=show_only,
        )

    # Show or save a bitmap image, given its pixel data
    def generate_img(
        self,
        img_size,
        img_data,
        crop=None,
        save_path="img.bmp",
        show_only=False,
    ):
        img = Image.new(MODE_RGB, img_size)
        img.putdata(img_data)
        if crop is not None:
            img = img.crop(crop)
        if show_only:
            img.show()
        else:
            img.save(save_path)

    # Unpack binary data from a WindowsProcess object
    def unpack_from_proc_memory(
        self, address, num_bytes=4, format_string="<L", as_iter=False
    ):
        # Iteratively unpack only if specified by caller
        unpack_func = struct.iter_unpack if as_iter else struct.unpack
        try:
            unpacked = unpack_func(
                format_string,
                self.target_process.read_memory(address, num_bytes),
            )
        # Must use Windowed mode as this method does not work in fullscreen
        except struct.error:
            raise Exception(
                "Unpacking failed; Is RCT running in Windowed mode?"
            ) from None
        # If we are only reading a single byte, don't return a list
        if not as_iter:
            if len(unpacked) == 1:
                return unpacked[0]
        return unpacked
