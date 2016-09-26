[:var_set('', """
# Compile command
aoikdyndocdsl -s README.src.md -n aoikdyndocdsl.ext.all::nto -g README.md
""")
]\
[:HDLR('heading', 'heading')]\
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
[:toc(beg='next', indent=-1)]

## Setup
[:tod()]

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

## Usage
[:tod()]

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

### Specify hotkey config
Create hotkey config file `hotkey_config.py` (see [my hotkey config](https://github.com/AoiKuiyuyou/AoikHotkeyHowto) for ideas):
```
# coding: utf-8
"""
This module contains hotkey spec list.
"""
from __future__ import absolute_import

# Internal imports
from aoikhotkey.util.cmd import Quit
from aoikhotkey.util.cmd import SpecReload
from aoikhotkey.util.efunc import efunc_no_mouse


SPEC = [
    # ----- Event function -----

    # None means event function
    (None, efunc_no_mouse),

    # ----- ESC -----

    # Quit AoikHotkey.
    # Hotkey: ESC
    ('{ESC}', Quit),

    # Reload hotkey spec list.
    # Hotkey: SHIFT+ESC
    ('+{ESC}', SpecReload),

    # ----- F1 -----

    # Open URL.
    # Hotkey: F1
    ('F1', 'https://github.com/'),

    # Open file.
    # Hotkey: CTRL+F1
    ('^F1', 'C:/Windows/win.ini'),

    # Open directory.
    # Hotkey: ALT+F1
    ('!F1', '/'),

    # Open program.
    # Hotkey: WIN+F1
    ('#F1', 'notepad.exe'),
]
```

Run:
```
aoikhotkey -s hotkey_config.py::SPEC
```

### Send notifications to Growl
Run:
```
aoikhotkey -s hotkey_config.py::SPEC -t aoikhotkey.util.growl::hotkey_tfunc
```
