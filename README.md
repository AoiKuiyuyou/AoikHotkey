# AoikHotkey
AutoHotkey remake in Python. Hotkey calls Python function.

![Image](/readmedata/aoikhotkey.png?raw=true)
- The [green keyboard icon](http://www.iconsdb.com/moth-green-icons/keyboard-icon.html) in the image is provided by
  [icons8](https://icons8.com/) under
  [Creative Commons Attribution-NoDerivs 3.0 Unported](http://creativecommons.org/licenses/by-nd/3.0/).)

Tested working with:
- Python 2.7 and 3.4
- Windows 7
- Windows 8.1
  - With Python x86 version (tested with 2.7.9) some key-up events are not
   received if a hotkey function is run in the main thread.

Inspired by:
- [AutoHotkey](https://github.com/AutoHotkey/AutoHotkey)
- [pyhk](https://github.com/schurpf/pyhk)

## Table of Contents
- [Features](#features)
  - [Key-down, key-up and key-sequence hotkey](#key-down-key-up-and-key-sequence-hotkey)
  - [Hotkey function](#hotkey-function)
  - [Hotkey trigger function](#hotkey-trigger-function)
  - [Event function](#event-function)
  - [Spec reloading via hotkey](#spec-reloading-via-hotkey)
  - [Spec switching via hotkey](#spec-switching-via-hotkey)
  - [Similar hotkey definition syntax](#similar-hotkey-definition-syntax)
  - [Customizable hotkey definition parsing](#customizable-hotkey-definition-parsing)
  - [Growl Notification](#growl-notification)
    - [Setup of Growl](#setup-of-growl)
    - [Setup of GNTP Python Library](#setup-of-gntp-python-library)
- [Setup of PyWin32](#setup-of-pywin32)
- [Setup of pyHook](#setup-of-pyhook)
  - [In Python 2](#in-python-2)
  - [In Python 3](#in-python-3)
- [Setup of AoikHotkey](#setup-of-aoikhotkey)
  - [Setup via git](#setup-via-git)
  - [Setup via pip](#setup-via-pip)
- [Quick Usage](#quick-usage)
- [Program Usage](#program-usage)
  - [Show help](#show-help)
  - [Show version](#show-version)
  - [Specify spec object](#specify-spec-object)
  - [Specify spec ID](#specify-spec-id)
  - [Specify spec parse function](#specify-spec-parse-function)
  - [Specify hotkey parse function](#specify-hotkey-parse-function)
  - [Specify virtual key name-to-code function](#specify-virtual-key-name-to-code-function)
  - [Specify virtual key translate function](#specify-virtual-key-translate-function)
  - [Specify virtual key expand function](#specify-virtual-key-expand-function)
  - [Specify virtual key code-to-name function](#specify-virtual-key-code-to-name-function)
  - [Specify hotkey trigger function](#specify-hotkey-trigger-function)
  - [Specify repeat mode on/off](#specify-repeat-mode-onoff)
  - [Specify program's debug message on/off](#specify-programs-debug-message-onoff)
- [Internals](#internals)
  - [Parsing Mechanism](#parsing-mechanism)
    - [Spec parse function](#spec-parse-function)
    - [Hotkey parse function](#hotkey-parse-function)
    - [Virtual key name-to-code function](#virtual-key-name-to-code-function)
    - [Virtual key translate function](#virtual-key-translate-function)
    - [Virtual key expand function](#virtual-key-expand-function)
  - [Hotkey type](#hotkey-type)
    - [Key down](#key-down)
    - [Key up](#key-up)
    - [Key sequence](#key-sequence)
  - [Hotkey function](#hotkey-function-1)
  - [Built-in hotkey functions](#built-in-hotkey-functions)
    - [Quit](#quit)
    - [SpecReload](#specreload)
    - [SpecSwitch](#specswitch)
    - [EventProp](#eventprop)
    - [EventStop](#eventstop)
    - [Cmd](#cmd)
    - [Cmd2](#cmd2)
    - [Send](#send)
    - [Send2](#send2)
    - [SendSubs](#sendsubs)
    - [Sleep](#sleep)
  - [Event function](#event-function-1)
  - [Built-in event functions](#built-in-event-functions)
    - [efunc](#efunc)
    - [efunc_no_mouse](#efunc_no_mouse)
    - [efunc_no_mouse_move](#efunc_no_mouse_move)
- [Gotchas](#gotchas)
  - [Quit the program](#quit-the-program)
  - [Freeze Windows](#freeze-windows)

## Features
- [Key-down, key-up and key-sequence hotkey](#key-down-key-up-and-key-sequence-hotkey)
- [Hotkey function](#hotkey-function)
- [Hotkey trigger function](#hotkey-trigger-function)
- [Event function](#event-function)
- [Spec reloading via hotkey](#spec-reloading-via-hotkey)
- [Spec switching via hotkey](#spec-switching-via-hotkey)
- [Similar hotkey definition syntax](#similar-hotkey-definition-syntax)
- [Customizable hotkey definition parsing](#customizable-hotkey-definition-parsing)
- [Growl Notification](#growl-notification)
  - [Setup of Growl](#setup-of-growl)
  - [Setup of GNTP Python Library](#setup-of-gntp-python-library)

### Key-down, key-up and key-sequence hotkey
Like AutoHotkey, hotkey can be triggered by key-down, key-up, and key-sequence
 events.

See the details of [hotkey types](#hotkey-type).

### Hotkey function
A triggered hotkey calls a Python function.

This means the whole Python language is available at hand, which is more
 powerful than AutoHotkey's built-in language.

See an [example](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L37).

See the details of [hotkey function](#hotkey-function-1).

### Hotkey trigger function
A **hotkey trigger function** is always called right before the hotkey function
registered for a hotkey is called.

Hotkey trigger function can be used to implement general things that apply to
every triggered hotkey.

The default hotkey trigger function is
[aoikhotkey.spec.tfunc::hotkey_tfunc](/src/aoikhotkey/spec/tfunc.py#L12). It
prints information about the triggered hotkey to command console.

Use [argument -T](#specify-hotkey-trigger-function) to
specify a hotkey trigger function.

### Event function
Besides hotkey function that is registered for specific hotkey, event function
 can be registered to handle all key events.

See an [example](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L39).

See the details of [event function](#event-function-1).

### Spec reloading via hotkey
A group of hotkey definitions is called a **spec**.

[Reloading a spec](#specreload) can be done via hotkey, without
 restarting the program. This is very handy.

See how I use [one hotkey](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L143) to open the editor to
 edit the spec file, and then use [another hotkey](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L232)
 to reload the spec.

### Spec switching via hotkey
A group of hotkey definitions is called a **spec**.

AoikHotkey supports specifying multiple specs.

[Switching between specs](#specreload) can be done via hotkey. This
 is very handy and it greatly increaes the utility of hotkeys because same
 hotkey can do different things in different specs.

### Similar hotkey definition syntax
The syntax for hotkey definition is very similar to that of AutoHotkey.

See an [example](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L37).

See the details of [hotkey parse function](#hotkey-parse-function) that
 defines the hotkey definition syntax.

### Customizable hotkey definition parsing
A mechanism is provided to customize how hotkey spec and hotkey definition are
 parsed.

Can be used to do simple things like defining custom name for virtual keys,
 e.g. `ctrla` for `VK_Control` and `VK_KEY_A`.

Can also be used to do complicated things like reinventing the whole hotkey
 definition syntax.

See the details of [parsing mechanism](#parsing-mechanism).

### Growl Notification
![Image](/readmedata/growl.png?raw=true)
- The [green keyboard icon](http://www.iconsdb.com/moth-green-icons/keyboard-icon.html) in the image is provided by
  [icons8](https://icons8.com/) under
  [Creative Commons Attribution-NoDerivs 3.0 Unported](http://creativecommons.org/licenses/by-nd/3.0/).)

Support for **Growl** notification is implemented as a
[hotkey trigger function](#hotkey-trigger-function).

The hotkey trigger function is
 [aoikhotkey.ext.growl::hotkey_tfunc](/src/aoikhotkey/ext/growl.py#L25).

Use [argument -T](#specify-hotkey-trigger-function) to
 specify using it:
```
-T aoikhotkey.ext.growl::hotkey_tfunc
```

This hotkey trigger function requires
[GNTP Python Library](#setup-of-gntp-python-library) to send notifications, and
[Growl](#setup-of-growl) to receive and display the notifications.

#### Setup of Growl
In Windows, use the installer from
 [www.growlforwindows.com](http://www.growlforwindows.com/gfw/).

#### Setup of GNTP Python Library
Run:
```
pip install git+https://github.com/kfdm/gntp
```

## Setup of PyWin32
Use an installer from [here](http://sourceforge.net/projects/pywin32/files/pywin32/).
- Choose the latest build version  (e.g. Build 219 on 2014-05-04).
- Make sure the installer matches with your Python version, e.g. **amd64-py2.7**
   if you are using a **Python 2.7 x64** version.

## Setup of pyHook
- [In Python 2](#in-python-2)
- [In Python 3](#in-python-3)

### In Python 2
If your Python 2 is x86 version, use the installer
 [pyHook-1.5.1.win32-py2.7.exe](http://sourceforge.net/projects/pyhook/files/pyhook/1.5.1/pyHook-1.5.1.win32-py2.7.exe/download).

If your Python 2 is x64 version, download the source code
 [pyHook-1.5.1.zip](http://sourceforge.net/projects/pyhook/files/pyhook/1.5.1/pyHook-1.5.1.zip/download).

Unzip and run
```
python setup.py install
```
- Toolset for compiling C extension is required.

### In Python 3
pyHook's official version does not support Python 3.

Instead, use the fork [pyhook_py3k](https://github.com/Answeror/pyhook_py3k).

Download the latest source code and unzip.

There is one change to make. In file
 [HookManager.py](https://github.com/Answeror/pyhook_py3k/blob/3a0a1fe8fb190e10761dd80f55a4cf8efd0fb3e3/HookManager.py#L1), change the first line's
 `import cpyHook` into `import pyHook.cpyHook as cpyHook`. Otherwise it will
 cause ImportError in Python 3.

After making the change, run
```
python setup.py install
```
- Toolset for compiling C extension is required.

## Setup of AoikHotkey
- [Setup via git](#setup-via-git)
- [Setup via pip](#setup-via-pip)

### Setup via git
Clone this git repository to local:
```
git clone https://github.com/AoiKuiyuyou/AoikHotkey
```

In the local repository directory, the entry program can be run directly without
further installation:
```
python src/aoikhotkey/main/aoikhotkey.py
```
- No requirements on working directory, the entry program can be run anywhere as
   long as the path is correct.
- No need to configure **PYTHONPATH** because the entry program supports
  [package bootstrap](https://github.com/AoiKuiyuyou/AoikProjectStart-Python#package-bootstrap).

If you prefer an installation, run the **setup.py** file in the local repository
directory:
```
python setup.py install
```

The installation will install program files into Python's "package directory".
As a result, the entry program is also accessible via module name:
```
python -m aoikhotkey.main
```

And the installation will create an executable file in Python's
"script directory". If Python's "script directory" has been added to your
command console's **PATH** environment variable, the entry program should be
accessible in short name:
```
aoikhotkey
```

### Setup via pip
Run:
```
pip install git+https://github.com/AoiKuiyuyou/AoikHotkey
```

Installing via pip is equivalent to cloning this git repository to local and
running the **setup.py** file in the local repository directory.

## Quick Usage
The only argument required by command **aoikhotkey** is a spec object's URI. A
 spec object is a Python list object that contains
 [hotkey definitions](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L37). The
 spec object to use is specified by a URI, using [argument -s](#specify-spec-object).

E.g.
```
aoikhotkey -s aoikhotkey.main.spec::SPEC

aoikhotkey -s src/aoikhotkey/main/spec.py::SPEC
```
- [SPEC](/src/aoikhotkey/main/spec.py#L14)

The **SPEC** object above is just a simple example. See
 [AoikHotkeyDemo](https://github.com/AoiKuiyuyou/AoikHotkeyDemo) for more demo
 specs.

## Program Usage
- [Show help](#show-help)
- [Show version](#show-version)
- [Specify spec object](#specify-spec-object)
- [Specify spec ID](#specify-spec-id)
- [Specify spec parse function](#specify-spec-parse-function)
- [Specify hotkey parse function](#specify-hotkey-parse-function)
- [Specify virtual key name-to-code function](#specify-virtual-key-name-to-code-function)
- [Specify virtual key translate function](#specify-virtual-key-translate-function)
- [Specify virtual key expand function](#specify-virtual-key-expand-function)
- [Specify virtual key code-to-name function](#specify-virtual-key-code-to-name-function)
- [Specify hotkey trigger function](#specify-hotkey-trigger-function)
- [Specify repeat mode on/off](#specify-repeat-mode-onoff)
- [Specify program's debug message on/off](#specify-programs-debug-message-onoff)

Examples below assume you have command **aoikhotkey** available from
 command line, which is equivalent to running the entry program directly using
 `python src/aoikhotkey/main/aoikhotkey.py` from the local repo dir.

Some of the command examples below use relative paths:
- `src/aoikhotkey` assumes your working dir is the local repo dir.

### Show help
Use argument **-h**
```
aoikhotkey -h
```

### Show version
Use argument **--ver**
```
aoikhotkey --ver
```

### Specify spec object
This argument can be used multiple times because AoikHotkey supports multiple
 specs. You can use hotkey to [switch between specs](#specswitch).
 
Use argument **-s**
```
aoikhotkey -s _OBJ_URI_
```
- Replace `_OBJ_URI_` with proper value of yours.
- `_OBJ_URI_` can be any object URI formats supported by
   [AoikImportUtil](https://github.com/AoiKuiyuyou/AoikImportUtil-Python#load-object).

E.g.
```
aoikhotkey -s aoikhotkey.main.spec::SPEC

aoikhotkey -s src/aoikhotkey/main/spec.py::SPEC
```
- [SPEC](/src/aoikhotkey/main/spec.py#L14)
- Use `LCtrl q` to quit the program.

The **SPEC** object above is just a simple example. See
 [AoikHotkeyDemo](https://github.com/AoiKuiyuyou/AoikHotkeyDemo) for more demo
 specs.

A spec object's format is dependent on the
 [spec parse function](#spec-parse-function) and
 [hotkey parse function](#hotkey-parse-function) in use.

### Specify spec ID
A spec can be given a spec ID.

Spec ID is used by built-in hotkey function
 [SpecSwitch](#specswitch) to identify the spec to swicth to.

This argument can be used multiple times, each time matching with one spec
 specified by [argument -s](#specify-spec-object), in
 order.

Use argument **-i**
```
aoikhotkey -i _SPEC_ID_
```
- Replace `_SPEC_ID_` with proper value of yours.

E.g.
```
aoikhotkey -s aoikhotkey.main.spec::SPEC -i main_spec
```
- [SPEC](/src/aoikhotkey/main/spec.py#L14)
- Use `LCtrl q` to quit the program.

### Specify spec parse function
Spec parse function is discussed [here](#spec-parse-function).

Use argument **-S**
```
aoikhotkey -S _OBJ_URI_
```
- Replace `_OBJ_URI_` with proper value of yours.
- `_OBJ_URI_` can be any object URI formats supported by
   [AoikImportUtil](https://github.com/AoiKuiyuyou/AoikImportUtil-Python#load-object).

E.g.
```
aoikhotkey -s aoikhotkey.main.spec::SPEC -S aoikhotkey.spec.parser::spec_parse

aoikhotkey -s src/aoikhotkey/main/spec.py::SPEC -S src/aoikhotkey/spec/parser.py::spec_parse
```
- [SPEC](/src/aoikhotkey/main/spec.py#L14)
- [spec_parse](/src/aoikhotkey/spec/parser.py#L42)
- Use `LCtrl q` to quit the program.

The default is
 [aoikhotkey.spec.parser::spec_parse](/src/aoikhotkey/spec/parser.py#L42).

### Specify hotkey parse function
Hotkey parse function is discussed [here](#hotkey-parse-function).

Use argument **-p**
```
aoikhotkey -p _OBJ_URI_
```
- Replace `_OBJ_URI_` with proper value of yours.
- `_OBJ_URI_` can be any object URI formats supported by
   [AoikImportUtil](https://github.com/AoiKuiyuyou/AoikImportUtil-Python#load-object).

E.g.
```
aoikhotkey -s aoikhotkey.main.spec::SPEC -p aoikhotkey.spec.parser::hotkey_parse

aoikhotkey -s src/aoikhotkey/main/spec.py::SPEC -p src/aoikhotkey/spec/parser.py::hotkey_parse
```
- [SPEC](/src/aoikhotkey/main/spec.py#L14)
- [hotkey_parse](/src/aoikhotkey/spec/parser.py#L236)
- Use `LCtrl q` to quit the program.

The default is
 [aoikhotkey.spec.parser::hotkey_parse](/src/aoikhotkey/spec/parser.py#L236).

### Specify virtual key name-to-code function
Virtual key name-to-code function is discussed [here](#virtual-key-name-to-code-function).

Use argument **-n**
```
aoikhotkey -n _OBJ_URI_
```
- Replace `_OBJ_URI_` with proper value of yours.
- `_OBJ_URI_` can be any object URI formats supported by
   [AoikImportUtil](https://github.com/AoiKuiyuyou/AoikImportUtil-Python#load-object).

E.g.
```
aoikhotkey -s aoikhotkey.main.spec::SPEC -n aoikhotkey.virkey::vk_ntc

aoikhotkey -s src/aoikhotkey/main/spec.py::SPEC -n src/aoikhotkey/virkey.py::vk_ntc
```
- [SPEC](/src/aoikhotkey/main/spec.py#L14)
- [vk_ntc](/src/aoikhotkey/virkey.py#L159)
- Use `LCtrl q` to quit the program.

The default is
 [aoikhotkey.virkey::vk_ntc](/src/aoikhotkey/virkey.py#L159).

### Specify virtual key translate function
Virtual key translate function is discussed [here](#virtual-key-translate-function).

Use argument **-t**
```
aoikhotkey -t _OBJ_URI_
```
- Replace `_OBJ_URI_` with proper value of yours.
- `_OBJ_URI_` can be any object URI formats supported by
   [AoikImportUtil](https://github.com/AoiKuiyuyou/AoikImportUtil-Python#load-object).

E.g.
```
aoikhotkey -s aoikhotkey.main.spec::SPEC -t aoikhotkey.virkey::vk_tran

aoikhotkey -s src/aoikhotkey/main/spec.py::SPEC -t src/aoikhotkey/virkey.py::vk_tran
```
- [SPEC](/src/aoikhotkey/main/spec.py#L14)
- [vk_tran](/src/aoikhotkey/virkey.py#L235)
- Use `LCtrl q` to quit the program.

The default is
 [aoikhotkey.virkey::vk_tran](/src/aoikhotkey/virkey.py#L235).

### Specify virtual key expand function
Virtual key expand function is discussed [here](#virtual-key-expand-function).

Use argument **-e**
```
aoikhotkey -e _OBJ_URI_
```
- Replace `_OBJ_URI_` with proper value of yours.
- `_OBJ_URI_` can be any object URI formats supported by
   [AoikImportUtil](https://github.com/AoiKuiyuyou/AoikImportUtil-Python#load-object).

E.g.
```
aoikhotkey -s aoikhotkey.main.spec::SPEC -e aoikhotkey.virkey::vk_expand

aoikhotkey -s src/aoikhotkey/main/spec.py::SPEC -e src/aoikhotkey/virkey.py::vk_expand
```
- [SPEC](/src/aoikhotkey/main/spec.py#L14)
- [vk_expand](/src/aoikhotkey/virkey.py#L222)
- Use `LCtrl q` to quit the program.

The default is
 [aoikhotkey.virkey::vk_expand](/src/aoikhotkey/virkey.py#L222).

### Specify virtual key code-to-name function
Virtual key code-to-name function is used by hotkey manager to print message
 when a key event is received. E.g. convert virtual key code 162 to key name
 VK_LCONTROL.

Use argument **-c**
```
aoikhotkey -c _OBJ_URI_
```
- Replace `_OBJ_URI_` with proper value of yours.
- `_OBJ_URI_` can be any object URI formats supported by
   [AoikImportUtil](https://github.com/AoiKuiyuyou/AoikImportUtil-Python#load-object).

E.g.
```
aoikhotkey -s aoikhotkey.main.spec::SPEC -c aoikhotkey.virkey::vk_ctn

aoikhotkey -s src/aoikhotkey/main/spec.py::SPEC -c src/aoikhotkey/virkey.py::vk_ctn
```
- [SPEC](/src/aoikhotkey/main/spec.py#L14)
- [vk_ctn](/src/aoikhotkey/virkey.py#L197)
- Use `LCtrl q` to quit the program.

The default is
 [aoikhotkey.virkey::vk_ctn](/src/aoikhotkey/virkey.py#L197).

### Specify hotkey trigger function

Use argument **-P**
```
aoikhotkey -P _OBJ_URI_
```
- Replace `_OBJ_URI_` with proper value of yours.
- `_OBJ_URI_` can be any object URI formats supported by
   [AoikImportUtil](https://github.com/AoiKuiyuyou/AoikImportUtil-Python#load-object).

E.g.
```
aoikhotkey -s aoikhotkey.main.spec::SPEC -T aoikhotkey.spec.tfunc::hotkey_tfunc

aoikhotkey -s src/aoikhotkey/main/spec.py::SPEC -T src/aoikhotkey/spec/tfunc.py::hotkey_tfunc
```
- [SPEC](/src/aoikhotkey/main/spec.py#L14)
- [hotkey_tfunc](/src/aoikhotkey/spec/tfunc.py#L12)
- Use `LCtrl q` to quit the program.

The default is
 [aoikhotkey.spec.tfunc::hotkey_tfunc](/src/aoikhotkey/spec/tfunc.py#L12).

### Specify repeat mode on/off
If repeat mode is set off, a repeated key-down event will be ignored. Default is
 on.

Use argument **-r**
```
#/ On
aoikhotkey -r

aoikhotkey -r1

#/ Off
aoikhotkey -r0
```

E.g.
```
aoikhotkey -s aoikhotkey.main.spec::SPEC -r

aoikhotkey -s aoikhotkey.main.spec::SPEC -r1

aoikhotkey -s aoikhotkey.main.spec::SPEC -r0
```
- [SPEC](/src/aoikhotkey/main/spec.py#L14)
- Use `LCtrl q` to quit the program.

### Specify program's debug message on/off
Use argument **-V**
```
#/ On
aoikhotkey -V

aoikhotkey -V1

#/ Off
aoikhotkey -V0
```

E.g.
```
aoikhotkey -s "nonexistent_spec" -V

aoikhotkey -s "nonexistent_spec" -V1

aoikhotkey -s "nonexistent_spec" -V0
```

## Internals
- [Parsing Mechanism](#parsing-mechanism)
- [Hotkey type](#hotkey-type)
- [Hotkey function](#hotkey-function-1)
- [Built-in hotkey functions](#built-in-hotkey-functions)
- [Event function](#event-function-1)
- [Built-in event functions](#built-in-event-functions)

### Parsing Mechanism
The parsing of hotkey spec is a division of labour by the following functions:
- [Spec parse function](#spec-parse-function)
- [Hotkey parse function](#hotkey-parse-function)
- [Virtual key name-to-code function](#virtual-key-name-to-code-function)
- [Virtual key translate function](#virtual-key-translate-function)
- [Virtual key expand function](#virtual-key-expand-function)

#### Spec parse function
First, the spec object specified via [argument -s](#specify-spec-object) is
 parsed by a **spec parse function**.

The spec object's format is not fixed but should be compatible with the spec
 parse function in use.

Here is an [example](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L37) of the spec format supported by
 the [default spec parse function](/src/aoikhotkey/spec/parser.py#L42).

The default spec parse function takes a list of
 (hotkey definition, hotkey function ...) tuples where "hotkey function ..."
 means one or more hotkey functions.

The return value's format of a spec parse function is fixed. It should be a list
 of (hotkey definition, hotkey type, hotkey function) tuples. The three values
 of each tuple will then be fed into hotkey manager's method
 [hotkey_add](/src/aoikhotkey/manager.py#L404).

From the input and output of a spec parse function, we can infer that a spec
 parse function usually does two things:
- Determines the hotkey's [event type](#hotkey-type), e.g.
   [key-down](#key-down),
   [key-up](#key-up),
   or [key-sequence](#key-sequence).
- Normalizes the list of hotkey functions into one single hotkey function.

The default spec parse function does exactly the two things. Meanwhile, it
 recognizes some special syntax in the hotkey definition:
- A beginning `~` means the hotkey is triggered by
   [key-up](#key-up) event instead of
   [key-down](#key-down). E.g. spec item `('~a', f)`
   means to call hotkey function `f` when key-up event of key `a` is received.
- A beginning `::` means the hotkey is triggered by
   [key-sequence](#key-sequence) event. E.g. spec item
   `('::abc', f)` means to call hotkey function `f` when keys `abc` are typed
   in sequence.  
  Trailing `::` can be added to resemble AutoHotkey's syntax, e.g.
   `('::abc::', f)`.
- A beginning `@` means to call the hotkey function in another thread. E.g. spec
   item `('@a', f)` means to call hotkey function `f` in another thread. This is
   the default behaviour so `@` needs not be specified explicitly.
- A beginning `$` means to call the hotkey function in the same thread. E.g.
   spec item `('$a', f)` means to call hotkey function `f` in the same thread.
- `@` or `$` can be combined with either `~` or `::`. `~` and `::` can not be
   combined with each other, for the obvious reason.

The special syntax recognized by a spec parse function should be removed from
 the hotkey definition after the call. What's left in the resulting hotkey
 definition should be compatible with the
 [hotkey parse function](#hotkey-parse-function) in use.

#### Hotkey parse function
As mentioned in section [Spec parse function](#spec-parse-function), hotkey definition, hotkey type,
 and hotkey function in each of the tuples returned from the spec parse function
 in use is then fed into hotkey manager's method
 [hotkey_add](/src/aoikhotkey/manager.py#L404). Inside this method, the hotkey
 definition is parsed by the hotkey parse function in use.

The hotkey parse function in use can be specified via [argument -p](#specify-hotkey-parse-function).

A hotkey parse function is required to take three arguments:
- A hotkey definition.
- A [virtual key name-to-code function](#virtual-key-name-to-code-function) (discussed in
   section below).
- A [virtual key translate function](#virtual-key-translate-function) (discussed in
   section below).

It is the hotkey parse function in use that defines the syntax of the hotkey
 definition.

The default [hotkey parse function](/src/aoikhotkey/spec/parser.py#L236) supports a
 syntax that is very similar to that of AutoHotkey:
- `^`, `!`, `+` and `#` mean Control, Alt, Shift and Win keys, respectively.
- A `<` or `>` preceding any of the four keys above converts the key into its
   sided counterpart, e.g. `<^` means LControl, `>^` means RControl.
- `F1` to `F12` mean the 12 function keys.
- Anything inside a `{}` is a name to be resolved by the
   [virtual key name-to-code function](#virtual-key-name-to-code-function) in use.
- Characters that have special meaning in the syntax can be put inside `{}`
   to get their literal values. E.g. `{^}`, `{!}`, `{+}`, `{#}`, `{<}`, `{>}`,
   `{F}`, `{{}` and `{}}`. Inside `{}`, they are just single-character name to
   be resolved by the virtual key name-to-code function in use.
- Characters not inside `{}` are resolved one by one, as if each character
   is inside a `{}`. E.g. `abc` is equivalent to `{a}{b}{c}`.  
   Note this is different with AutoHotkey, in which special names like `PageUp`
    are not put inside `{}`. In AoikHotkey, special names must be put inside
    `{}`, with the only exception of `F1` to `F12`.

#### Virtual key name-to-code function
As mentioned in section [Hotkey parse function](#hotkey-parse-function), a hotkey parse function takes a
 virtual key name-to-code (VK_NTC for short) function as its second argument. It
 uses the VK_NTC function to resolve a name to one or a list of virtual key
 codes.

A VK_NTC function is required to take one argument: the virtual key name.

A VK_NTC function is required to return one or a list of virtual key codes.

The VK_NTC function in use can be specified via
 [argument -n](#specify-virtual-key-name-to-code-function).

The default is [aoikhotkey.virkey::vk_ntc](/src/aoikhotkey/virkey.py#L159).

The default VK_NTC function supports a reasonable set of names:
- Lowercase printable character: e.g. `{a}` is resolved to VK_KEY_A.  
  See the [full list](/src/aoikhotkey/dep/aoikvirkey.py#L209).
- Uppercase printable character: e.g. `{A}` is resolved to VK_SHIFT and
   VK_KEY_A.  
  Note this is different with AutoHotkey, in which `A` is treated just like
   `a`, without adding a Shift.  
  See the [full list](/src/aoikhotkey/dep/aoikvirkey.py#L271).
- Virtual key name: e.g. `{VK_HOME}` is resolved to VK_HOME.  
  See the [full list](/src/aoikhotkey/dep/aoikvirkey.py#L6).
- Virtual key name without `VK_` prefix: e.g. `{HOME}` is resolved to VK_HOME.  
  See the [full list](/src/aoikhotkey/dep/aoikvirkey.py#L6).
- Common name: e.g. `{ESC}` is resolved to VK_ESCAPE.  
  See the [full list](/src/aoikhotkey/virkey.py#L114).

#### Virtual key translate function
As mentioned in section [Hotkey parse function](#hotkey-parse-function), a hotkey parse function takes a
 virtual key translate (VK_TRAN for short) function as its third argument. It
 uses the VK_TRAN function to translate a neutral key with a preceding `<`
 or `>` into its sided counterpart. E.g. `<^` and `>^` will be translated into
 VK_LCONTROL and VK_RCONTROL, respectively.

A VK_TRAN function is required to take two arguments:
- A virtual key code.
- A "side" value indicating how the virtual key is sided.

A VK_TRAN function is required to return one or a list of virtual key codes.

The VK_TRAN function in use can be specified via
 [argument -t](#specify-virtual-key-translate-function).

The default is [aoikhotkey.virkey::vk_tran](/src/aoikhotkey/virkey.py#L235).

The default VK_TRAN function does the following translation:
- VK_CONTROL: to VK_LCONTROL or VK_RCONTROL
- VK_MENU: to VK_LMENU or VK_RMENU
- VK_SHIFT: to VK_LSHIFT or VK_RSHIFT
- EVK_WIN: to VK_LWIN or VK_RWIN
- VK_MOUSE_WHEEL: EVK_MOUSE_WHEEL_UP or EVK_MOUSE_WHEEL_DOWN

#### Virtual key expand function
After a hotkey definition is parsed by the hotkey parse function into a list of
 virtual keys, a virtual key expand function (VK_EXPAND for short) is used
 to expand neutral virtual keys in the list into their sided counterparts. For
 example, `^a` is parsed into `[VK_CONTROL, VK_KEY_A]`, then expanded into
 `[VK_LCONTROL, VK_KEY_A]` and `[VK_RCONTROL, VK_KEY_A]`.

This is because in the hotkey definition `^` has no preceding `<` or `>`, so
 the neutral form survives the parsing. However, a normal keyboard never
 generates a neutral VK_CONTROL. It generates either VK_LCONTROL or VK_RCONTROL.
 Therefore it is not wise to wait on VK_CONTROL events. The right choice is to
 wait on both VK_LCONTROL and VK_RCONTROL events instead. The VK_EXPAND function
 is just for this purpose.

A VK_EXPAND function is required to take one argument: the virtual key.

A VK_EXPAND function is required to return a list of sided keys of the virtual
 key, or None if the virtual key has no sided keys.

The VK_EXPAND function in use can be specified via
 [argument -e](#specify-virtual-key-expand-function).

The default is [aoikhotkey.virkey::vk_expand](/src/aoikhotkey/virkey.py#L222).

The default VK_EXPAND function does the following expansion:
- VK_CONTROL: to (VK_LCONTROL, VK_RCONTROL)
- VK_MENU: to (VK_LMENU, VK_RMENU)
- VK_SHIFT: to (VK_LSHIFT, VK_RSHIFT)
- EVK_WIN: to (VK_LWIN, VK_RWIN)
- VK_MOUSE_WHEEL: to (EVK_MOUSE_WHEEL_UP, EVK_MOUSE_WHEEL_DOWN)

### Hotkey type
A hotkey can be triggered by either of the three event types:
- [Key down](#key-down)
- [Key up](#key-up)
- [Key sequence](#key-sequence)

#### Key down
Key-down hotkey is the default hotkey type.

#### Key up
Key-up hotkey can be specified by adding a beginning `~` to a hotkey definition.
This syntax is supported by the [default spec parser](#spec-parse-function).

#### Key sequence
Key-sequence hotkey can be specified by adding a beginning `::` to a hotkey
 definition. This syntax is supported by the
 [default spec parser](#spec-parse-function).

Unlike AutoHotkey's key-sequence hotkey that always does text substitution,
 AoikHotkey's key-sequence hotkey calls a function. To resemble AutoHotkey's
 text substitution, simply use the built-in function
 [SendSubs](#sendsubs).

Unlike AutoHotkey's key-sequence hotkey that is triggered by an extra space
 after the target key sequence, AoikHotkey's key-sequence hotkey is triggered
 as soon as the target key sequence is typed. To resemble AutoHotkey's extra
 space behaviour, simply add a space to the end of a hotkey definition.

### Hotkey function
A hotkey function can either take no argument, or take one argument: the event
 object.

A hotkey function's return value matters.
- If the last hotkey function returns non-True, the key event is not propagated
   to the foreground window. This is the recommended default behaviour.
- If the last hotkey function returns True, the key event is propagated
   to the foreground window.
- If any hotkey function returns False, follwing hotkey functions (if any) will
   not be called. And the key event is not propagated to the foreground window.

### Built-in hotkey functions
- [Quit](#quit)
- [SpecReload](#specreload)
- [SpecSwitch](#specswitch)
- [EventProp](#eventprop)
- [EventStop](#eventstop)
- [Cmd](#cmd)
- [Cmd2](#cmd2)
- [Send](#send)
- [Send2](#send2)
- [SendSubs](#sendsubs)
- [Sleep](#sleep)

#### Quit
Quit the program.

See the [code](/src/aoikhotkey/spec/util.py#L42) and [example](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L230).

#### SpecReload
Reload the current spec.

See the [code](/src/aoikhotkey/spec/util.py#L47) and [example](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L232).

#### SpecSwitch
Switch to a spec.

See the [code](/src/aoikhotkey/spec/util.py#L91) and [example](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L273).

#### EventProp
Return True so that a key event is propagated to next handler.

See the [code](/src/aoikhotkey/spec/util.py#L95).

#### EventStop
Return False so that a key event is not propagated to next handler.

See the [code](/src/aoikhotkey/spec/util.py#L102).

#### Cmd
Run a command.

It takes a single command string and splits it into components (program and
 arguments).

The default separator is space.

If a command can not be well split on space, e.g. it has space inside some
 argument, you can either specify another separator, or use
 [Cmd2](#cmd2) instead.

See the [code](/src/aoikhotkey/spec/util.py#L139) and [example](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L106).

#### Cmd2
Run a command.

It takes a variable-list (e.g. *args, not a list object) of command components.
 The first is the program and the rest is the arguments.

Command components can have spaces inside them.

See the [code](/src/aoikhotkey/spec/util.py#L152) and [example](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L74).

#### Send
Send keys. Similar to AutoHotkey's **Send** function.

See the [code](/src/aoikhotkey/spec/util.py#L178) and [example](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L87).

#### Send2
[Send](#send) with the **imod_dn** option set on.

Before sending keys, **Send** will first release the triggered hotkey's modifier
 keys. Otherwise the modifier keys will interfere with the keys to be sent.

After sending the keys, if the **imod_dn** option is set on, **Send** will
 re-press the triggered hotkey's modifier keys. This makes the hotkey
 repeatable. Without the re-pressing the hotkey is not repeatable because the
 hotkey's modifier keys have been released already (even though you are still
 physically pressing on them).

See the [code](/src/aoikhotkey/spec/util.py#L228) and [example](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L260).

#### SendSubs

Send substitution text. Used together with a
 [key-sequence](#key-sequence) hotkey to implement the effect
 of text substitution. Similar to what key-sequence hotkey (e.g. `::abc::`) does
 in AutoHotkey.

See the [code](/src/aoikhotkey/spec/util.py#L233) and [example](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L91).

#### Sleep
Sleep for a while. Similar to AutoHotkey's **Sleep** function.

Note sleep will block the current thread. If the sleep time is long, you might
 want to run the hotkey function in [another thread](#spec-parse-function).

See the [code](/src/aoikhotkey/spec/util.py#L267) and [example](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L117).

### Event function
If a hotkey definition is None, the hotkey function becomes an event function.

Unlike a hotkey function gets called on a specific key event, an event function
 gets called on every key event.

An event function is required to take one argument: the event object.

An event function's return value matters the same way as a
 [hotkey function](#hotkey-function-1) does.

### Built-in event functions
- [efunc](#efunc)
- [efunc_no_mouse](#efunc_no_mouse)
- [efunc_no_mouse_move](#efunc_no_mouse_move)

#### efunc
Print message about every key event, including the overwhelming mouse move
 events.

See the [code](/src/aoikhotkey/spec/efunc.py#L12).

#### efunc_no_mouse
Print message about every key event except mouse events.

See the [code](/src/aoikhotkey/spec/efunc.py#L64) and [example](https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1.1/src/aoikhotkeydemo/common/spec.py#L39).

#### efunc_no_mouse_move
Print message about every key event except mouse move events.

See the [code](/src/aoikhotkey/spec/efunc.py#L74).

## Gotchas

### Quit the program
Pressing `Ctrl Shift c` to quit the program does not work because the interrupt
 does not play well with pyHook. The right way to quit the program is choose
 a hotkey and let it call the built-in hotkey function
 [Quit](#quit). Here is an
 [example](/src/aoikhotkey/main/spec.py#L18).

### Freeze Windows
Unlike AutoHotkey, AoikHotkey is a console program.

If you run it in a Windows CMD console as I do, and the CMD console's
 **QuickEdit** mode is on, make sure you do not click inside the CMD console.

This is because when clicking inside a CMD console with **QuickEdit** mode on,
 the AoikHotkey program running in it gets paused. The pause does not play well
 with pyHook and Windows. As a result, Windows (the whole GUI environment)
 becomes almost irresponsive.

In case this unfortunate situation does happen to you, try press ESC or clicking
 your mouse outside the CMD console (you can not see it because the Windows GUI
 is irresponsive) to get your cursor out of the CMD console. If these do not
 work, press "Ctrl Alt Del" and select "Log off" would save you a reboot.
