# Reverse Engineering and Weaponizing XP Solitaire (Mini-Course)

## YouTube Video

-

## Contents

```
├───cards_dll_proxy --> CPP and DEF file to create weaponized cards.dll
│       cards.def
│       cards_proxy.cpp
│
├───card_generator --> Python script to generate custom card bitmaps
│       card_generator.py
│       requirements.txt
│
└───example_files --> Example files from the video
        0_C.bmp
        A_H.bmp
        A_S.bmp
        cards.rc
        cards.res
        cards_weaponized.dll
        D_C.bmp
        E_D.bmp
        F_D.bmp
        F_H.bmp
        F_S.bmp
        J_C.bmp
        L_C.bmp
        L_S.bmp
        R_H.bmp
        S_H.bmp
        T_D.bmp
```

## Usage

### Generating Card Bitmaps/RES File

#### Using card_generator.py

```bash
$ python card_generator.py -h
Usage: card_generator.py
Edit script to select text, characters, and suits
```

#### Building the RES File

_Note: Requires windres or rc.exe_

```bash
windres cards.rc  -o cards.res
```

or

```bash
rc.exe /fo cards.res cards.rc
```

### Building the Weaponized DLL

_Note: This is just one method; Visual Studio or another C++ compiler/IDE can be used_

1. [Download MSYS2](https://www.msys2.org/)
2. Run MSYS2 and download GCC and 32/64-bit toolchains:

```
pacman -S mingw-w64-x86_64-gcc
pacman -S --needed base-devel mingw-w64-x86_64-toolchain
pacman -S --needed base-devel mingw-w64-i686-toolchain
```

3. Compile the weaponized DLL:

```bash
g++ -Werror -static -mdll -o cards_weaponized.dll cards_proxy.cpp cards.def
```

## Remember: Use your knowledge and skills for good and fun, not evil (not even evil fun)

Enjoy and please leave questions and feedback on [YouTube](https://www.youtube.com/@jeff0falltrades) or [Mastodon](https://infosec.exchange/@jeFF0Falltrades)!
