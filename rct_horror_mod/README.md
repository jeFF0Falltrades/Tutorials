# RollerCoaster Tycoon Horror Mod (with Video Tutorial)

Contains scripts to:

1. Display or dump color palette and Device-Independent Bitmap (DIB) information
2. Dump all bitmap resources
3. Patch the game so that any explosion results in park visitors clapping, along with replacing the explosion animation with an animation of choice, while playing a WAV file of choice (by default choosing a spooky skull animation and a horror track included with the game), and setting the game window title to "RollerCoaster Diecoon" for extra flair

using the original 1999 Roller Coaster Tycoon Gold Edition game executable.

Enjoy and please leave questions and feedback on [YouTube](https://www.youtube.com/@jeff0falltrades) or [Mastodon](https://infosec.exchange/@jeFF0Falltrades)!

# Video Tutorial

For a full walkthrough of how this mod was created, and a general introduction to reverse engineering and game patching, see the accompanying videos (specifically Part 2 for the code overview):

[Modding RollerCoaster Tycoon into a Peele Horror Film](https://www.youtube.com/watch?v=1MOrjGZ4hbo)

# Installation

## Python

- Clone this repo
- Install requirements: `python -m pip install -r requirements.txt`
- See below for usage notes

# Usage

## General Usage

```
usage: rct_horror_mod.py [-h] {bitmaps,dump,show,patch} ...

positional arguments:
  {bitmaps,dump,show,patch}
    bitmaps             Given a palette file, CSG1.dat file, and CSG1i.dat file, parse bitmaps from CSG1.dat and save them to disk
    dump                Dump palette and DIB data from an active RCT process
    show                Display, but don't save, palette and DIB data from an active RCT process
    patch               Patch the RCT executable to enable "horror mode"

options:
  -h, --help            show this help message and exit
```

## Bitmaps Command

```
usage: rct_horror_mod.py bitmaps [-h] path_palette path_csg1 path_csg1i path_outdir

positional arguments:
  path_palette  Path to palette file
  path_csg1     Path to CSG1.dat file
  path_csg1i    Path to CSG1i.dat file
  path_outdir   Directory to output extracted bitmaps to

options:
  -h, --help    show this help message and exit
```

### Example

```
$ python rct_horror_mod.py bitmaps palette.bmp CSG1.DAT csg1i.dat bitmaps/
INFO:root:Parsing palette from palette.bmp...
INFO:root:Parsing TGraphicRecords from csg1i.dat...
INFO:root:Extracting bitmaps from CSG1.DAT...
INFO:root:Successfully extracted 69917 bitmaps to bitmaps/
```

## Dump Command

```
usage: rct_horror_mod.py dump [-h] path_palette path_dib

positional arguments:
  path_palette  Path to save palette file
  path_dib      Path to save DIB file

options:
  -h, --help    show this help message and exit
```

### Example

```
$ python rct_horror_mod.py dump palette.bmp dib.bmp
INFO:root:DIB Located at: 0xcac0000

INFO:root:BITMAPINFO located at: 0x2b01b98

INFO:root:Parsed the following BITMAPINFOHEADER:
{'biBitCount': 8,
 'biClrImportant': 256,
 'biClrUsed': 256,
 'biCompression': 0,
 'biHeight': -1024,
 'biPlanes': 1,
 'biSize': 40,
 'biSizeImage': 1310720,
 'biWidth': 1280,
 'biXPelsPerMeter': 0,
 'biYPelsPerMeter': 0}

INFO:root:Color Table located at: 0x2b01bc0

INFO:root:Resolution: 640 x 480

INFO:root:Generating palette...

INFO:root:Generating DIB...
```

## Show Command

```
usage: rct_horror_mod.py show [-h]

options:
  -h, --help  show this help message and exit
```

### Example

```
$ python rct_horror_mod.py show
INFO:root:DIB Located at: 0xcac0000

INFO:root:BITMAPINFO located at: 0x2b01b98

INFO:root:Parsed the following BITMAPINFOHEADER:
{'biBitCount': 8,
 'biClrImportant': 256,
 'biClrUsed': 256,
 'biCompression': 0,
 'biHeight': -1024,
 'biPlanes': 1,
 'biSize': 40,
 'biSizeImage': 1310720,
 'biWidth': 1280,
 'biXPelsPerMeter': 0,
 'biYPelsPerMeter': 0}

INFO:root:Color Table located at: 0x2b01bc0

INFO:root:Resolution: 640 x 480

INFO:root:Generating palette...

INFO:root:Generating DIB...
```

## Patch Command

```
usage: rct_horror_mod.py patch [-h] [-i INFILE] [-o OUTFILE] [-b SELECTED_BITMAP_OFFSET] [-t SELECTED_TRACK]

options:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        Path to the RCT executable to modify
  -o OUTFILE, --outfile OUTFILE
                        Path to the patched output executable (NOTE: The default value is appended with '_PATCHED' to avoid accidental overwriting of RCT.exe in the
                        same directory; You should specify a different path or rename the patched executable to 'RCT.exe' to avoid conflicts in running the game)
  -b SELECTED_BITMAP_OFFSET, --selected_bitmap_offset SELECTED_BITMAP_OFFSET
                        Hex offset to the bitmap/animation to play (default is "Skelly" @ b94a0) instead of an explosion
  -t SELECTED_TRACK, --selected_track SELECTED_TRACK
                        Path to the DAT/WAV track to play upon modification (default is CSS25.DAT at its default Windows location)
```

### Example

```
$ python rct_horror_mod.py patch -i RCT.EXE -o patch/RCT.EXE -b b94a0 -t "C:\Program Files (x86)\Hasbro Interactive\RollerCoaster Tycoon\Data\CSS25.DAT"
INFO:root:Attempting to patch program...
INFO:root:Successfully replaced explosion bitmap with bitmap at offset 0xb94a0
INFO:root:Successfully set audio track to C:\Program Files (x86)\Hasbro Interactive\RollerCoaster Tycoon\Data\CSS25.DAT
INFO:root:Shellcode offset 4984514 translated to Virtual Address 0xc412c2
INFO:root:Successfully wrote shellcode to 0xc412c2
INFO:root:Successfully patched call instruction for shellcode
INFO:root:Wrote output file to patch/RCT.EXE
INFO:root:Patch successful!
```
