# coding: utf-8
from __future__ import absolute_import

import ctypes
import time

from win32api import MapVirtualKey

from aoikvirkey import VK_CONTROL
from aoikvirkey import VK_LCONTROL
from aoikvirkey import VK_LMENU
from aoikvirkey import VK_LSHIFT
from aoikvirkey import VK_LWIN
from aoikvirkey import VK_MENU
from aoikvirkey import VK_RCONTROL
from aoikvirkey import VK_RMENU
from aoikvirkey import VK_RSHIFT
from aoikvirkey import VK_RWIN
from aoikvirkey import VK_SHIFT
import time as time_mod


#/
KEYEVENTF_EXTENDEDKEY = 1
KEYEVENTF_KEYUP       = 2
KEYEVENTF_UNICODE     = 4
KEYEVENTF_SCANCODE    = 8

#/ Modified from http://stackoverflow.com/a/2004267
## ---BEG
SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]
## ---END

#/
def vk_to_sc(vk, flags=0):
    #/
    sc = MapVirtualKey(vk, 0)

    #/
    if (vk >= 33 and vk <= 46) \
    or (vk >= 91 and vk <= 93):
        flags |= KEYEVENTF_EXTENDEDKEY

    #/
    return sc, flags

#/
def key_send(vk=0, scan=0, flags=0, time=0):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(vk, scan, flags, time, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

#/
def key_dn(vk=0, scan=0, flags=0, time=0):
    flags &= ~KEYEVENTF_KEYUP
    key_send(vk=vk, scan=scan, flags=flags, time=time)

#/
def key_dn_sc(vk):
    #/
    scan, flags = vk_to_sc(vk, flags=KEYEVENTF_SCANCODE)

    key_dn(scan=scan, flags=flags)

#/
def key_up(vk=0, scan=0, flags=0, time=0):
    flags |= KEYEVENTF_KEYUP
    key_send(vk=vk, scan=scan, flags=flags, time=time)

#/
def key_up_sc(vk):
    #/
    scan, flags = vk_to_sc(vk, flags=KEYEVENTF_SCANCODE)

    key_up(scan=scan, flags=flags)

#/
def key_stroke(vk=0, scan=0, flags=0, time=0, stroke_time=0.05):
    #/
    key_dn(vk=vk, scan=scan, flags=flags, time=time)

    #/
    time_mod.sleep(stroke_time)

    #/
    key_up(vk=vk, scan=scan, flags=flags, time=time)

#/
def list_diff(a, b):
    return [x for x in a if x not in b]

#/
_MOD_VK_S = (
    VK_CONTROL,
    VK_LCONTROL,
    VK_RCONTROL,
    VK_SHIFT,
    VK_LSHIFT,
    VK_RSHIFT,
    VK_MENU,
    VK_LMENU,
    VK_RMENU,
    VK_LWIN,
    VK_RWIN,
)

#/ Send keys, without being interfered by previously pressed modifier keys.
def keys_stroke(
    vk_s,
    vk_s_dn=[],
    imod_dn=False,
    inorm_up=False,
    delay=None,
    mod_dn_delay=None,
    norm_dn_delay=None,
    imod_dn_delay=None,
    ):
    """
    @param vk_s: virtual keys to send.
    @param vk_s_dn: initial virtual keys that are currently "down".
    @param imod_dn: Send "down" event for initial modifier keys in the end.
    @param inorm_up: Send "up" event for initial normal keys in the beginning.
    Normal means non-modifier.
    @param delay: Delay between sending events for two consecutive normal keys.
    A normal key may have preceding modifier keys. Delay of these modifier keys
     are controlled by "mod_dn_delay".
    @param mod_dn_delay: Delay between sending "down" events for two consecutive
     modifier keys.
    @param norm_dn_delay: Delay between sending "down" and "up" events for a
     normal key.
    @param imod_dn_delay: Delay between sending "down" events for two
     consecutive initial modifier keys.
    """
    #/
    idx = 0

    vk_s_len = len(vk_s)

    #/
    ## Init value be True is for algorithm at 2nG2AMb
    last_vk_is_mod = True

    #/
    group_s = []

    group_norm_vk_s = []

    group_mod_vk_s = []

    #/
    while idx < vk_s_len:
        #/
        vk = vk_s[idx]

        idx += 1

        #/ 2nG2AMb
        if not last_vk_is_mod:
            #/
            group_s.append((group_mod_vk_s, group_norm_vk_s))

            #/
            group_norm_vk_s = []

            group_mod_vk_s = []

        #/
        if vk in _MOD_VK_S:
            #/
            group_mod_vk_s.append(vk)

            #/
            last_vk_is_mod = True

        #/
        else:
            #/
            group_norm_vk_s.append(vk)

            #/
            last_vk_is_mod = False

    #/
    if group_mod_vk_s or group_norm_vk_s:
        #/
        group_s.append((group_mod_vk_s, group_norm_vk_s))

        #/
        group_mod_vk_s = group_norm_vk_s = None

    #/
    group_init = (
        tuple(vk for vk in vk_s_dn if vk in _MOD_VK_S),
        tuple(vk for vk in vk_s_dn if vk not in _MOD_VK_S),
    )

    #/ updated at 2b4sAfM
    group_last = group_init

    #/
    if inorm_up:
        #/
        for vk in group_init[1]:
            #/
            key_up_sc(vk)

    #/
    group_idx_max = len(group_s) - 1

    for group_idx, group in enumerate(group_s):
        #/
        mod_s_old, _ = group_last

        mod_s_new, norm_s_new = group

        #/
        mod_s_new_diff = list_diff(mod_s_new, mod_s_old)

        mod_s_old_diff = list_diff(mod_s_old, mod_s_new)

        #/ add new modifier keys
        vk_idx_max = len(mod_s_new) - 1

        for vk_idx, vk in enumerate(mod_s_new):
            #/
            key_dn_sc(vk)

            #/
            if mod_dn_delay:
                if vk_idx != vk_idx_max:
                    time.sleep(mod_dn_delay)

        #/ remove old modifier keys
        for vk in mod_s_old_diff:
            #/
            key_up_sc(vk)

        #/ stroke non-modifier keys
        vk_idx_max = len(norm_s_new) - 1

        for vk_idx, vk in enumerate(norm_s_new):
            #/
            ## Note "key_dn(vk=vk, flags=KEYEVENTF_UNICODE)" does not work for
            ##  DirectInput.
            key_dn_sc(vk)

            if norm_dn_delay:
                if vk_idx != vk_idx_max:
                    time.sleep(norm_dn_delay)

            #/
            key_up_sc(vk)

        #/ remove new modifier keys
        for vk in reversed(mod_s_new):
            key_up_sc(vk)

        #/ 2b4sAfM
        group_last = group

        #/
        if delay:
            #/
            if group_idx != group_idx_max:
                time.sleep(delay)

    #/
    if imod_dn:
        #/
        if group_last is not group_init:
            #/
            mod_s_init, _ = group_init

            #/ add initial modifier keys
            vk_idx_max = len(mod_s_init) - 1

            for vk_idx, vk in enumerate(mod_s_init):
                #/
                key_dn_sc(vk)

                #/
                if imod_dn_delay:
                    if vk_idx != vk_idx_max:
                        time.sleep(imod_dn_delay)
