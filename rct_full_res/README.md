# Roller Coaster Tycoon (1999) Full Resolution Game Patch (with Video Tutorial)
Patches the original 1999 Roller Coaster Tycoon game executable (including expansions Corkscrew Follies and/or Loopy Landscapes) for full resolution on modern systems.

This patch can be used to allow windowed mode to maximize the window to the specified resolution, or (by default) patch the game to run in full screen mode at the specified resolution.

It will create a copy of the Roller Coaster Tycoon executable file, and it will not modify the original executable, so you needn't worry about breaking your base installation.

# Video Tutorial
For a full walkthrough of how this patch was created, and a general introduction to reverse engineering and game patching, see the accompanying video:

[Reverse Engineering/Game Patching Tutorial: Full Res Roller Coaster Tycoon with Ghidra+x64dbg+Python](https://youtu.be/cwBoUuy4nGc)

# Installation
## Python
* Download [Python](https://www.python.org/downloads/) (Python 3+ preferred)
* Follow the usage instructions below to run the patch program
## EXE
* Download `rct_patch.exe`
* Run the executable with the same options shown below, e.g. 

```
$ ./rct_patch.exe auto -w -t ~/Downloads/RCT/RCT.EXE  1920 1080 -o ~/Downloads/RCT/rct_patched.exe
```

# Usage
## Checking an Executable for Compatibility
```
$ python rct_patch.py check -h
usage: rct_patch.py check [-h] [-t TARGET]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Full path to RCT.EXE (defaults to local directory)
```

The `check` command can be used to first test if an executable can be patched using this script. 

It performs a (lazy) check to ensure the byte sequences to be patched are present in the file.

The target file should be your primary Roller Coaster Tycoon executable (RCT.exe).


**Successful Check**
```
$ python rct_patch.py check -t ~/Downloads/RCT/RCT.EXE
Success!
```

**Unsuccessful Check**
```
$ python rct_patch.py check -t ~/Downloads/not_rct.exe 
File failed offset check: ~/not_rct.exe. Use manual mode for replacements or modify patching script.
```

## Using Manual Mode to Retrieve Replacement Strings
```
$ python rct_patch.py manual -h
usage: rct_patch.py manual [-h] width height

positional arguments:
  width       Your desired resolution width
  height      Your desired resolution height

optional arguments:
  -h, --help  show this help message and exit
```

You can use the `manual` command to specify a desired width and height, and the patch will show the strings to find and replace in the Roller Coaster Tycoon file (using a hex editor), along with which strings to replace them with:

```
$ python rct_patch.py manual 1920 1080

Search String
        --> Replacement


E8 86 7A FF FF
        --> E8 33 7A FF FF

00 05 00 00 0F 8E 07 00 00 00 C7 45 FC 00 05 00 00 81 7D F4 00 04 00 00 0F 8E 07 00 00 00 C7 45 F4 00 04 00 00
        --> 80 07 00 00 0F 8E 07 00 00 00 C7 45 FC 80 07 00 00 81 7D F4 38 04 00 00 0F 8E 07 00 00 00 C7 45 F4 38 04 00 00

Success!
```

Note that for "Windowed Mode", only the second string (`00 05...`) needs to be replaced.

# Using Automatic Mode to Patch Easily
```
$ python rct_patch.py auto -h
usage: rct_patch.py auto [-h] [-t TARGET] [-o OUTFILE] [-w] width height

positional arguments:
  width                 Your desired resolution width
  height                Your desired resolution height

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Full path to RCT.EXE (defaults to local directory)
  -o OUTFILE, --outfile OUTFILE
                        Desired output file name (defaults to `rct_patched.exe`)
  -w, --windowed        Patch for windowed mode only
```

The `auto` command be used to patch the primary Roller Coaster Tycoon executable automatically for either full screen play or windowed play (where windowed mode is patched to maximize the window to the specified resolution):

**Patching for Full Screen Mode**
```
$ python rct_patch.py auto -t ~/Downloads/RCT/RCT.EXE  1920 1080 -o ~/Downloads/RCT/rct_patched.exe

```

**Patching for Windowed Mode**
```
$ python rct_patch.py auto -w -t ~/Downloads/RCT/RCT.EXE  1920 1080 -o ~/Downloads/RCT/rct_patched.exe
```
