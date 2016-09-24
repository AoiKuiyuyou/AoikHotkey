# coding: utf-8
"""
This module contains hotkey parse function.
"""
from __future__ import absolute_import

# Standard imports
from copy import copy
import re

# Local imports
from .compat import IS_MACOS
from .virtualkey import EVK_ALT
from .virtualkey import EVK_CTRL
from .virtualkey import EVK_MOUSE_WHEEL_DOWN
from .virtualkey import EVK_MOUSE_WHEEL_UP
from .virtualkey import EVK_SHIFT
from .virtualkey import EVK_WIN
from .virtualkey import KVK_COMMAND
from .virtualkey import KVK_CONTROL
from .virtualkey import KVK_OPTION
from .virtualkey import KVK_RIGHTCOMMAND
from .virtualkey import KVK_RIGHTCONTROL
from .virtualkey import KVK_RIGHTOPTION
from .virtualkey import KVK_RIGHTSHIFT
from .virtualkey import KVK_SHIFT
from .virtualkey import MAP_CHAR_TO_WIN_VK
from .virtualkey import MAP_NAME_TO_MAC_VK
from .virtualkey import MAP_NAME_TO_WIN_VK
from .virtualkey import MAP_SHIFTED_CHAR_TO_WIN_VK
from .virtualkey import MAP_WIN_VK_TO_MAC_VK
from .virtualkey import VK_DIVIDE
from .virtualkey import VK_ESCAPE
from .virtualkey import VK_LCONTROL
from .virtualkey import VK_LMENU
from .virtualkey import VK_LSHIFT
from .virtualkey import VK_LWIN
from .virtualkey import VK_MOUSE_LEFT_DOWN
from .virtualkey import VK_MOUSE_LEFT_UP
from .virtualkey import VK_MOUSE_MIDDLE_DOWN
from .virtualkey import VK_MOUSE_MIDDLE_UP
from .virtualkey import VK_MOUSE_MOVE
from .virtualkey import VK_MOUSE_RIGHT_DOWN
from .virtualkey import VK_MOUSE_RIGHT_UP
from .virtualkey import VK_MOUSE_WHEEL
from .virtualkey import VK_MULTIPLY
from .virtualkey import VK_NEXT
from .virtualkey import VK_NUMPAD0
from .virtualkey import VK_NUMPAD1
from .virtualkey import VK_NUMPAD2
from .virtualkey import VK_NUMPAD3
from .virtualkey import VK_NUMPAD4
from .virtualkey import VK_NUMPAD5
from .virtualkey import VK_NUMPAD6
from .virtualkey import VK_NUMPAD7
from .virtualkey import VK_NUMPAD8
from .virtualkey import VK_NUMPAD9
from .virtualkey import VK_OEM_1
from .virtualkey import VK_OEM_2
from .virtualkey import VK_OEM_3
from .virtualkey import VK_OEM_4
from .virtualkey import VK_OEM_5
from .virtualkey import VK_OEM_6
from .virtualkey import VK_OEM_7
from .virtualkey import VK_PRIOR
from .virtualkey import VK_RCONTROL
from .virtualkey import VK_RETURN
from .virtualkey import VK_RMENU
from .virtualkey import VK_RSHIFT
from .virtualkey import VK_RWIN
from .virtualkey import VK_SUBTRACT


def _dict_swap_kv(dict_obj):
    """
    Swap given dict's key-value pairs.

    :param dict_obj: Dict.

    :return: New dict with key-value pairs swapped.
    """
    # Swap given dict's keys and values
    return dict((x[1], x[0]) for x in dict_obj.items())


def _extend_short_names(name_to_vk_map, keep_orig=True):
    """
    Extend given `name to virtual key` map with short names.

    Rules for converting standard name to short name:
        VK_KEY_A -> A
        VK_HOME -> HOME
        KVK_ANSI_A -> A
        KVK_HOME -> HOME

    :param name_to_vk_map: Name to virtual key map.

    :param keep_orig: Whether keep original names.

    :return: New `name to virtual key` map with short names added.
    """
    # Result dict
    res_dict = {}

    # For given `name to virtual key` map's each item
    for name, vk in name_to_vk_map.items():
        # If need keep original names
        if keep_orig:
            # Add the original name to the result dict
            res_dict[name] = vk

        # Short name
        short_name = None

        # If the name starts with `VK_KEY_`
        if name.startswith('VK_KEY_'):
            # Strip prefix `VK_KEY_`, e.g. `VK_KEY_A` -> `A`
            short_name = name[7:]

        # If the name not starts with `VK_KEY_`.

        # If the name starts with `VK_`.
        elif name.startswith('VK_'):
            # Strip prefix `VK_`, e.g. `VK_HOME` -> `HOME`
            short_name = name[3:]

        # If the name starts with `KVK_ANSI_`
        elif name.startswith('KVK_ANSI_'):
            # Strip prefix `KVK_ANSI_`, e.g. `KVK_ANSI_A` -> `A`
            short_name = name[9:]

        # If the name not starts with `KVK_ANSI_`.

        # If the name starts with `KVK_`.
        elif name.startswith('KVK_'):
            # Strip prefix `KVK_`, e.g. `KVK_HOME` -> `HOME`
            short_name = name[4:]

        # If the name is none of above
        else:
            # Set short name be None
            short_name = None

        # If short name is found
        if short_name is not None:
            # Add the short name to the result dict
            res_dict[short_name] = vk

    # Return the result dict
    return res_dict


# Map standard name or short name to MacOS virtual key
_MAP_NAME_SHORT_NAME_TO_MAC_VK = _extend_short_names(MAP_NAME_TO_MAC_VK)


# Map custom name to Windows virtual key
_MAP_CUSTOM_NAME_TO_WIN_VK = {
    '^': EVK_CTRL,
    '#': EVK_WIN,
    '!': EVK_ALT,
    '+': EVK_SHIFT,
    'ESC': VK_ESCAPE,
    'SUB': VK_SUBTRACT,
    'MUL': VK_MULTIPLY,
    'DIV': VK_DIVIDE,
    'PAGEUP': VK_PRIOR,
    'PAGEDOWN': VK_NEXT,
    'ENTER': VK_RETURN,
    'PAD0': VK_NUMPAD0,
    'PAD1': VK_NUMPAD1,
    'PAD2': VK_NUMPAD2,
    'PAD3': VK_NUMPAD3,
    'PAD4': VK_NUMPAD4,
    'PAD5': VK_NUMPAD5,
    'PAD6': VK_NUMPAD6,
    'PAD7': VK_NUMPAD7,
    'PAD8': VK_NUMPAD8,
    'PAD9': VK_NUMPAD9,
    'CTRL': EVK_CTRL,
    'LCTRL': VK_LCONTROL,
    'RCTRL': VK_RCONTROL,
    'ALT': EVK_ALT,
    'LALT': VK_LMENU,
    'RALT': VK_RMENU,
    'OPT': EVK_ALT,
    'LOPT': VK_LMENU,
    'ROPT': VK_RMENU,
    'OPTION': EVK_ALT,
    'LOPTION': VK_LMENU,
    'ROPTION': VK_RMENU,
    'WIN': EVK_WIN,
    'CMD': EVK_WIN,
    'LCMD': VK_LWIN,
    'RCMD': VK_RWIN,
    'COMMAND': EVK_WIN,
    'LCOMMAND': VK_LWIN,
    'RCOMMAND': VK_RWIN,
    'SHIFT': EVK_SHIFT,
    'LMOUSE': VK_MOUSE_LEFT_DOWN,
    'LMOUSEUP': VK_MOUSE_LEFT_UP,
    'RMOUSE': VK_MOUSE_RIGHT_DOWN,
    'RMOUSEUP': VK_MOUSE_RIGHT_UP,
    'MMOUSE': VK_MOUSE_MIDDLE_DOWN,
    'MMOUSEUP': VK_MOUSE_MIDDLE_UP,
    'WHEEL': VK_MOUSE_WHEEL,
    'WHEELUP': EVK_MOUSE_WHEEL_UP,
    'WHEELDN': EVK_MOUSE_WHEEL_DOWN,
    'MOUSEMOVE': VK_MOUSE_MOVE,
    'SEMICOLON': VK_OEM_1,
    'SLASH': VK_OEM_2,
    'GRAVE': VK_OEM_3,
    'LBRACKET': VK_OEM_4,
    'BACKSLASH': VK_OEM_5,
    'RBRACKET': VK_OEM_6,
    'APOSTROPHE': VK_OEM_7,
    'QUOTE': VK_OEM_7,
    'PAGEUP': VK_PRIOR,
    'PAGEDN': VK_NEXT,
}


# Map standard name or short name to Windows virtual key
_MAP_NAME_SHORT_NAME_TO_WIN_VK = _extend_short_names(MAP_NAME_TO_WIN_VK)


def _map_name_to_win_vk(name):
    """
    Map given name to Windows virtual key.

    :param name: Name.

    :return: Windows virtual key, or None if not found.
    """
    # Map custom name to Windows virtual key.
    # Custom name is mapped first for `^`, `#`, `!`, `+` to mean modifier keys.
    vk = _MAP_CUSTOM_NAME_TO_WIN_VK.get(name.upper(), None)

    # If virtual key is found
    if vk is not None:
        # Return the virtual key
        return vk

    # If virtual key is not found.

    # Map character to Windows virtual key
    vk = MAP_CHAR_TO_WIN_VK.get(name, None)

    # If virtual key is found
    if vk is not None:
        # Return the virtual key
        return vk

    # If virtual key is not found.

    # Map shifted character to Windows virtual key
    vk = MAP_SHIFTED_CHAR_TO_WIN_VK.get(name, None)

    # If virtual key is found
    if vk is not None:
        # Prefix the virtual key with EVK_SHIFT
        vk_s = [EVK_SHIFT, vk]

        # Return the virtual key tuple
        return vk_s

    # If virtual key is not found.

    # Map standard name or short name to Windows virtual key
    vk = _MAP_NAME_SHORT_NAME_TO_WIN_VK.get(name.upper(), None)

    # If virtual key is found
    if vk is not None:
        # Return the virtual key
        return vk

    # If virtual key is not found.

    # Return None
    return None


def vk_ntc(name):
    """
    Map given name to virtual key.

    :param name: Name.

    :return: Virtual key, or None if not found.
    """
    # If the platform is MacOS
    if IS_MACOS:
        # Map standard name or short name to MacOS virtual key
        mac_vk = _MAP_NAME_SHORT_NAME_TO_MAC_VK.get(name.upper(), None)

        # If virtual key is found
        if mac_vk is not None:
            # Return the virtual key
            return mac_vk

    # Map standard name or short name to Windows virtual key.
    win_vk = _map_name_to_win_vk(name)

    # If virtual key is found
    if win_vk is not None:
        # If the platform is MacOS
        if IS_MACOS:
            # If the virtual key is pre-defined
            if win_vk < 1000:
                # Map the Windows virtual key to MacOS virtual key.
                # May be None.
                vk = MAP_WIN_VK_TO_MAC_VK.get(win_vk, None)

            # If the virtual key is not pre-defined,
            # it means the virtual key is extended virtual key, e.g. EVK_CTRL.
            # Extended virtual keys will be processed by hotkey parse function.
            else:
                # Use the virtual key as-is
                vk = win_vk

            # Return the virtual key, or None
            return vk

    # Return the virtual key, or None
    return win_vk


# Map Windows virtual key to custom name
_MAP_WIN_VK_TO_CUSTOM_NAME = {}

# Add standard names
_MAP_WIN_VK_TO_CUSTOM_NAME.update(_dict_swap_kv(MAP_NAME_TO_WIN_VK))

# Add short names
_MAP_WIN_VK_TO_CUSTOM_NAME.update(
    _dict_swap_kv(_extend_short_names(MAP_NAME_TO_WIN_VK, keep_orig=False))
)

# Add custom names
_MAP_WIN_VK_TO_CUSTOM_NAME.update(_dict_swap_kv(_MAP_CUSTOM_NAME_TO_WIN_VK))

# Specify custom names for virtual keys that have multiple custom names
_MAP_WIN_VK_TO_CUSTOM_NAME.update({
    EVK_CTRL: 'ECTRL',
    EVK_WIN: 'EWIN',
    EVK_ALT: 'EALT',
    EVK_SHIFT: 'ESHIFT',
    VK_LCONTROL: 'LCTRL',
    VK_RCONTROL: 'RCTRL',
    VK_LWIN: 'LWIN',
    VK_RWIN: 'RWIN',
    VK_LMENU: 'LALT',
    VK_RMENU: 'RALT',
    VK_LSHIFT: 'LSHIFT',
    VK_RSHIFT: 'RSHIFT',
    VK_ESCAPE: 'ESC',
})


# Map MacOS virtual key to custom name
_MAP_MAC_VK_TO_CUSTOM_NAME = {}

# Add standard names
_MAP_MAC_VK_TO_CUSTOM_NAME.update(_dict_swap_kv(MAP_NAME_TO_MAC_VK))

# Add short names
_MAP_MAC_VK_TO_CUSTOM_NAME.update(
    _dict_swap_kv(_extend_short_names(MAP_NAME_TO_MAC_VK, keep_orig=False))
)


def vk_ctn(vk):
    """
    Map given virtual key to name.

    :param vk: Virtual key.

    :return: Virtual key's name, or None if not found.
    """
    # If the platform is MacOS
    if IS_MACOS:
        # Map given virtual key to name.
        # May be None.
        return _MAP_MAC_VK_TO_CUSTOM_NAME.get(vk, None)

    # If the platform is not MacOS.
    else:
        # Map given virtual key to name.
        # May be None.
        return _MAP_WIN_VK_TO_CUSTOM_NAME.get(vk, None)


# 2AO2I
# Map virtual key to a tuple containing two sided Windows virtual keys.
#
# The two-item tuple structure is required by 3MMWQ.
_MAP_VK_TO_SIDED_WIN_VK_TUPLE = {
    EVK_CTRL: (VK_LCONTROL, VK_RCONTROL),
    EVK_WIN: (VK_LWIN, VK_RWIN),
    EVK_ALT: (VK_LMENU, VK_RMENU),
    EVK_SHIFT: (VK_LSHIFT, VK_RSHIFT),
    VK_MOUSE_WHEEL: (EVK_MOUSE_WHEEL_UP, EVK_MOUSE_WHEEL_DOWN),
}

# Map virtual key to a tuple containing two sided MacOS virtual keys.
#
# The two-item tuple structure is required by 3MMWQ.
_MAP_VK_TO_SIDED_MAC_VK_TUPLE = {
    EVK_CTRL: (KVK_CONTROL, KVK_RIGHTCONTROL),
    EVK_WIN: (KVK_COMMAND, KVK_RIGHTCOMMAND),
    EVK_ALT: (KVK_OPTION, KVK_RIGHTOPTION),
    EVK_SHIFT: (KVK_SHIFT, KVK_RIGHTSHIFT),
    VK_MOUSE_WHEEL: (EVK_MOUSE_WHEEL_UP, EVK_MOUSE_WHEEL_DOWN),
}


def vk_expand(vk):
    """
    Expand given virtual key to a tuple containing two sided virtual keys.

    :param vk: Virtual key.

    :return: A tuple containing two sided virtual keys, or None if given \
        virtual key can not be expanded.
    """
    # If the platform is MacOS
    if IS_MACOS:
        # Expand given virtual key
        return _MAP_VK_TO_SIDED_MAC_VK_TUPLE.get(vk, None)

    # If the platform is not MacOS
    else:
        # Expand given virtual key
        return _MAP_VK_TO_SIDED_WIN_VK_TUPLE.get(vk, None)


# 2MVP3
# Transform side types.
#
# Transform side: none
VK_TRAN_SIDE_V_NONE = None

# Transform side: left
VK_TRAN_SIDE_V_LEFT = 0

# Transform side: right
VK_TRAN_SIDE_V_RIGHT = 1


def vk_tran(vk, side=VK_TRAN_SIDE_V_LEFT):
    """
    Transform given virtual key to sided virtual key.
    """
    # If given side is not valid
    if side not in {
        VK_TRAN_SIDE_V_NONE,
        VK_TRAN_SIDE_V_LEFT,
        VK_TRAN_SIDE_V_RIGHT,
    }:
        # Raise error
        raise ValueError(side)

    # If given side is valid.

    # If given side is none
    if side == VK_TRAN_SIDE_V_NONE:
        # Return given virtual key
        return vk

    # If given side is not none.

    # Expand given virtual key to two sided virtual keys
    vk_s = vk_expand(vk)

    # If given virtual key has no corresponding sided virtual keys
    if vk_s is None:
        # Return given virtual key
        return vk

    # If given virtual key has corresponding sided virtual keys.

    # 3MMWQ
    # Get sided virtual key
    #
    # Code `vk_s[side]` assumes the two-item tuple structure at 2AO2I and the
    # side values defined at 2MVP3 being 0 and 1.
    sided_vk = vk_s[side]

    # Return the sided virtual key
    return sided_vk


# RE object to match function key names F1 to F24
_FUNC_KEY_NAME_REO = re.compile('2[0-4]|1[0-9]|[1-9]')


def hotkey_parse_inner(pattern, vk_ntc, vk_tran, vk_expand):
    """
    Hotkey parse function's inner function.

    :param pattern: Hotkey pattern.

    :param vk_ntc: Name to virtual key function.

    :param vk_tran: Virtual key transform function.

    :param vk_expand: Virtual key expand function.

    :return: Hotkey list. Each hotkey is a virtual key list.
    """
    # Virtual key list
    vk_s = []

    # Get hotkey pattern length
    pattern_len = len(pattern)

    # Pattern character index
    idx = 0

    # Whether last character is left-side marker
    last_is_left = False

    # Whether last character is right-side marker
    last_is_right = False

    # While have unparsed part
    while idx < pattern_len:
        # Get current character
        char = pattern[idx]

        # Increment the character index
        idx += 1

        # Whether the character is left-side marker
        is_left = False

        # Whether the character is right-side marker
        is_right = False

        # Virtual key
        vk = None

        # If the character is `<`
        if char == '<':
            # Set is left-side marker be True
            is_left = True

        # If the character is `>`
        elif char == '>':
            # Set is right-side marker be True
            is_right = True

        # If the character is `}`
        elif char == '}':
            # Get error message
            msg = '"}" has no matching "{" before it.'

            # Raise error
            raise ValueError(msg)

        # If the character is not `<`, `>`, or `}`
        else:
            # If the character is `{`
            if char == '{':
                # Find next `}` character's index.
                #
                # `idx + 1` aims to cover the `{}}` situation.
                idx_end = pattern.find('}', idx + 1)

                # If next `}` character's index is not found
                if idx_end == -1:
                    # Get error message
                    msg = '"{" has no matching "}" after it.'

                    # Raise error
                    raise ValueError(msg)

                # If next `}` character's index is found.

                # Get the name inside the curly braces
                name = pattern[idx:idx_end]

                # Move forward the character index
                idx = idx_end + 1

                # Get the name's virtual key.
                # May be None, which will be handled below.
                vk = vk_ntc(name)

            # If the character is `F`
            elif char == 'F':
                # Get next two characters.
                #
                # E.g. F1 to F24
                next_2chars = pattern[idx:idx + 2]

                # Match the next two characters
                matched = _FUNC_KEY_NAME_REO.match(next_2chars)

                # If not matched
                if not matched:
                    # Get error message
                    msg = 'Met "F" but is not one of F1 to F24.'

                    # Raise error
                    raise ValueError(msg)

                # Get matched text
                matched_text = matched.group()

                # Get matched text length
                matched_text_len = len(matched_text)

                # Move forward the character index
                idx += matched_text_len

                # Get the name
                name = 'F' + matched_text

                # Get the name's virtual key.
                # May be None, which will be handled below.
                vk = vk_ntc(name)

            # If the character is none of above
            else:
                # Use the character as name
                name = char

                # Get the name's virtual key.
                # May be None, which will be handled below.
                vk = vk_ntc(name)

            # If virtual key is not found
            if vk is None:
                # Get error message
                msg = '{name} has no virtual key.'.format(name=repr(name))

                # Raise error
                raise ValueError(msg)

            # If virtual key is found.

            # If the virtual key is virtual key list.
            #
            # This aims to allow `vk_ntc` to return virtual key list,
            # e.g. Map name 'A' to [EVK_SHIFT, VK_KEY_A].
            if isinstance(vk, list):
                # Use the virtual key list
                vk_list = vk

            # If the virtual key is not virtual key list
            else:
                # Create virtual key list containing the virtual key
                vk_list = [vk]

            # If left-side marker is on
            if last_is_left:
                # Set side be left side
                side = VK_TRAN_SIDE_V_LEFT

            # If right-side marker is on
            elif last_is_right:
                # Set side be right side
                side = VK_TRAN_SIDE_V_RIGHT

            # If left-side and right-side are not on
            else:
                # Set side be none side
                side = VK_TRAN_SIDE_V_NONE

            # Transform the virtual key list to sided value
            vk_list = [vk_tran(x, side=side) for x in vk_list]

            # For each transformed virtual key
            for transformed_vk in vk_list:
                # If the transformed virtual key is virtual key list.
                #
                # This aims to allow `vk_tran` to return virtual key list.
                if isinstance(transformed_vk, (list, tuple)):
                    # Add the virtual key list to the result
                    vk_s.extend(transformed_vk)

                # If the transformed virtual key is not virtual key list
                else:
                    # Add the virtual key to the result
                    vk_s.append(transformed_vk)

        # Store whether left-side marker is on
        last_is_left = is_left

        # Store whether right-side marker is on
        last_is_right = is_right

    # Expand the virtual key list to multiple virtual key lists.
    # E.g. [CTRL, A] -> [[LCTRL, A], [RCTRL, A]]
    hotkey_s = _hotkey_expand(vk_s, vk_expand)

    # Return a list of virtual key lists
    return hotkey_s


def _hotkey_expand(hotkey, vk_expand):
    """
    Expand given virtual key list to multiple virtual key lists.

    Expansion is needed because some virtual keys are one-to-many.
    E.g. [CTRL, A] -> [[LCTRL, A], [RCTRL, A]]

    :param hotkey: Virtual key list.

    :param vk_expand: Virtual key expand function.

    :return: A list of virtual key lists.
    """
    # Hotkey list.
    # Each hotkey is a virtual key list.
    # The one empty list inside is for code at 4EWMS.
    hotkey_s = [[]]

    # For given virtual key list's each virtual key
    for vk in hotkey:
        # Expand the virtual key.
        # May be None.
        exp_vk_s = vk_expand(vk)

        # If the expanded result is None,
        # or the expanded result is the original virtual key.
        if (exp_vk_s is None) or (exp_vk_s is vk):
            # Create expanded list containing only the original virtual key
            exp_vk_s = [vk]

        # If the expanded result is not None or the original virtual key
        else:
            # Use the expanded list
            exp_vk_s = exp_vk_s

        # New hotkey list
        new_hotkey_s = []

        # For the expanded list's each virtual key
        for exp_vk in exp_vk_s:
            # 4EWMS
            # For the hotkey list's each hotkey
            for old_hotkey in hotkey_s:
                # Copy the hotkey
                new_hotkey = copy(old_hotkey)

                # Append the virtual key in the expanded list to the hotkey
                new_hotkey.append(exp_vk)

                # Add the new hotkey to the new hotkey list
                new_hotkey_s.append(new_hotkey)

        # Store the new hotkey list
        hotkey_s = new_hotkey_s

    # Return the expanded hotkey list
    return hotkey_s


def hotkey_parse(pattern):
    """
    Hotkey parse function.

    :param pattern: Hotkey pattern.

    :return: Hotkey list. Each hotkey is a virtual key list.
    """
    # Delegate call to `hotkey_parse_inner`
    return hotkey_parse_inner(
        pattern,
        vk_ntc=vk_ntc,
        vk_tran=vk_tran,
        vk_expand=vk_expand,
    )
