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
import ctypes
from psutil import process_iter


# Read binary data from a specific region of a running Windows process
class WindowsProcess:
    PROCESS_VM_READ = 0x0010

    def __init__(self, process_name) -> None:
        try:
            # Find pid by process name
            self.pid = next(
                (
                    proc.pid
                    for proc in process_iter()
                    if proc.name() == process_name
                )
            )
            self.process_name = process_name
        except StopIteration:
            raise Exception(f"Process '{process_name}' not found.")

    # Read num_bytes bytes from address within the desired process's memory
    def read_memory(self, address, num_bytes):
        try:
            self.process_handle = ctypes.windll.kernel32.OpenProcess(
                self.PROCESS_VM_READ, False, self.pid
            )
            if self.process_handle is None:
                raise Exception(f"Failed to open process {self.process_name}")
            buffer = ctypes.create_string_buffer(num_bytes)
            bytes_read = ctypes.c_ulong(0)
            ctypes.windll.kernel32.ReadProcessMemory(
                self.process_handle,
                address,
                buffer,
                ctypes.sizeof(buffer),
                ctypes.byref(bytes_read),
            )
            ctypes.windll.kernel32.CloseHandle(self.process_handle)
            return buffer.raw[: bytes_read.value]
        except Exception:
            raise Exception(f"Failed to read from {hex(address)}")
