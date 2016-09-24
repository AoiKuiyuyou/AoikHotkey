# coding: utf-8
"""
This module contains utility for sending key events for Windows platform.
"""
from __future__ import absolute_import

# Standard imports
import ctypes
import time as _time


# ----- Modified from http://stackoverflow.com/a/2004267 -----
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    """
    KeyBdInput structure.
    """

    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class HardwareInput(ctypes.Structure):
    """
    HardwareInput structure.
    """

    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort),
    ]


class MouseInput(ctypes.Structure):
    """
    MouseInput structure.
    """

    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class InputUnion(ctypes.Union):
    """
    Input union.
    """

    _fields_ = [
        ("ki", KeyBdInput),
        ("mi", MouseInput),
        ("hi", HardwareInput),
    ]


class Input(ctypes.Structure):
    """
    Input structure.
    """

    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii", InputUnion),
    ]
# ===== Modified from http://stackoverflow.com/a/2004267 =====


# Modifier virtual keys
_VK_CONTROL = 0x11
_VK_LCONTROL = 0xA2
_VK_RCONTROL = 0xA3
_VK_MENU = 0x12
_VK_LMENU = 0xA4
_VK_RMENU = 0xA5
_VK_SHIFT = 0x10
_VK_LSHIFT = 0xA0
_VK_RSHIFT = 0xA1
_VK_LWIN = 0x5B
_VK_RWIN = 0x5C


# Modifier virtual key set
_MODIFIER_VKS = {
    _VK_CONTROL,
    _VK_LCONTROL,
    _VK_RCONTROL,
    _VK_SHIFT,
    _VK_LSHIFT,
    _VK_RSHIFT,
    _VK_MENU,
    _VK_LMENU,
    _VK_RMENU,
    _VK_LWIN,
    _VK_RWIN,
}


# Key event flags
_KEYEVENTF_EXTENDEDKEY = 1
_KEYEVENTF_KEYUP = 2
_KEYEVENTF_UNICODE = 4
_KEYEVENTF_SCANCODE = 8


# Map virtual key to scan code
_MapVirtualKeyW = ctypes.windll.user32.MapVirtualKeyW


def vk_to_sc(vk, flags=0):
    """
    Map virtual key to scan code and flags.

    :param vk: Virtual key.

    :param flags: Flags.

    :return: A tuple of (scan_code, flags).
    """
    # Map virtual key to scan code
    sc = _MapVirtualKeyW(vk, 0)

    # If the virtual key is extended key
    if (vk >= 33 and vk <= 46) or (vk >= 91 and vk <= 93):
        # Add extended key flag
        flags |= _KEYEVENTF_EXTENDEDKEY

    # Return the scan code and flags
    return sc, flags


def key_send(vk=0, scan=0, flags=0, time=0):
    """
    Send key event.

    :param vk: Virtual key.

    :param scan: Scan code.

    :param flags: Flags.

    :param time: Time.

    :return: None.
    """
    # Create `extra` argument
    extra = ctypes.c_ulong(0)

    # Create input union
    input_union = InputUnion()

    # Create KeyBdInput structure
    input_union.ki = KeyBdInput(
        vk, scan, flags, time, ctypes.pointer(extra)
    )

    # Create Input structure
    input_struct = Input(ctypes.c_ulong(1), input_union)

    # Send input event
    ctypes.windll.user32.SendInput(
        1, ctypes.pointer(input_struct), ctypes.sizeof(input_struct)
    )


def key_dn(vk=0, scan=0, flags=0, time=0):
    """
    Send key-down event.

    :param vk: Virtual key.

    :param scan: Scan code.

    :param flags: Flags.

    :param time: Time.

    :return: None.
    """
    # Remove key-up flag
    flags &= ~_KEYEVENTF_KEYUP

    # Send key event
    key_send(vk=vk, scan=scan, flags=flags, time=time)


def key_dn_sc(vk):
    """
    Send key-down event using scan code.

    :param vk: Virtual key.

    :return: None.
    """
    # Map virtual key to scan code and flags
    scan, flags = vk_to_sc(vk, flags=_KEYEVENTF_SCANCODE)

    # Send key-down event
    key_dn(scan=scan, flags=flags)


def key_up(vk=0, scan=0, flags=0, time=0):
    """
    Send key-up event.

    :param vk: Virtual key.

    :param scan: Scan code.

    :param flags: Flags.

    :param time: Time.

    :return: None.
    """
    # Add key-up flag
    flags |= _KEYEVENTF_KEYUP

    # Send key event
    key_send(vk=vk, scan=scan, flags=flags, time=time)


def key_up_sc(vk):
    """
    Send key-up event using scan code.

    :param vk: Virtual key.

    :return: None.
    """
    # Map virtual key to scan code and flags
    scan, flags = vk_to_sc(vk, flags=_KEYEVENTF_SCANCODE)

    # Send key-up event
    key_up(scan=scan, flags=flags)


def key_stroke(vk=0, scan=0, flags=0, time=0, stroke_time=0.05):
    """
    Send key-down and key-up event.

    :param vk: Virtual key.

    :param scan: Scan code.

    :param flags: Flags.

    :param time: Time.

    :param stroke_time: Sleep time before sending key-up event.

    :return: None.
    """
    # Send key-down event
    key_dn(vk=vk, scan=scan, flags=flags, time=time)

    # Sleep
    _time.sleep(stroke_time)

    # Send key-up event
    key_up(vk=vk, scan=scan, flags=flags, time=time)


def _list_diff(a, b):
    """
    Get the difference between two lists.

    :param a: The first list.

    :param b: The second list.

    :return: A list of items that are in the first list but not in the second \
        list.
    """
    # Return the difference between two lists
    return [x for x in a if x not in b]


def keys_stroke(
    vks,
    vks_pressed=[],
    key_duration=None,
    key_interval=None,
    modifier_interval=None,
    release_initial_keys=True,
    restore_initial_modifiers=True,
):
    """
    Send keys, without being interfered by previously pressed modifier keys.

    :param vks: Virtual keys to send.

    :param vks_pressed: Virtual keys that are currently pressed.

    :param key_duration: Duration between sending key-down and key-up events \
        for a non-modifier key.

    :param key_interval: Interval between sending events for two consecutive
        non-modifier keys.

    :param modifier_interval: Delay between sending key-down events for two \
        consecutive modifier keys.

    :param release_initial_keys: Whether send key-up events to release \
        non-modifier keys that were pressed before sending the keys. Notice
        initial modifier keys will always be released to avoid interference.

    :param restore_initial_modifiers: Whether send key-down events to press \
        modifier keys that were pressed before sending the keys.

    :return: None.
    """
    # Whether last virtual key is modifier.
    # Initial value being True is required by code at 2NG2A.
    last_vk_is_modifier = True

    # Group list.
    # Each group is a tuple of (modifier_s, non_modifier_s).
    group_s = []

    # Current group's modifier virtual key list
    modifier_s = []

    # Current group's non-modifier virtual key list
    non_modifier_s = []

    # Virtual key index
    vk_idx = 0

    # Virtual key list length
    vks_len = len(vks)

    # While have remaining virtual keys
    while vk_idx < vks_len:
        # Get a virtual key
        vk = vks[vk_idx]

        # Increment the virtual key index
        vk_idx += 1

        # 2NG2A
        # If last virtual key is not modifier,
        # it means the end of a group.
        if not last_vk_is_modifier:
            # Add the group's modifiers and non-modifiers to the group list
            group_s.append((modifier_s, non_modifier_s))

            # Set the modifier virtual key list be empty for next group
            modifier_s = []

            # Set the non-modifier virtual key list be empty for next group
            non_modifier_s = []

        # If the virtual key is modifier
        if vk in _MODIFIER_VKS:
            # Add the virtual key to the modifier virtual key list
            modifier_s.append(vk)

            # Set last virtual key is modifier be True
            last_vk_is_modifier = True

        # If the virtual key is not modifier
        else:
            # Add the virtual key to the non-modifier virtual key list
            non_modifier_s.append(vk)

            # Set last virtual key is modifier be False
            last_vk_is_modifier = False

    # If the modifier or non-modifier virtual key list is not empty
    if modifier_s or non_modifier_s:
        # Add the last group's modifiers and non-modifiers to the group list
        group_s.append((modifier_s, non_modifier_s))

    # Set the modifier virtual key list be None
    modifier_s = None

    # Set the non-modifier virtual key list be None
    non_modifier_s = None

    # Get initial group's modifier and non-modifier virtual key lists
    initial_group = (
        tuple(vk for vk in vks_pressed if vk in _MODIFIER_VKS),
        tuple(vk for vk in vks_pressed if vk not in _MODIFIER_VKS),
    )

    # If need release initial non-modifier keys
    if release_initial_keys:
        # For initial group's each non-modifier virtual key
        for vk in initial_group[1]:
            # Send key-up event
            key_up_sc(vk)

    # Use the initial group as the initial previous group
    previous_group = initial_group

    # Get max group index
    group_idx_max = len(group_s) - 1

    # For the group list's each group
    for group_idx, group in enumerate(group_s):
        # Get previous group's modifiers
        modifier_s_old, _ = previous_group

        # Get current group's modifiers and non-modifiers
        modifier_s_new, non_modifier_s_new = group

        # ----- Press new modifiers -----
        # Get max index of the new modifier list
        vk_idx_max = len(modifier_s_new) - 1

        # For the new modifier list's each virtual key
        for vk_idx, vk in enumerate(modifier_s_new):
            # Send key-down event
            key_dn_sc(vk)

            # If have modifier interval
            if modifier_interval:
                # If the index is not the max index
                if vk_idx != vk_idx_max:
                    # Sleep for modifier interval
                    _time.sleep(modifier_interval)
        # ===== Press new modifiers =====

        # ----- Release old modifiers -----
        # Get the two modifier lists' difference list.
        # The difference list contains the modifiers that should be released.
        modifier_s_diff = _list_diff(modifier_s_old, modifier_s_new)

        # For the difference list's each virtual key
        for vk in modifier_s_diff:
            # Send key-up event.
            #
            # Use `key_up_sc` because `key_up` does not work for DirectInput.
            key_up_sc(vk)
        # ===== Release old modifiers =====

        # ----- Press new non-modifiers -----
        # Get max index of the new non-modifier list
        vk_idx_max = len(non_modifier_s_new) - 1

        # For the new non-modifier list's each virtual key
        for vk_idx, vk in enumerate(non_modifier_s_new):
            # Send key-down event.
            #
            # Use `key_dn_sc` because `key_dn` does not work for DirectInput.
            key_dn_sc(vk)

            # If have key duration
            if key_duration:
                # If the index is not the max index
                if vk_idx != vk_idx_max:
                    # Sleep for key duration
                    _time.sleep(key_duration)

            # Send key-up event
            key_up_sc(vk)
        # ===== Press new non-modifiers =====

        # ----- Release new non-modifiers -----
        # For the new non-modifier list's each virtual key
        for vk in reversed(modifier_s_new):
            # Send key-up event
            key_up_sc(vk)
        # ===== Release new non-modifiers =====

        # Set the previous group be the current group for next group
        previous_group = group

        # If have key interval
        if key_interval:
            # If is not the last group
            if group_idx != group_idx_max:
                # Sleep for key interval
                _time.sleep(key_interval)

    # If need restore initial modifiers after sending the keys
    if restore_initial_modifiers:
        # If the initial group is not the only group
        if previous_group is not initial_group:
            # Get initial group's modifier list
            initial_modifier_s, _ = initial_group

            # Get the max index
            vk_idx_max = len(initial_modifier_s) - 1

            # For initial group's modifier list's each virtual key
            for vk_idx, vk in enumerate(initial_modifier_s):
                # Send key-down event
                key_dn_sc(vk)

                # If have modifier interval
                if modifier_interval:
                    # If the index is not the max index
                    if vk_idx != vk_idx_max:
                        # Sleep for modifier interval
                        _time.sleep(modifier_interval)
