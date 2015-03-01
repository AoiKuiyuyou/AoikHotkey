[:var_set('', """
#/ Compile command
aoikdyndocdsl -s README.src.md -n aoikdyndocdsl.ext.all::nto -g README.md
""")
]\
[:var_set('common_spec_link', 'https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1/src/aoikhotkeydemo/common/spec.py#L37')]\
[:var_set('common_spec_efunc_link', 'https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1/src/aoikhotkeydemo/common/spec.py#L39')]\
[:var_set('common_spec_link2', 'https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1/src/aoikhotkeydemo/common/spec.py#L143')]\
[:var_set('common_spec_link3', 'https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1/src/aoikhotkeydemo/common/spec.py#L232')]\
[:var_set('hotkey_add_link', '/src/aoikhotkey/manager.py#L400')]\
[:var_set('hotkey_parse_link', '/src/aoikhotkey/spec/parser.py#L214')]\
[:var_set('main_spec_link', '/src/aoikhotkey/main/spec.py#L14')]\
[:var_set('hook_manager_link', 'https://github.com/Answeror/pyhook_py3k/blob/3a0a1fe8fb190e10761dd80f55a4cf8efd0fb3e3/HookManager.py#L1')]\
[:var_set('spec_arg_flag', '-s')]\
[:var_set('spf_arg_flag', '-p')]\
[:var_set('spf_link', '/src/aoikhotkey/spec/parser.py#L33')]\
[:var_set('vk_ntc_arg_flag', '-n')]\
[:var_set('vk_ntc_link', '/src/aoikhotkey/virkey.py#L159')]\
[:var_set('vk_tran_arg_flag', '-t')]\
[:var_set('vk_tran_link', '/src/aoikhotkey/virkey.py#L235')]\
[:var_set('vk_expand_arg_flag', '-e')]\
[:var_set('vk_expand_link', '/src/aoikhotkey/virkey.py#L222')]\
[:var_set('vk_ctn_link', '/src/aoikhotkey/virkey.py#L197')]\
[:var_set('vk_ntc_full_list_lc', '/src/aoikhotkey/dep/aoikvirkey.py#L209')]\
[:var_set('vk_ntc_full_list_uc', '/src/aoikhotkey/dep/aoikvirkey.py#L271')]\
[:var_set('vk_ntc_full_list_vk_name', '/src/aoikhotkey/dep/aoikvirkey.py#L6')]\
[:var_set('vk_ntc_full_list_vk_sname', '/src/aoikhotkey/virkey.py#L114')]\
[:var_set('quit_link', '/src/aoikhotkey/spec/util.py#L26')]\
[:var_set('quit_eg', 'https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1/src/aoikhotkeydemo/common/spec.py#L230')]\
[:var_set('specreload_link', '/src/aoikhotkey/spec/util.py#L30')]\
[:var_set('specreload_eg', 'https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1/src/aoikhotkeydemo/common/spec.py#L232')]\
[:var_set('specswitch_link', '/src/aoikhotkey/spec/util.py#L72')]\
[:var_set('specswitch_eg', 'https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1/src/aoikhotkeydemo/common/spec.py#L273')]\
[:var_set('eventprop_link', '/src/aoikhotkey/spec/util.py#L76')]\
[:var_set('eventstop_link', '/src/aoikhotkey/spec/util.py#L83')]\
[:var_set('cmd_link', '/src/aoikhotkey/spec/util.py#L120')]\
[:var_set('cmd_eg', 'https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1/src/aoikhotkeydemo/common/spec.py#L106')]\
[:var_set('cmd2_link', '/src/aoikhotkey/spec/util.py#L133')]\
[:var_set('cmd2_eg', 'https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1/src/aoikhotkeydemo/common/spec.py#L74')]\
[:var_set('send_link', '/src/aoikhotkey/spec/util.py#L159')]\
[:var_set('send_eg', 'https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1/src/aoikhotkeydemo/common/spec.py#L87')]\
[:var_set('send2_link', '/src/aoikhotkey/spec/util.py#L209')]\
[:var_set('send2_eg', 'https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1/src/aoikhotkeydemo/common/spec.py#L260')]\
[:var_set('sendsubs_link', '/src/aoikhotkey/spec/util.py#L214')]\
[:var_set('sendsubs_eg', 'https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1/src/aoikhotkeydemo/common/spec.py#L91')]\
[:var_set('sleep_link', '/src/aoikhotkey/spec/util.py#L248')]\
[:var_set('sleep_eg', 'https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1/src/aoikhotkeydemo/common/spec.py#L117')]\
[:var_set('efunc_link', '/src/aoikhotkey/spec/efunc.py#L12')]\
[:var_set('efunc_no_mouse_link', '/src/aoikhotkey/spec/efunc.py#L64')]\
[:var_set('efunc_no_mouse_eg', 'https://github.com/AoiKuiyuyou/AoikHotkeyDemo/blob/0.1/src/aoikhotkeydemo/common/spec.py#L39')]\
[:var_set('efunc_no_mouse_move_link', '/src/aoikhotkey/spec/efunc.py#L74')]\
[:HDLR('heading', 'heading')]\
# AoikHotkey
AutoHotkey remake in Python. Hotkey calls Python function.

Tested working with:
- Windows 7
- Python 2.7 and 3.4. (x86 and x64 both work.)

Inspired by:
- [AutoHotkey](https://github.com/AutoHotkey/AutoHotkey)
- [pyhk](https://github.com/schurpf/pyhk)

## Table of Contents
[:toc(beg='next', indent=-1)]

## Features
[:tod()]

### Key-down, key-up and key-sequence hotkey
Like AutoHotkey, hotkey can be triggered by key-down, key-up, and key-sequence
 events.

See the details of [hotkey types]([:hd_url('hotkey_type')]).

### Hotkey function
A triggered hotkey calls a Python function.

This means the whole Python language is available at hand, which is more
 powerful than AutoHotkey's built-in language.

See an [example]([:var('common_spec_link')]).

See the details of [hotkey function]([:hd_url('hotkey_func')]).

### Event function
Besides hotkey function that is registered for specific hotkey, event function
 can be registered to handle all key events.

See an [example]([:var('common_spec_efunc_link')]).

See the details of [event function]([:hd_url('event_func')]).

### Spec reloading via hotkey
A group of hotkey definitions is called a **spec**.

[Reloading a spec]([:hd_url('spec_reload')]) can be done via hotkey, without
 restarting the program. This is very handy.

See how I use [one hotkey]([:var('common_spec_link2')]) to open the editor to
 edit the spec file, and then use [another hotkey]([:var('common_spec_link3')])
 to reload the spec.

### Spec switching via hotkey
A group of hotkey definitions is called a **spec**.

AoikHotkey supports specifying multiple specs.

[Switching between specs]([:hd_url('spec_reload')]) can be done via hotkey. This
 is very handy and it greatly increaes the utility of hotkeys because same
 hotkey can do different things in different specs.

### Similar hotkey definition syntax
The syntax for hotkey definition is very similar to that of AutoHotkey.

See an [example]([:var('common_spec_link')]).

See the details of [hotkey parse function]([:hd_url('hpf')]) that
 defines the hotkey definition syntax.

### Customizable hotkey definition parsing
A mechanism is provided to customize how hotkey spec and hotkey definition are
 parsed.

Can be used to do simple things like defining custom name for virtual keys,
 e.g. `ctrla` for `VK_Control` and `VK_KEY_A`.

Can also be used to do complicated things like reinventing the whole hotkey
 definition syntax.

See the details of [parsing mechanism]([:hd_url('par_mech')]).

## Setup
AoikHotkey depends on external libs [PyWin32](http://sourceforge.net/projects/pywin32/)
 and [pyHook](http://sourceforge.net/projects/pyhook/).

**pyHook** uses C extension so toolset for compiling C extension is required.

### Setup of PyWin32
Use an installer from [here](http://sourceforge.net/projects/pywin32/files/pywin32/).
- Choose the latest build version  (e.g. Build 219 on 2014-05-04).
- Make sure the installer matches with your Python version, e.g. **amd64-py2.7**
   if you are using a **Python 2.7 x64** version.

### Setup of pyHook
[:tod()]

#### In Python 2
If your Python 2 is x86 version, use the installer
 [pyHook-1.5.1.win32-py2.7.exe](http://sourceforge.net/projects/pyhook/files/pyhook/1.5.1/pyHook-1.5.1.win32-py2.7.exe/download).

If your Python 2 is x64 version, download the source code
 [pyHook-1.5.1.zip](http://sourceforge.net/projects/pyhook/files/pyhook/1.5.1/pyHook-1.5.1.zip/download).

Unzip and run
```
python setup.py install
```
- Toolset for compiling C extension is required.

#### In Python 3
pyHook's official version does not support Python 3.

Instead, use the fork [pyhook_py3k](https://github.com/Answeror/pyhook_py3k).

Download the latest source code and unzip.

There is one change to make. In file
 [HookManager.py]([:var('hook_manager_link')]), change the first line's
 `import cpyHook` into `import pyHook.cpyHook as cpyHook`. Otherwise it will
 cause ImportError in Python 3.

After making the change, run
```
python setup.py install
```
- Toolset for compiling C extension is required.

### Setup of AoikHotkey
[:tod()]

#### Setup via pip
Run
```
pip install git+https://github.com/AoiKuiyuyou/AoikHotkey
```

#### Setup via git
Clone this repo to local
```
git clone https://github.com/AoiKuiyuyou/AoikHotkey
```

Run the **setup.py** file in the local repo dir
```
python setup.py install
```
The effect is equivalent to installation via pip.

It's also ok not running **setup.py**, because the entry program can be run
directly without installation.

### Find entry program
If the installation is via pip, or you have run the **setup.py** in the local
 repo dir, then a command named **aoikhotkey** should be available from
 command line. Run
```
aoikhotkey
```

And because the package has been installed to system package dir, it's
also runnable via module name
```
python -m aoikhotkey.main
```

Anyway, if command **aoikhotkey** is not available, you can still run the
 entry program directly. Go to the local repo dir. Run
```
python src/aoikhotkey/main/aoikhotkey.py
```
- No requirement on working dir, the entry program can be run anywhere as
   long as the path is correct.
- No need to configure **PYTHONPATH** because the entry program supports
  [package bootstrap](https://github.com/AoiKuiyuyou/AoikProjectStart-Python#package-bootstrap).

## Quick Usage
The only argument required by command **aoikhotkey** is a spec object's URI. A
 spec object is a Python list object that contains
 [hotkey definitions]([:var('common_spec_link')]). The
 spec object to use is specified by a URI, using [argument [:var('spec_arg_flag')]]([:hd_url('spec_arg')]).

E.g.
```
aoikhotkey -s aoikhotkey.main.spec::SPEC

aoikhotkey -s src/aoikhotkey/main/spec.py::SPEC
```
- [SPEC]([:var('main_spec_link')])

The **SPEC** object above is just a simple example. See
 [AoikHotkeyDemo](https://github.com/AoiKuiyuyou/AoikHotkeyDemo) for more demo
 specs.

## Program Usage
[:tod()]

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
[:hd_to_key('spec_arg')]\
This argument can be used multiple times because AoikHotkey supports multiple
 specs. You can use hotkey to [switch between specs]([:hd_url('spec_switch')]).
 
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
- [SPEC]([:var('main_spec_link')])
- Use `LCtrl q` to quit the program.

The **SPEC** object above is just a simple example. See
 [AoikHotkeyDemo](https://github.com/AoiKuiyuyou/AoikHotkeyDemo) for more demo
 specs.

A spec object's format is dependent on the
 [spec parse function]([:hd_url('spf')]) and
 [hotkey parse function]([:hd_url('hpf')]) in use.

### Specify spec ID
A spec can be given a spec ID.

Spec ID is used by built-in hotkey function
 [SpecSwitch]([:hd_url('spec_switch')]) to identify the spec to swicth to.

This argument can be used multiple times, each time matching with one spec
 specified by [argument [:var('spec_arg_flag')]]([:hd_url('spec_arg')]), in
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
- [SPEC]([:var('main_spec_link')])
- Use `LCtrl q` to quit the program.

### Specify spec parse function
Spec parse function is discussed [here]([:hd_url('spf')]).

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
- [SPEC]([:var('main_spec_link')])
- [spec_parse]([:var('spf_link')])
- Use `LCtrl q` to quit the program.

The default is
 [aoikhotkey.spec.parser::spec_parse]([:var('spf_link')]).

### Specify hotkey parse function
[:hd_to_key('hpf_arg')]\
Hotkey parse function is discussed [here]([:hd_url('hpf')]).

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
- [SPEC]([:var('main_spec_link')])
- [hotkey_parse]([:var('hotkey_parse_link')])
- Use `LCtrl q` to quit the program.

The default is
 [aoikhotkey.spec.parser::hotkey_parse]([:var('hotkey_parse_link')]).

### Specify virtual key name-to-code function
[:hd_to_key('vk_ntc_arg')]\
Virtual key name-to-code function is discussed [here]([:hd_url('vk_ntc')]).

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
- [SPEC]([:var('main_spec_link')])
- [vk_ntc]([:var('vk_ntc_link')])
- Use `LCtrl q` to quit the program.

The default is
 [aoikhotkey.virkey::vk_ntc]([:var('vk_ntc_link')]).

### Specify virtual key translate function
[:hd_to_key('vk_tran_arg')]\
Virtual key translate function is discussed [here]([:hd_url('vk_tran')]).

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
- [SPEC]([:var('main_spec_link')])
- [vk_tran]([:var('vk_tran_link')])
- Use `LCtrl q` to quit the program.

The default is
 [aoikhotkey.virkey::vk_tran]([:var('vk_tran_link')]).

### Specify virtual key expand function
[:hd_to_key('vk_expand_arg')]\
Virtual key expand function is discussed [here]([:hd_url('vk_expand')]).

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
- [SPEC]([:var('main_spec_link')])
- [vk_expand]([:var('vk_expand_link')])
- Use `LCtrl q` to quit the program.

The default is
 [aoikhotkey.virkey::vk_expand]([:var('vk_expand_link')]).

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
- [SPEC]([:var('main_spec_link')])
- [vk_ctn]([:var('vk_ctn_link')])
- Use `LCtrl q` to quit the program.

The default is
 [aoikhotkey.virkey::vk_ctn]([:var('vk_ctn_link')]).

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
- [SPEC]([:var('main_spec_link')])
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
[:tod(depth=1)]

### Parsing Mechanism
[:hd_to_key('par_mech')]\
The parsing of hotkey spec is a division of labour by the following functions:
[:tod()]

#### Spec parse function
[:hd_to_key('spf')]\
First, the spec object specified via [argument [:var('spec_arg_flag')]]([:hd_url('spec_arg')]) is
 parsed by a **spec parse function**.

The spec object's format is not fixed but should be compatible with the spec
 parse function in use.

Here is an [example]([:var('common_spec_link')]) of the spec format supported by
 the [default spec parse function]([:var('spf_link')]).

The default spec parse function takes a list of
 (hotkey definition, hotkey function ...) tuples where "hotkey function ..."
 means one or more hotkey functions.

The return value's format of a spec parse function is fixed. It should be a list
 of (hotkey definition, hotkey type, hotkey function) tuples. The three values
 of each tuple will then be fed into hotkey manager's method
 [hotkey_add]([:var('hotkey_add_link')]).

From the input and output of a spec parse function, we can infer that a spec
 parse function usually does two things:
- Determines the hotkey's [event type]([:hd_url('hotkey_type')]), e.g.
   [key-down]([:hd_url('hotkey_type_key_down')]),
   [key-up]([:hd_url('hotkey_type_key_up')]),
   or [key-sequence]([:hd_url('hotkey_type_key_seq')]).
- Normalizes the list of hotkey functions into one single hotkey function.

The default spec parse function does exactly the two things. Meanwhile, it
 recognizes some special syntax in the hotkey definition:
- A beginning `~` means the hotkey is triggered by
   [key-up]([:hd_url('hotkey_type_key_up')]) event instead of
   [key-down]([:hd_url('hotkey_type_key_down')]). E.g. spec item `('~a', f)`
   means to call hotkey function `f` when key-up event of key `a` is received.
- A beginning `::` means the hotkey is triggered by
   [key-sequence]([:hd_url('hotkey_type_key_seq')]) event. E.g. spec item
   `('::abc', f)` means to call hotkey function `f` when keys `abc` are typed
   in sequence.  
  Trailing `::` can be added to resemble AutoHotkey's syntax, e.g.
   `('::abc::', f)`.
- A beginning `@` means to call the hotkey function in another thread. E.g. spec
   item `('@a', f)` means to call hotkey function `f` in another thread.
- `@` can be combined with either `~` or `::`. `~` and `::` can not be combined
   with each other, for the obvious reason.

The special syntax recognized by a spec parse function should be removed from
 the hotkey definition after the call. What's left in the resulting hotkey
 definition should be compatible with the
 [hotkey parse function]([:hd_url('hpf')]) in use.

#### Hotkey parse function
[:hd_to_key('hpf')]\
As mentioned in section [:hd_link('spf')], hotkey definition, hotkey type,
 and hotkey function in each of the tuples returned from the spec parse function
 in use is then fed into hotkey manager's method
 [hotkey_add]([:var('hotkey_add_link')]). Inside this method, the hotkey
 definition is parsed by the hotkey parse function in use.

The hotkey parse function in use can be specified via [argument -p]([:hd_url('hpf_arg')]).

A hotkey parse function is required to take three arguments:
- A hotkey definition.
- A [virtual key name-to-code function]([:hd_url('vk_ntc')]) (discussed in
   section below).
- A [virtual key translate function]([:hd_url('vk_tran')]) (discussed in
   section below).

It is the hotkey parse function in use that defines the syntax of the hotkey
 definition.

The default [hotkey parse function]([:var('hotkey_parse_link')]) supports a
 syntax that is very similar to that of AutoHotkey:
- `^`, `!`, `+` and `#` mean Control, Alt, Shift and Win keys, respectively.
- A `<` or `>` preceding any of the four keys above converts the key into its
   sided counterpart, e.g. `<^` means LControl, `>^` means RControl.
- `F1` to `F12` mean the 12 function keys.
- Anything inside a `{}` is a name to be resolved by the
   [virtual key name-to-code function]([:hd_url('vk_ntc')]) in use.
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
[:hd_to_key('vk_ntc')]\
As mentioned in section [:hd_link('hpf')], a hotkey parse function takes a
 virtual key name-to-code (VK_NTC for short) function as its second argument. It
 uses the VK_NTC function to resolve a name to one or a list of virtual key
 codes.

A VK_NTC function is required to take one argument: the virtual key name.

A VK_NTC function is required to return one or a list of virtual key codes.

The VK_NTC function in use can be specified via
 [argument [:var('vk_ntc_arg_flag')]]([:hd_url('vk_ntc_arg')]).

The default is [aoikhotkey.virkey::vk_ntc]([:var('vk_ntc_link')]).

The default VK_NTC function supports a reasonable set of names:
- Lowercase printable character: e.g. `{a}` is resolved to VK_KEY_A.  
  See the [full list]([:var('vk_ntc_full_list_lc')]).
- Uppercase printable character: e.g. `{A}` is resolved to VK_SHIFT and
   VK_KEY_A.  
  Note this is different with AutoHotkey, in which `A` is treated just like
   `a`, without adding a Shift.  
  See the [full list]([:var('vk_ntc_full_list_uc')]).
- Virtual key name: e.g. `{VK_HOME}` is resolved to VK_HOME.  
  See the [full list]([:var('vk_ntc_full_list_vk_name')]).
- Virtual key name without `VK_` prefix: e.g. `{HOME}` is resolved to VK_HOME.  
  See the [full list]([:var('vk_ntc_full_list_vk_name')]).
- Common name: e.g. `{ESC}` is resolved to VK_ESCAPE.  
  See the [full list]([:var('vk_ntc_full_list_vk_sname')]).

#### Virtual key translate function
[:hd_to_key('vk_tran')]\
As mentioned in section [:hd_link('hpf')], a hotkey parse function takes a
 virtual key translate (VK_TRAN for short) function as its third argument. It
 uses the VK_TRAN function to translate a neutral key with a preceding `<`
 or `>` into its sided counterpart. E.g. `<^` and `>^` will be translated into
 VK_LCONTROL and VK_RCONTROL, respectively.

A VK_TRAN function is required to take two arguments:
- A virtual key code.
- A "side" value indicating how the virtual key is sided.

A VK_TRAN function is required to return one or a list of virtual key codes.

The VK_TRAN function in use can be specified via
 [argument [:var('vk_tran_arg_flag')]]([:hd_url('vk_tran_arg')]).

The default is [aoikhotkey.virkey::vk_tran]([:var('vk_tran_link')]).

The default VK_TRAN function does the following translation:
- VK_CONTROL: to VK_LCONTROL or VK_RCONTROL
- VK_MENU: to VK_LMENU or VK_RMENU
- VK_SHIFT: to VK_LSHIFT or VK_RSHIFT
- EVK_WIN: to VK_LWIN or VK_RWIN
- VK_MOUSE_WHEEL: EVK_MOUSE_WHEEL_UP or EVK_MOUSE_WHEEL_DOWN

#### Virtual key expand function
[:hd_to_key('vk_expand')]\
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
 [argument [:var('vk_expand_arg_flag')]]([:hd_url('vk_expand_arg')]).

The default is [aoikhotkey.virkey::vk_expand]([:var('vk_expand_link')]).

The default VK_EXPAND function does the following expansion:
- VK_CONTROL: to (VK_LCONTROL, VK_RCONTROL)
- VK_MENU: to (VK_LMENU, VK_RMENU)
- VK_SHIFT: to (VK_LSHIFT, VK_RSHIFT)
- EVK_WIN: to (VK_LWIN, VK_RWIN)
- VK_MOUSE_WHEEL: to (EVK_MOUSE_WHEEL_UP, EVK_MOUSE_WHEEL_DOWN)

### Hotkey type
[:hd_to_key('hotkey_type')]\
A hotkey can be triggered by either of the three event types:
[:tod()]

#### Key down
[:hd_to_key('hotkey_type_key_down')]\
Key-down hotkey is the default hotkey type.

#### Key up
[:hd_to_key('hotkey_type_key_up')]\
Key-up hotkey can be specified by adding a beginning `~` to a hotkey definition.
This syntax is supported by the [default spec parser]([:hd_url('spf')]).

#### Key sequence
[:hd_to_key('hotkey_type_key_seq')]\
Key-sequence hotkey can be specified by adding a beginning `::` to a hotkey
 definition. This syntax is supported by the
 [default spec parser]([:hd_url('spf')]).

Unlike AutoHotkey's key-sequence hotkey that always does text substitution,
 AoikHotkey's key-sequence hotkey calls a function. To resemble AutoHotkey's
 text substitution, simply use the built-in function
 [SendSubs]([:hd_url('sendsubs')]).

Unlike AutoHotkey's key-sequence hotkey that is triggered by an extra space
 after the target key sequence, AoikHotkey's key-sequence hotkey is triggered
 as soon as the target key sequence is typed. To resemble AutoHotkey's extra
 space behaviour, simply add a space to the end of a hotkey definition.

### Hotkey function
[:hd_to_key('hotkey_func')]\
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
[:tod()]

#### Quit
[:hd_to_key('quit')]\
Quit the program.

See the [code]([:var('quit_link')]) and [example]([:var('quit_eg')]).

#### SpecReload
[:hd_to_key('spec_reload')]\
Reload the current spec.

See the [code]([:var('specreload_link')]) and [example]([:var('specreload_eg')]).

#### SpecSwitch
[:hd_to_key('spec_switch')]\
Switch to a spec.

See the [code]([:var('specswitch_link')]) and [example]([:var('specswitch_eg')]).

#### EventProp
Return True so that a key event is propagated to next handler.

See the [code]([:var('eventprop_link')]).

#### EventStop
Return False so that a key event is not propagated to next handler.

See the [code]([:var('eventstop_link')]).

#### Cmd
Run a command.

It takes a single command string and splits it into components (program and
 arguments).

The default separator is space.

If a command can not be well split on space, e.g. it has space inside some
 argument, you can either specify another separator, or use
 [Cmd2]([:hd_url('cmd2')]) instead.

See the [code]([:var('cmd_link')]) and [example]([:var('cmd_eg')]).

#### Cmd2
[:hd_to_key('cmd2')]\
Run a command.

It takes a variable-list (e.g. *args, not a list object) of command components.
 The first is the program and the rest is the arguments.

Command components can have spaces inside them.

See the [code]([:var('cmd2_link')]) and [example]([:var('cmd2_eg')]).

#### Send
[:hd_to_key('send')]\
Send keys. Similar to AutoHotkey's **Send** function.

See the [code]([:var('send_link')]) and [example]([:var('send_eg')]).

#### Send2
[Send]([:hd_url('send')]) with the **imod_dn** option set on.

Before sending keys, **Send** will first release the triggered hotkey's modifier
 keys. Otherwise the modifier keys will interfere with the keys to be sent.

After sending the keys, if the **imod_dn** option is set on, **Send** will
 re-press the triggered hotkey's modifier keys. This makes the hotkey
 repeatable. Without the re-pressing the hotkey is not repeatable because the
 hotkey's modifier keys have been released already (even though you are still
 physically pressing on them).

See the [code]([:var('send2_link')]) and [example]([:var('send2_eg')]).

#### SendSubs
[:hd_to_key('sendsubs')]
Send substitution text. Used together with a
 [key-sequence]([:hd_url('hotkey_type_key_seq')]) hotkey to implement the effect
 of text substitution. Similar to what key-sequence hotkey (e.g. `::abc::`) does
 in AutoHotkey.

See the [code]([:var('sendsubs_link')]) and [example]([:var('sendsubs_eg')]).

#### Sleep
Sleep for a while. Similar to AutoHotkey's **Sleep** function.

Note sleep will block the current thread. If the sleep time is long, you might
 want to run the hotkey function in [another thread]([:hd_url('spf')]).

See the [code]([:var('sleep_link')]) and [example]([:var('sleep_eg')]).

### Event function
[:hd_to_key('event_func')]\
If a hotkey definition is None, the hotkey function becomes an event function.

Unlike a hotkey function gets called on a specific key event, an event function
 gets called on every key event.

An event function is required to take one argument: the event object.

An event function's return value matters the same way as a
 [hotkey function]([:hd_url('hotkey_func')]) does.

### Built-in event functions
[:tod()]

#### efunc
Print message about every key event, including the overwhelming mouse move
 events.

See the [code]([:var('efunc_link')]).

#### efunc_no_mouse
Print message about every key event except mouse events.

See the [code]([:var('efunc_no_mouse_link')]) and [example]([:var('efunc_no_mouse_eg')]).

#### efunc_no_mouse_move
Print message about every key event except mouse move events.

See the [code]([:var('efunc_no_mouse_move_link')]).

## Gotchas

### Quit the program
Pressing `Ctrl Shift c` to quit the program does not work because the interrupt
 does not play well with pyHook. The right way to quit the program is choose
 a hotkey and let it call the built-in hotkey function
 [Quit]([:hd_url('quit')]). Here is an
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
