# rct_patch.py
#
# Author: jeFF0Falltrades
#
# A patching script for the Roller Coaster Tycoon (1999) game
# executable for play on modern systems at full resolution.
#
# Homepage with Video Tutorial:
# https://github.com/jeFF0Falltrades/Game-Patches/tree/master/rct_full_res
#
# MIT License
#
# Copyright (c) 2020 Jeff Archer
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

from argparse import ArgumentParser, RawTextHelpFormatter
from os.path import isfile

# Dict of both hardcoded and variable values to be checked/patched
PATCHES = {
    'FULL_SCREEN': {
        # Patches default window function to use full screen mode
        'E8 86 7A FF FF': 'E8 33 7A FF FF'
    },
    'WINDOWED': {
        # Patches maximum allowable resolution for windowed mode
        '00 05 00 00 0F 8E 07 00 00 00 C7 45 FC 00 05 00 00 81 7D F4 00 04 00 00 0F 8E 07 00 00 00 C7 45 F4 00 04 00 00':
        '{wl} {wh} 00 00 0F 8E 07 00 00 00 C7 45 FC {wl} {wh} 00 00 81 7D F4 {hl} {hh} 00 00 0F 8E 07 00 00 00 C7 45 F4 {hl} {hh} 00 00'
    }
}


# Gets command line arguments
def getCLAs():
    ap = ArgumentParser(
        description=
        'Roller Coaster Tycoon (1999) Full Resolution Patch by jeFF0Falltrades\n\nHomepage: https://github.com/jeFF0Falltrades/Game-Patches/tree/master/rct_full_res',
        formatter_class=RawTextHelpFormatter)
    sp = ap.add_subparsers(dest='cmd')
    auto = sp.add_parser(
        'auto',
        help=
        'Attempt to patch the program automatically (Patches for full screen mode by default)'
    )
    auto.add_argument('width', help='Your desired resolution width')
    auto.add_argument('height', help='Your desired resolution height')
    auto.add_argument(
        '-t',
        '--target',
        default='RCT.exe',
        help='Full path to RCT.EXE (defaults to local directory)')
    auto.add_argument(
        '-o',
        '--outfile',
        default='rct_patched.exe',
        help='Desired output file name (defaults to `rct_patched.exe`)')
    auto.add_argument('-w',
                      '--windowed',
                      action='store_true',
                      help='Patch for windowed mode only')
    check = sp.add_parser(
        'check', help='Check a file for compatibility with auto-patching mode')
    check.add_argument(
        '-t',
        '--target',
        default='RCT.exe',
        help='Full path to RCT.EXE (defaults to local directory)')
    man = sp.add_parser(
        'manual',
        help=
        'Do not patch the file, just show the necessary hex replacements for manual search/replace with a hex editor'
    )
    man.add_argument('width', help='Your desired resolution width')
    man.add_argument('height', help='Your desired resolution height')
    return ap.parse_args()


# Populates empty dictionary values based on user input
def populateVals(w, h):
    try:
        w = int(w)
        h = int(h)
    except ValueError:
        raise SystemExit(
            'Invalid width and height values received: {}x{}'.format(
                args.width, args.height))

    for key in PATCHES['WINDOWED']:
        PATCHES['WINDOWED'][key] = PATCHES['WINDOWED'][key].format(
            wl=hex(w & 0XFF).replace('0x', '').zfill(2),
            wh=hex((w & 0XFF00) >> 8).replace('0x', '').zfill(2),
            hl=hex(h & 0XFF).replace('0x', '').zfill(2),
            hh=hex((h & 0XFF00) >> 8).replace('0x', '').zfill(2))


# Checks if default values are found in target file
def fileCheck(fp):
    data = ''
    with open(fp, 'rb') as f:
        data = f.read()
    for key in PATCHES:
        for def_val in PATCHES[key]:
            if data.find(bytearray.fromhex(def_val)) == -1:
                return False
    return True


# Prints hex string replacements for manual patching
def printReplacements():
    print('\n{}\n\t--> {}\n\n'.format('Search String', 'Replacement'))
    for key in PATCHES:
        for k, v in PATCHES[key].items():
            print('{}\n\t--> {}\n'.format(k, v))


# Patches for full screen mode
def patchFullScreen(fp, outfile):
    data = ''
    with open(fp, 'rb') as f:
        data = f.read()
    for key in PATCHES:
        for k, v in PATCHES[key].items():
            data = data.replace(bytearray.fromhex(k), bytearray.fromhex(v))
    with open(outfile, 'wb') as o:
        o.write(data)


# Patches for windowed mode
def patchWindowed(fp, outfile):
    data = ''
    with open(fp, 'rb') as f:
        data = f.read()
    for k, v in PATCHES['WINDOWED'].items():
        data = data.replace(bytearray.fromhex(k), bytearray.fromhex(v))
    with open(outfile, 'wb') as o:
        o.write(data)


# Checks if file exists and passes predefined checks
def doFileChecks(fp):
    if not isfile(fp):
        raise SystemExit(
            'Cannot find file {}. Check file path and try again'.format(fp))
    if not fileCheck(fp):
        raise SystemExit(
            'File failed offset check: {}. Use manual mode for replacements or modify patching script.'
            .format(fp))


if __name__ == '__main__':
    args = getCLAs()

    if args.cmd == 'check':
        doFileChecks(args.target)

    elif args.cmd == 'manual':
        populateVals(args.width, args.height)
        printReplacements()

    elif args.cmd == 'auto':
        populateVals(args.width, args.height)
        doFileChecks(args.target)
        if args.windowed:
            patchWindowed(args.target, args.outfile)
        else:
            patchFullScreen(args.target, args.outfile)

    else:
        raise SystemExit(
            'Unknown command received. Use `python rct_patch.py -h` for help')

    print('Success!')