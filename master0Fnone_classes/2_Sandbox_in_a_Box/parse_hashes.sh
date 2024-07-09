#!/usr/bin/env bash
#
# Author: jeFF0Falltrades
#
# parse_hashes.sh extracts the following hashes for one or more files:
#     - MD5
#     - SHA1
#     - SHA256
#     - SSDEEP/Fuzzy Hash (requires ssdeep to be installed)
#     - Import Hash (requires python and the pefile module to be installed)
#
# MIT License
#
# Copyright (c) 2024 Jeff Archer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
imphash_script="
try:
    from pefile import PE
    file = PE('%s')
    print(file.get_imphash())
except:
    raise SystemExit(0)
"

# Determine which version of Python to run
command -v python3 >/dev/null && PYTHON_BIN=python3 || PYTHON_BIN=python

for filename in $@; do
    basename "$filename"
    md5sum "$filename" | awk ' { print $1 }'
    sha1sum "$filename" | awk ' { print $1 }'
    sha256sum "$filename" | awk ' { print $1 }'
    ssdeep "$filename" | grep -Po "([0-9]+:.*(?=,))"
    printf "$imphash_script" "$filename" | $PYTHON_BIN
done
