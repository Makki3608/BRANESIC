# BRANESIC

## What ?

A compiler and higher-level programming language, compiling to '[Branefuck](https://github.com/skirlez/void-stranger-endless-void/wiki/Branefuck)', a modified version of '[Brainfuck](https://esolangs.org/wiki/Brainfuck)' for the level editor mod '[Endless Void](https://github.com/skirlez/void-stranger-endless-void)', for the game '[Void Stranger](https://en.wikipedia.org/wiki/Void_Stranger)'. Aren't hyperlinks fun ?

## Why ?

Because making a programming language is a programming rite of passage. Or so i've been told. And writing a C compiler is boring and too hard. Anyways, maybe this could be useful to anyone making [Endless Void](https://github.com/skirlez/void-stranger-endless-void) levels.

## How do I use it ?

### ~~You can either:~~

~~Download the executable. Run it. ( Not recommended cus you can't modify Config or The Dictionaries. I know that's stupid. Working on that )~~

### Or you can:

Find the release. Extract one of the zips. And run `__main__.py`.
Make sure you have Python installed.

## How do I write something in this novel new programming language ?

Check the wiki :3

## Compatibility ?

<p>The one thing that i'm worried might not work across platforms is the file select popup. I've been told tkinter works everywhere, tho I can't test that claim because I don't have a Windows or Apple PC. ( Yes I am aware Apple doesn't want you to call it a Personal Compuer because they are evil and don't want you to own the thing you paid 5k for. )</p>

## Disclaimer:

<p>This is very unprofessional. I am not a professional. I code for fun like once a year whenever I get the divine visitation required to get me to set my mind on making something. So yeah, this is why it feels kind of scuffed. I don't know how people usually get their programs to not be so cumbersome to use. I'm pretty sure that's a secret they only teach you in university</p>

## TODO List

### The big ones

- Write the wiki.
- Somehow make config.py and bnf_dictionary.py into .json files so that you can just use the executable.
- Add control logic things. ( If, else, while, etc statements ).
- More ways to pass text thru the compiler ( I now what I means ).
  - O(0) static +/-/== ?
- Add persistent memory management.

### Tweaks

- Fix all the typos. 
- Probably more testing.
- Get pyinstall to work.
- Fix `Get_neccessary_workspace_size()`
- Fix # Actons not returning anything.
- Add more useful !functions!

### QOL ideas

- A preprocessing step that would put all the variable initialisations to the start so you can put them anywhere.
- Copy output to clipboard automatically ?
- Set `<r>` automatically.  
- A preprocessing step that would use PEMDAS to turn something like `(x + y ^ 2 * (3 + 1))` to `(x + (y ^ (2 * (3 + 1))))`