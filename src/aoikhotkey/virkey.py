# coding: utf-8
from __future__ import absolute_import

import re

from aoikvirkey import VK_CONTROL
from aoikvirkey import VK_DIVIDE
from aoikvirkey import VK_ESCAPE
from aoikvirkey import VK_LCONTROL
from aoikvirkey import VK_LMENU
from aoikvirkey import VK_LSHIFT
from aoikvirkey import VK_LWIN
from aoikvirkey import VK_MENU
from aoikvirkey import VK_MOUSE_LEFT_DOWN
from aoikvirkey import VK_MOUSE_LEFT_UP
from aoikvirkey import VK_MOUSE_MIDDLE_DOWN
from aoikvirkey import VK_MOUSE_MIDDLE_UP
from aoikvirkey import VK_MOUSE_RIGHT_DOWN
from aoikvirkey import VK_MOUSE_RIGHT_UP
from aoikvirkey import VK_MOUSE_WHEEL
from aoikvirkey import VK_MULTIPLY
from aoikvirkey import VK_NAME_TO_CODE_D
from aoikvirkey import VK_NEXT
from aoikvirkey import VK_NUMPAD0
from aoikvirkey import VK_NUMPAD1
from aoikvirkey import VK_NUMPAD2
from aoikvirkey import VK_NUMPAD3
from aoikvirkey import VK_NUMPAD4
from aoikvirkey import VK_NUMPAD5
from aoikvirkey import VK_NUMPAD6
from aoikvirkey import VK_NUMPAD7
from aoikvirkey import VK_NUMPAD8
from aoikvirkey import VK_NUMPAD9
from aoikvirkey import VK_PRIOR
from aoikvirkey import VK_RCONTROL
from aoikvirkey import VK_RETURN
from aoikvirkey import VK_RMENU
from aoikvirkey import VK_RSHIFT
from aoikvirkey import VK_RWIN
from aoikvirkey import VK_SHIFT
from aoikvirkey import VK_SUBTRACT
from aoikvirkey import char_to_vk
from aoikvirkey import dict_swap_kv
from aoikvirkey import upchar_to_vk
from aoikvirkey import vk_code_to_name
from aoikvirkey import vk_name_to_code


#/ "EVK" means "extended virtual key".
##
## They are not pre-defined by Windows API, and their values should not clash
##  with that of a pre-defined virtual key.
##
## They are converted into or from pre-defined virtual keys, for the convenience
##  of user.
#/ EVK_WIN will be expanded to VK_LWIN and VK_RWIN, at 3n8gHjs.
EVK_WIN = 10000

#/ VK_MOUSE_WHEEL event will be converted into either EVK_MOUSE_WHEEL_UP or
##  EVK_MOUSE_WHEEL_DOWN, at 4bIvsHS.
EVK_MOUSE_WHEEL_UP = 10001

EVK_MOUSE_WHEEL_DOWN = 10002

#/
VK_MOUSE_UP_TO_DN_D = {
    VK_MOUSE_LEFT_UP: VK_MOUSE_LEFT_DOWN,
    VK_MOUSE_RIGHT_UP: VK_MOUSE_RIGHT_DOWN,
    VK_MOUSE_MIDDLE_UP: VK_MOUSE_MIDDLE_DOWN,
}

#/
def vk_mouse_up_to_dn(vk):
    return VK_MOUSE_UP_TO_DN_D.get(vk, None)

#/
_NORM_KEY_REO = re.compile('^VK_KEY_[0-9A-Z]$')

#/ "sname" means short name
def vk_name_d_to_sname_d(di):
    #/
    res_d = {}

    for key, val in di.items():
        #/ if is 0-9 A-Z
        if _NORM_KEY_REO.match(key):
            #/
            ## 7 means strip prefix 'VK_KEY_'
            key = key[7:]
        else:
            #/
            ## 3 means strip prefix 'VK_'
            key = key[3:]

        #/
        res_d[key] = val

    #/
    return res_d

#/
VK_SNAME_TO_CODE_D = vk_name_d_to_sname_d(VK_NAME_TO_CODE_D)

#/
def vk_sname_to_code(name):
    #/
    name = name.upper()

    #/
    return VK_SNAME_TO_CODE_D.get(name, None)

#/ 2xAIF0b
#/ "EVK" means "extended virtual key"
EVK_NAME_TO_CODE_D = {
    'ESC': VK_ESCAPE,
    'SUB': VK_SUBTRACT,
    'MUL': VK_MULTIPLY,
    'DIV': VK_DIVIDE,
    'LF': VK_RETURN,
    'PGUP': VK_PRIOR,
    'PAGEUP': VK_PRIOR,
    'PGDN': VK_NEXT,
    'PAGEDOWN': VK_NEXT,
    'ENTER': VK_RETURN,
    'NUM0': VK_NUMPAD0,
    'NUM1': VK_NUMPAD1,
    'NUM2': VK_NUMPAD2,
    'NUM3': VK_NUMPAD3,
    'NUM4': VK_NUMPAD4,
    'NUM5': VK_NUMPAD5,
    'NUM6': VK_NUMPAD6,
    'NUM7': VK_NUMPAD7,
    'NUM8': VK_NUMPAD8,
    'NUM9': VK_NUMPAD9,
    'CTRL': VK_CONTROL,
    'LCTRL': VK_LCONTROL,
    'RCTRL': VK_RCONTROL,
    'ALT': VK_MENU,
    'LALT':  VK_LMENU,
    'RALT':  VK_RMENU,
    'WIN':  EVK_WIN,
    'LMOUSE': VK_MOUSE_LEFT_DOWN,
    'RMOUSE': VK_MOUSE_RIGHT_DOWN,
    'MMOUSE': VK_MOUSE_MIDDLE_DOWN,
    'WHEEL': VK_MOUSE_WHEEL,
    'WHEELUP': EVK_MOUSE_WHEEL_UP,
    'WHEELDN': EVK_MOUSE_WHEEL_DOWN,
}

#/
EVK_CODE_TO_NAME_D = dict_swap_kv(EVK_NAME_TO_CODE_D)

#/
def evk_name_to_code(name):
    name = name.upper()
    return EVK_NAME_TO_CODE_D.get(name, None)

#/ "ntc" means "name to code"
def vk_ntc(name):
    #/ can None
    code = char_to_vk(name)

    #/
    if code is not None:
        return code

    #/ can None
    code = upchar_to_vk(name)

    if code is not None:
        code_s = (VK_SHIFT, code)

        return code_s

    #/ can None
    code = vk_sname_to_code(name)

    if code is not None:
        return code

    #/
    code = vk_name_to_code(name)

    if code is not None:
        return code

    #/
    code = evk_name_to_code(name)

    if code is not None:
        return code

    #/
    return None

#/ "ctn" means "code to name"
def vk_ctn(code):
    #/ can None
    name = vk_code_to_name(code)

    #/
    if name is None:
        #/ can None
        name = EVK_CODE_TO_NAME_D.get(code, None)

    #/ can None
    return name

#/ 2aO2ipj
##
## The two-element tuple structure is required by 3mmWQKC.
VK_EXPAND_D = {
    VK_CONTROL: (VK_LCONTROL, VK_RCONTROL),
    VK_MENU: (VK_LMENU, VK_RMENU),
    VK_SHIFT: (VK_LSHIFT, VK_RSHIFT),
    #/ 3n8gHjs
    EVK_WIN: (VK_LWIN, VK_RWIN),
    VK_MOUSE_WHEEL: (EVK_MOUSE_WHEEL_UP, EVK_MOUSE_WHEEL_DOWN),
}

#/
def vk_expand(vk):
    #/
    return VK_EXPAND_D.get(vk, None)

#/
VK_TRAN_SIDE_V_NONE = None

#/ 2mVp3T2
VK_TRAN_SIDE_V_LEFT = 0

VK_TRAN_SIDE_V_RIGHT = 1

#/
def vk_tran(vk, side=VK_TRAN_SIDE_V_LEFT):
    #/
    if side not in (
        VK_TRAN_SIDE_V_NONE,
        VK_TRAN_SIDE_V_LEFT,
        VK_TRAN_SIDE_V_RIGHT,
    ):
        #/
        raise ValueError(side)

    #/
    if side == VK_TRAN_SIDE_V_NONE:
        return vk

    #/ can None
    vk_s = vk_expand(vk)

    #/
    if vk_s is None:
        return vk

    #/ 3mmWQKC
    ## "vk_s[side]" depends on the two-element tuple structure at 2aO2ipj and
    ##  depends on the two values at 2mVp3T2 being 0 and 1.
    vk_new = vk_s[side]

    #/
    return vk_new
