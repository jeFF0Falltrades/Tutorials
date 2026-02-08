# Tutorials

## Reverse Engineering

- asyncrat_config_parser: AsyncRAT Malware Config Parser in Python (with Video Tutorial)
- hacking_weaponizing_solitaire: Reverse Engineering and Weaponizing XP Solitaire (with Video Tutorial)
- rct_full_res: Roller Coaster Tycoon (1999) Full Resolution Game Patch (with Video Tutorial)
- rct_horror_mod: Roller Coaster Tycoon (1999) Mod and Tutorial on Graphics Manipulation & Shellcode
- tie-dye-chain-attack: A toy game used to test GPT-5 + GhidraMCP reverse engineering capabilities

###  Disassembly in the D4rk

A YouTube series where we blindly reverse engineer games and other software.

See the README in this directory for all available episodes.

## jeFF0Falltrades master0Fnone Classes

The jeFF0Falltrades master0Fnone Class series is a collection of free, long-form online courses made to make learning topics - like reverse engineering - more accessible (and fun) to everyone.

See the README in this directory for all available classes.

## Machine Learning

- simple_transaction_classifier: Simple Bank/Credit Card Transaction Classification Tool

## How to Download Individual Project Directories

Oftentimes, you may just want to download one, or only a few, of these Tutorial projects, and not the whole repository.

To do so, you can take advantage of Git's `sparse-checkout` command, as such:

```bash
git clone --no-checkout https://github.com/jeFF0Falltrades/Tutorials.git
cd Tutorials
git sparse-checkout init --cone
git sparse-checkout set master0Fnone_classes/1_x86_Demystified
git pull origin master
```

In this example, only the code files in `master0Fnone_classes/1_x86_Demystified` and its subdirectories will be downloaded onto your machine.

If you want to download multiple directories, you must include them all in your `set` command:

```bash
git clone --no-checkout https://github.com/jeFF0Falltrades/Tutorials.git
cd Tutorials
git sparse-checkout init --cone
git sparse-checkout set master0Fnone_classes/1_x86_Demystified asyncrat_config_parser/
git pull origin master
```

If you omit `master0Fnone_classes/1_x86_Demystified` from the above after cloning it with `sparse-checkout`, for example, it will be removed and only `asyncrat_config_parser` will be present.

