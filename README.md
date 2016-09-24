# AoikHotkey
Python hotkey manager that works on Linux, MacOS, and Windows.

See [my hotkey config](https://github.com/AoiKuiyuyou/AoikHotkeyHowto) for
ideas.

Tested working with:
- Python 2.7 and 3.5
- Linux (X11 with Record Extension)
- Mac OS X 10.11 EI Captain
- Windows XP, Windows 8.1, Windows 10

## Table of Contents
- [Setup](#setup)
  - [Setup via pip](#setup-via-pip)
  - [Setup via git](#setup-via-git)
  - [Setup for MacOS](#setup-for-macos)
  - [Run program](#run-program)

## Setup
- [Setup via pip](#setup-via-pip)
- [Setup via git](#setup-via-git)
- [Setup for MacOS](#setup-for-macos)
- [Run program](#run-program)

### Setup via pip
Run:
```
pip install git+https://github.com/AoiKuiyuyou/AoikHotkey
```

### Setup via git
Run:
```
git clone https://github.com/AoiKuiyuyou/AoikHotkey

cd AoikHotkey

python setup.py install
```

### Setup for MacOS
In my case, installing dependency package `pyobjc` using pip took a long time
to download some sub-packages and eventually got timeout error. I managed
to complete the installation by manually downloading and installing these
sub-packages and re-running `pip install pyobjc`.
  
On MacOS, it is needed to allow the terminal in which AoikHotkey is running to
control your computer. First run AoikHotkey in the terminal, then go to
`System Preferences - Security & Privacy - Accessibility`, and enable the terminal
program in the list.

### Run program
Run:
```
aoikhotkey
```
Or:
```
python -m aoikhotkey
```
Or:
```
python src/aoikhotkey/__main__.py
```
