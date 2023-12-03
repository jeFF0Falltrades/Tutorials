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

from pefile import PE
from struct import pack

# Some tuples to contain the bytes we wish to replace, and the bytes we will
# replace them with
#
# Using the "hex string" approach here requires us to take some extra steps
# when working with these (like the len_hex_string() function below) but
# I like this format of hex strings for the readability it provides

# Replacement string which will contain the offset to the
# bitmap to replace the default "explosion" bitmap
REPLACEMENT_BITMAP = ("81 C3 75 FA 00 00", "81 C3 %s")

# Swap:
#     call    ds:funcs_408559[ebp*4]
# With:
#     mov     eax, offset <our shellcode offset>
#     call    eax
REPLACEMENT_PATCH_CALL = ("FF 14 AD A4 70 42 00", "B8 %s FF D0")

# Find a location in DATASEG segment of the executable with enough
# null bytes to write our shellcode, which becomes:
#
# call    ds:funcs_408559[ebp*4] (original call we overwrote)
# pusha (save all registers to the stack to restore after mod)
# push    0
# push    0
# push    0
# push    offset <our audio track path string>
# call    ds:mciSendStringA (open audio WAV with mciSendString)
# push    0
# push    0
# push    0
# push    offset aPlayHorrorTo15 ; "play horror to 15000"
# call    ds:mciSendStringA (play first 15 seconds of audio track)
# mov     eax, offset sub_438B96
# call    eax ; sub_438B96 (call "applause" function)
# popa    (restore the original register states from the stack)
# retn    (return to the regular program flow)
REPLACEMENT_SHELLCODE = (
    "03 00 02 00 01 00" + "00" * 80,
    (
        "FF 14 AD A4 70 42 00 60 6A 00 6A 00 6A 00 68 %s FF 15 14 B3 78 00 6A"
        " 00 6A 00 6A 00 68 %s FF 15 14 B3 78 00 B8 96 8B 43 00 FF D0 61 C3"
    ),
)

# "open <our audio track path> type waveaudio alias horror"
MCISENDSTR_OPEN = (
    "6F 70 65 6E 20 22 %s 22 20 74 79 70 65 20 77 61 76 65 61 75 64 69 6F 20 61"
    " 6C 69 61 73 20 68 6F 72 72 6F 72 00"
)
# "play horror to 15000"
MCISENDSTR_PLAY = (
    "70 6C 61 79 20 68 6F 72 72 6F 72 20 74 6F 20 31 35 30 30 30 00"
)
SECTION_DATASEG = "DATASEG"


# Since we'll be re-using the same data and a lot of offsets/addresses, it was # easier to put the patch functionality into its own class
class RCTHorrorPatcher:
    def __init__(
        self, infile, outfile, replacement_bitmap, selected_audio_track
    ):
        self.address_shellcode = -1
        self.data = None
        self.infile = infile
        try:
            with open(self.infile, "rb") as infile:
                self.data = infile.read()
        except FileNotFoundError:
            raise Exception(f"Valid input file not found at {self.infile}")
        self.offset_bitmap = -1
        self.offset_shellcode = -1
        self.outfile = outfile
        self.replacement_bitmap = replacement_bitmap
        self.selected_audio_track = selected_audio_track

    # Convert a byte-string to a hex string like those shown above, e.g.
    # b'\xaa\xbb\xcc\xdd' becomes "AA BB CC DD"
    #
    # Used with pack(), we can convert to little-endian as well, e.g.
    # byte_to_hex_str(pack("<I", b"\xaa\xbb\xcc\xdd")) -> "DD CC BB AA"
    def byte_to_hex_str(self, byte_str):
        return " ".join(f"{byte:02X}" for byte in byte_str)

    # Calculate the address we should call to run our shellcode by converting
    # the file offset of the shellcode to a Virtual Address; For this we use the
    # pefile library
    def calculate_shellcode_addr(self):
        pe = PE(self.infile)
        image_base = pe.OPTIONAL_HEADER.ImageBase
        for section in pe.sections:
            if section.Name.strip(b"\x00").decode("utf-8") == SECTION_DATASEG:
                # Virtual Address = file offset - file offset to beginning of
                # section + section's Virtual Address + the base address of
                # the PE
                self.address_shellcode = (
                    self.offset_shellcode
                    - section.PointerToRawData
                    + section.VirtualAddress
                    + image_base
                )
        logging.info(
            f"Shellcode offset {self.offset_shellcode} translated to Virtual"
            f" Address {hex(self.address_shellcode)}"
        )

    # Get the length of a hex string like those shown above - removing any
    # formatting placeholders and space, and dividing by 2 since each byte
    # takes 2 chars
    def len_hex_string(self, hex_str):
        return int(
            len((hex_str % tuple(" " * hex_str.count("%s"))).replace(" ", ""))
            / 2
        )

    # Make a bad pun in the window title (because we can)
    def make_bad_pun(self):
        self.data = self.data.replace(
            b"\x00\x00\x00RollerCoaster Tycoon\x00\x00\x00",
            b"\x00\x00\x00RollerCoaster Diecoon\x00\x00",
        )

    # Since Python strings are immutable, we have to re-assign self.data every
    # time we want to modify it; Here, we use join() and string splitting to do
    # a sort of "in-place" insertion at the offset we wish to overwrite
    def overwrite_data(self, offset, new_data):
        self.data = new_data.join(
            [self.data[:offset], self.data[offset + len(new_data) :]]
        )

    # Do ALL the things (to successfully patch the executable)
    def patch(self):
        self.replace_explosion_bitmap()
        self.write_shellcode()
        self.patch_call_instruction()
        self.make_bad_pun()
        self.write_output_file()

    # Patch the instruction "call    ds:funcs_408559[ebp*4]" in the block where
    # the explosion animation is played, and replace it with a call to our mod
    # shellcode
    def patch_call_instruction(self):
        # Find the location of the call to replace by looking for the opcode
        # for "call    ds:funcs_408559[ebp*4]" closest to where the explosion
        # bitmap was replaced
        offset_patch = self.data.find(
            bytes.fromhex(REPLACEMENT_PATCH_CALL[0]),
            self.offset_bitmap,
        )
        self.overwrite_data(
            offset_patch,
            bytes.fromhex(
                REPLACEMENT_PATCH_CALL[1]
                % self.byte_to_hex_str(pack("<I", self.address_shellcode))
            ),
        )
        logging.info("Successfully patched call instruction for shellcode")

    # Replace the bitmap offset from the default explosion bitmap (0xFA75)
    # with our custom bitmap offset
    def replace_explosion_bitmap(self):
        # Shift 4 here as the actual bitmap offsets end in a 0 we don't need
        # (e.g. 0xFA750 is the explosion bitmap offset, but we only need 0xFA75)
        try:
            bitmap_bytes = self.byte_to_hex_str(
                pack("<I", int(self.replacement_bitmap, 16) >> 4)
            )
        except Exception:
            raise Exception(
                "Error unpacking bitmap offset value:"
                f" {self.replacement_bitmap}"
            )
        self.offset_bitmap = self.data.find(
            bytes.fromhex(REPLACEMENT_BITMAP[0])
        )
        if self.offset_bitmap == -1:
            raise Exception("Could not find explosion bitmap offset")
        self.overwrite_data(
            self.offset_bitmap,
            bytes.fromhex(REPLACEMENT_BITMAP[1] % bitmap_bytes),
        )
        logging.info(
            "Successfully replaced explosion bitmap with bitmap at offset"
            f" 0x{self.replacement_bitmap}"
        )

    # Write the modified binary data to the desired output file
    def write_output_file(self):
        try:
            with open(self.outfile, "wb") as outfile:
                outfile.write(self.data)
        except Exception:
            raise Exception(f"Error writing patched data to {self.outfile}")
        logging.info(f"Wrote output file to {self.outfile}")

    # Write the mod shellcode to the DATASEG section
    def write_shellcode(self):
        # Add 8 to skip over \x03\x00...\x00\x00 at shellcode region
        self.offset_shellcode = (
            self.data.find(bytes.fromhex(REPLACEMENT_SHELLCODE[0])) + 8
        )
        if self.offset_shellcode == -1:
            raise Exception("Could not find shellcode placeholder offset")

        # Insert desired audio track path into the mciSendString "open" command
        mciss_open = MCISENDSTR_OPEN % self.byte_to_hex_str(
            self.selected_audio_track.encode("utf-8")
        )
        logging.info(
            f"Successfully set audio track to {self.selected_audio_track}"
        )

        # Calculate the Virtual Address of where our shellcode will go
        self.calculate_shellcode_addr()

        # Address of our mciSendString "open" command string will be the
        # address directly after our shellcode (add 8 bytes here to account for
        # the two 4-byte addresses of the two mciSendString commands we will
        # insert into the shellcode)
        addr_mciss_open = (
            self.address_shellcode
            + self.len_hex_string(REPLACEMENT_SHELLCODE[1])
            + 8
        )

        # The mciSendString "play" command will go right after the "open"
        # command
        addr_mciss_play = addr_mciss_open + self.len_hex_string(mciss_open)

        # Put the shellcode and mciSendString commands together and we got
        # ourselves a complete mod!
        shellcode = (
            REPLACEMENT_SHELLCODE[1]
            % (
                self.byte_to_hex_str(pack("<I", addr_mciss_open)),
                self.byte_to_hex_str(pack("<I", addr_mciss_play)),
            )
            + mciss_open
            + MCISENDSTR_PLAY
        )
        self.overwrite_data(self.offset_shellcode, bytes.fromhex(shellcode))
        logging.info(
            f"Successfully wrote shellcode to {hex(self.address_shellcode)}"
        )


# Run the patcher with the desired inputs
def patch(args):
    logging.info("Attempting to patch program...")
    patcher = RCTHorrorPatcher(
        args.infile,
        args.outfile,
        args.selected_bitmap_offset,
        args.selected_track,
    )
    patcher.patch()
    logging.info("Patch successful!")
