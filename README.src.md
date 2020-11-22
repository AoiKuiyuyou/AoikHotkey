[:var_set('', """
# Compile command
aoikdyndocdsl -s README.src.md -n aoikdyndocdsl.ext.all::nto -g README.md
""")
]\
[:HDLR('heading', 'heading')]\
# AoikHotkey
Python hotkey manager that works on Linux, MacOS, Windows and Cygwin.

See [my hotkey config](https://github.com/AoiKuiyuyou/AoikHotkeyHowto/blob/master/config/spec_main.py) for
ideas.

Tested working with:
- Python 2.7, 3.6, 3.7, 3.8, 3.9
- Linux (X11 with Record Extension)
- Mac OS X 10.15 Catalina
- Windows XP to Windows 10
- Cygwin 2.10.0 64-bit

## Table of Contents
[:toc(beg='next', indent=-1)]

## Setup
[:tod()]

### Setup via pip
Run:
```
pip install AoikHotkey
```

### Setup via git
Run:
```
git clone https://github.com/AoiKuiyuyou/AoikHotkey

cd AoikHotkey

python setup.py install
```

### Setup for MacOS
On MacOS, it is needed to allow the terminal in which AoikHotkey is running to
control your computer. First run AoikHotkey in the terminal, then go to
`System Preferences - Security & Privacy - Accessibility`, and enable the `Terminal`
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
Create hotkey config file `hotkey_config.py` (see [my hotkey config](https://github.com/AoiKuiyuyou/AoikHotkeyHowto/blob/master/config/spec_main.py) for ideas):
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


def print_hello():
    print('hello')


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
    
    # Call function.
    # Hotkey: CTRL+ALT+F1
    ('^!F1', print_hello),
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
