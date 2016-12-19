# coding: utf-8
"""
This module contains virtual keys.
"""
from __future__ import absolute_import


# ----- Windows virtual keys -----
VK_LBUTTON = 0x1
VK_RBUTTON = 0x2
VK_CANCEL = 0x3
VK_MBUTTON = 0x4
VK_XBUTTON1 = 0x5
VK_XBUTTON2 = 0x6
VK_BACK = 0x8
VK_TAB = 0x9
VK_CLEAR = 0xC
VK_RETURN = 0xD
VK_SHIFT = 0x10
VK_CONTROL = 0x11
VK_MENU = 0x12
VK_PAUSE = 0x13
VK_CAPITAL = 0x14
VK_KANA = 0x15
VK_JUNJA = 0x17
VK_FINAL = 0x18
VK_HANJA = 0x19
VK_ESCAPE = 0x1B
VK_CONVERT = 0x1C
VK_NONCONVERT = 0x1D
VK_ACCEPT = 0x1E
VK_MODECHANGE = 0x1F
VK_SPACE = 0x20
VK_PRIOR = 0x21
VK_NEXT = 0x22
VK_END = 0x23
VK_HOME = 0x24
VK_LEFT = 0x25
VK_UP = 0x26
VK_RIGHT = 0x27
VK_DOWN = 0x28
VK_SELECT = 0x29
VK_PRINT = 0x2A
VK_EXECUTE = 0x2B
VK_SNAPSHOT = 0x2C
VK_INSERT = 0x2D
VK_DELETE = 0x2E
VK_HELP = 0x2F
VK_KEY_0 = 0x30
VK_KEY_1 = 0x31
VK_KEY_2 = 0x32
VK_KEY_3 = 0x33
VK_KEY_4 = 0x34
VK_KEY_5 = 0x35
VK_KEY_6 = 0x36
VK_KEY_7 = 0x37
VK_KEY_8 = 0x38
VK_KEY_9 = 0x39
VK_KEY_A = 0x41
VK_KEY_B = 0x42
VK_KEY_C = 0x43
VK_KEY_D = 0x44
VK_KEY_E = 0x45
VK_KEY_F = 0x46
VK_KEY_G = 0x47
VK_KEY_H = 0x48
VK_KEY_I = 0x49
VK_KEY_J = 0x4A
VK_KEY_K = 0x4B
VK_KEY_L = 0x4C
VK_KEY_M = 0x4D
VK_KEY_N = 0x4E
VK_KEY_O = 0x4F
VK_KEY_P = 0x50
VK_KEY_Q = 0x51
VK_KEY_R = 0x52
VK_KEY_S = 0x53
VK_KEY_T = 0x54
VK_KEY_U = 0x55
VK_KEY_V = 0x56
VK_KEY_W = 0x57
VK_KEY_X = 0x58
VK_KEY_Y = 0x59
VK_KEY_Z = 0x5A
VK_LWIN = 0x5B
VK_RWIN = 0x5C
VK_APPS = 0x5D
VK_SLEEP = 0x5F
VK_NUMPAD0 = 0x60
VK_NUMPAD1 = 0x61
VK_NUMPAD2 = 0x62
VK_NUMPAD3 = 0x63
VK_NUMPAD4 = 0x64
VK_NUMPAD5 = 0x65
VK_NUMPAD6 = 0x66
VK_NUMPAD7 = 0x67
VK_NUMPAD8 = 0x68
VK_NUMPAD9 = 0x69
VK_MULTIPLY = 0x6A
VK_ADD = 0x6B
VK_SEPARATOR = 0x6C
VK_SUBTRACT = 0x6D
VK_DECIMAL = 0x6E
VK_DIVIDE = 0x6F
VK_F1 = 0x70
VK_F2 = 0x71
VK_F3 = 0x72
VK_F4 = 0x73
VK_F5 = 0x74
VK_F6 = 0x75
VK_F7 = 0x76
VK_F8 = 0x77
VK_F9 = 0x78
VK_F10 = 0x79
VK_F11 = 0x7A
VK_F12 = 0x7B
VK_F13 = 0x7C
VK_F14 = 0x7D
VK_F15 = 0x7E
VK_F16 = 0x7F
VK_F17 = 0x80
VK_F18 = 0x81
VK_F19 = 0x82
VK_F20 = 0x83
VK_F21 = 0x84
VK_F22 = 0x85
VK_F23 = 0x86
VK_F24 = 0x87
VK_NUMLOCK = 0x90
VK_SCROLL = 0x91
VK_LSHIFT = 0xA0
VK_RSHIFT = 0xA1
VK_LCONTROL = 0xA2
VK_RCONTROL = 0xA3
VK_LMENU = 0xA4
VK_RMENU = 0xA5
VK_BROWSER_BACK = 0xA6
VK_BROWSER_FORWARD = 0xA7
VK_BROWSER_REFRESH = 0xA8
VK_BROWSER_STOP = 0xA9
VK_BROWSER_SEARCH = 0xAA
VK_BROWSER_FAVORITES = 0xAB
VK_BROWSER_HOME = 0xAC
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_STOP = 0xB2
VK_MEDIA_PLAY_PAUSE = 0xB3
VK_LAUNCH_MAIL = 0xB4
VK_LAUNCH_MEDIA_SELECT = 0xB5
VK_LAUNCH_APP1 = 0xB6
VK_LAUNCH_APP2 = 0xB7
# Semicolon
VK_OEM_1 = 0xBA
VK_OEM_PLUS = 0xBB
VK_OEM_COMMA = 0xBC
VK_OEM_MINUS = 0xBD
VK_OEM_PERIOD = 0xBE
# Slash
VK_OEM_2 = 0xBF
# Grave
VK_OEM_3 = 0xC0
# Left bracket
VK_OEM_4 = 0xDB
# Backslash
VK_OEM_5 = 0xDC
# Right bracket
VK_OEM_6 = 0xDD
# Apostrophe
VK_OEM_7 = 0xDE
VK_OEM_8 = 0xDF
VK_OEM_102 = 0xE2
VK_PROCESSKEY = 0xE5
VK_PACKET = 0xE7
VK_ATTN = 0xF6
VK_CRSEL = 0xF7
VK_EXSEL = 0xF8
VK_EREOF = 0xF9
VK_PLAY = 0xFA
VK_ZOOM = 0xFB
VK_NONAME = 0xFC
VK_PA1 = 0xFD
VK_OEM_CLEAR = 0xFE

# Mouse virtual keys
VK_MOUSE_MOVE = 512
VK_MOUSE_LEFT_DOWN = 513
VK_MOUSE_LEFT_UP = 514
VK_MOUSE_RIGHT_DOWN = 516
VK_MOUSE_RIGHT_UP = 517
VK_MOUSE_MIDDLE_UP = 520
VK_MOUSE_MIDDLE_DOWN = 519
VK_MOUSE_WHEEL = 522
# ===== Windows virtual keys =====


# Map name to Windows virtual key
MAP_NAME_TO_WIN_VK = dict(
    (k, v) for k, v in globals().items() if k.startswith('VK_')
)


def _dict_swap_kv(dict_obj):
    """
    Swap given dict's key-value pairs.

    :param dict_obj: Dict.

    :return: New dict with key-value pairs swapped.
    """
    # Swap given dict's keys and values
    return dict((x[1], x[0]) for x in dict_obj.items())


# Map character to Windows virtual key
MAP_CHAR_TO_WIN_VK = {
    '0': VK_KEY_0,
    '1': VK_KEY_1,
    '2': VK_KEY_2,
    '3': VK_KEY_3,
    '4': VK_KEY_4,
    '5': VK_KEY_5,
    '6': VK_KEY_6,
    '7': VK_KEY_7,
    '8': VK_KEY_8,
    '9': VK_KEY_9,
    'a': VK_KEY_A,
    'b': VK_KEY_B,
    'c': VK_KEY_C,
    'd': VK_KEY_D,
    'e': VK_KEY_E,
    'f': VK_KEY_F,
    'g': VK_KEY_G,
    'h': VK_KEY_H,
    'i': VK_KEY_I,
    'j': VK_KEY_J,
    'k': VK_KEY_K,
    'l': VK_KEY_L,
    'm': VK_KEY_M,
    'n': VK_KEY_N,
    'o': VK_KEY_O,
    'p': VK_KEY_P,
    'q': VK_KEY_Q,
    'r': VK_KEY_R,
    's': VK_KEY_S,
    't': VK_KEY_T,
    'u': VK_KEY_U,
    'v': VK_KEY_V,
    'w': VK_KEY_W,
    'x': VK_KEY_X,
    'y': VK_KEY_Y,
    'z': VK_KEY_Z,
    ' ': VK_SPACE,
    '-': VK_OEM_MINUS,
    '=': VK_OEM_PLUS,
    ';': VK_OEM_1,
    '/': VK_OEM_2,
    '`': VK_OEM_3,
    '[': VK_OEM_4,
    '\\': VK_OEM_5,
    ']': VK_OEM_6,
    "'": VK_OEM_7,
    ',': VK_OEM_COMMA,
    '.': VK_OEM_PERIOD,
    '\b': VK_BACK,
    '\t': VK_TAB,
    '\n': VK_RETURN,
}


# Map Windows virtual key to character
MAP_WIN_VK_TO_CHAR = _dict_swap_kv(MAP_CHAR_TO_WIN_VK)


# Map shifted character to Windows virtual key
MAP_SHIFTED_CHAR_TO_WIN_VK = {
    ')': VK_KEY_0,
    '!': VK_KEY_1,
    '@': VK_KEY_2,
    '#': VK_KEY_3,
    '$': VK_KEY_4,
    '%': VK_KEY_5,
    '^': VK_KEY_6,
    '&': VK_KEY_7,
    '*': VK_KEY_8,
    '(': VK_KEY_9,
    'A': VK_KEY_A,
    'B': VK_KEY_B,
    'C': VK_KEY_C,
    'D': VK_KEY_D,
    'E': VK_KEY_E,
    'F': VK_KEY_F,
    'G': VK_KEY_G,
    'H': VK_KEY_H,
    'I': VK_KEY_I,
    'J': VK_KEY_J,
    'K': VK_KEY_K,
    'L': VK_KEY_L,
    'M': VK_KEY_M,
    'N': VK_KEY_N,
    'O': VK_KEY_O,
    'P': VK_KEY_P,
    'Q': VK_KEY_Q,
    'R': VK_KEY_R,
    'S': VK_KEY_S,
    'T': VK_KEY_T,
    'U': VK_KEY_U,
    'V': VK_KEY_V,
    'W': VK_KEY_W,
    'X': VK_KEY_X,
    'Y': VK_KEY_Y,
    'Z': VK_KEY_Z,
    '_': VK_OEM_MINUS,
    '+': VK_OEM_PLUS,
    ':': VK_OEM_1,
    '?': VK_OEM_2,
    '~': VK_OEM_3,
    '{': VK_OEM_4,
    '|': VK_OEM_5,
    '}': VK_OEM_6,
    '"': VK_OEM_7,
    '<': VK_OEM_COMMA,
    '>': VK_OEM_PERIOD,
}


# Map X11 key name to Windows virtual key
MAP_X11_NAME_TO_WIN_VK = {
    'Escape': VK_ESCAPE,
    'BackSpace': VK_BACK,
    'Return': VK_RETURN,
    'Tab': VK_TAB,
    'Caps_Lock': VK_CAPITAL,
    'Shift_L': VK_LSHIFT,
    'Shift_R': VK_RSHIFT,
    'Control_L': VK_LCONTROL,
    'Control_R': VK_RCONTROL,
    'Super_L': VK_LWIN,
    'Super_R': VK_RWIN,
    'Alt_L': VK_LMENU,
    'Alt_R': VK_RMENU,
    'Menu': VK_APPS,
    'F1': VK_F1,
    'F2': VK_F2,
    'F3': VK_F3,
    'F4': VK_F4,
    'F5': VK_F5,
    'F6': VK_F6,
    'F7': VK_F7,
    'F8': VK_F8,
    'F9': VK_F9,
    'F10': VK_F10,
    'F11': VK_F11,
    'F12': VK_F12,
    'F13': VK_F13,
    'F14': VK_F14,
    'F15': VK_F15,
    'F16': VK_F16,
    'F17': VK_F17,
    'F18': VK_F18,
    'F19': VK_F19,
    'F20': VK_F20,
    'F21': VK_F21,
    'F22': VK_F22,
    'F23': VK_F23,
    'F24': VK_F24,
    '0': VK_KEY_0,
    '1': VK_KEY_1,
    '2': VK_KEY_2,
    '3': VK_KEY_3,
    '4': VK_KEY_4,
    '5': VK_KEY_5,
    '6': VK_KEY_6,
    '7': VK_KEY_7,
    '8': VK_KEY_8,
    '9': VK_KEY_9,
    'a': VK_KEY_A,
    'b': VK_KEY_B,
    'c': VK_KEY_C,
    'd': VK_KEY_D,
    'e': VK_KEY_E,
    'f': VK_KEY_F,
    'g': VK_KEY_G,
    'h': VK_KEY_H,
    'i': VK_KEY_I,
    'j': VK_KEY_J,
    'k': VK_KEY_K,
    'l': VK_KEY_L,
    'm': VK_KEY_M,
    'n': VK_KEY_N,
    'o': VK_KEY_O,
    'p': VK_KEY_P,
    'q': VK_KEY_Q,
    'r': VK_KEY_R,
    's': VK_KEY_S,
    't': VK_KEY_T,
    'u': VK_KEY_U,
    'v': VK_KEY_V,
    'w': VK_KEY_W,
    'x': VK_KEY_X,
    'y': VK_KEY_Y,
    'z': VK_KEY_Z,
    'A': VK_KEY_A,
    'B': VK_KEY_B,
    'C': VK_KEY_C,
    'D': VK_KEY_D,
    'E': VK_KEY_E,
    'F': VK_KEY_F,
    'G': VK_KEY_G,
    'H': VK_KEY_H,
    'I': VK_KEY_I,
    'J': VK_KEY_J,
    'K': VK_KEY_K,
    'L': VK_KEY_L,
    'M': VK_KEY_M,
    'N': VK_KEY_N,
    'O': VK_KEY_O,
    'P': VK_KEY_P,
    'Q': VK_KEY_Q,
    'R': VK_KEY_R,
    'S': VK_KEY_S,
    'T': VK_KEY_T,
    'U': VK_KEY_U,
    'V': VK_KEY_V,
    'W': VK_KEY_W,
    'X': VK_KEY_X,
    'Y': VK_KEY_Y,
    'Z': VK_KEY_Z,
    'grave': VK_OEM_3,
    'minus': VK_OEM_MINUS,
    'equal': VK_OEM_PLUS,
    'bracketleft': VK_OEM_4,
    'bracketright': VK_OEM_6,
    'backslash': VK_OEM_5,
    'semicolon': VK_OEM_1,
    'apostrophe': VK_OEM_7,
    'comma': VK_OEM_COMMA,
    'period': VK_OEM_PERIOD,
    'slash': VK_OEM_2,
    'Insert': VK_INSERT,
    'Delete': VK_DELETE,
    'Home': VK_HOME,
    'End': VK_END,
    'Page_Up': VK_PRIOR,
    'Next': VK_NEXT,
    'Up': VK_UP,
    'Left': VK_LEFT,
    'Right': VK_RIGHT,
    'Down': VK_DOWN,
    'Print': VK_SNAPSHOT,
    'Scroll_Lock': VK_SCROLL,
    'Pause': VK_PAUSE,
    'Num_Lock': VK_NUMLOCK,
    'P_Divide': VK_DIVIDE,
    'P_Multiply': VK_MULTIPLY,
    'P_Subtract': VK_SUBTRACT,
    'P_Add': VK_ADD,
    'P_Delete': VK_DECIMAL,
    'P_Enter': VK_RETURN,
    'P_Insert': VK_NUMPAD0,
    'P_End': VK_NUMPAD1,
    'P_Down': VK_NUMPAD2,
    'P_Next': VK_NUMPAD3,
    'P_Left': VK_NUMPAD4,
    'P_Begin': VK_NUMPAD5,
    'P_Right': VK_NUMPAD6,
    'P_Home': VK_NUMPAD7,
    'P_Up': VK_NUMPAD8,
    'P_Page_Up': VK_NUMPAD9,
}


# ----- MacOS virtual keys -----
KVK_ANSI_A = 0X00
KVK_ANSI_S = 0X01
KVK_ANSI_D = 0X02
KVK_ANSI_F = 0X03
KVK_ANSI_H = 0X04
KVK_ANSI_G = 0X05
KVK_ANSI_Z = 0X06
KVK_ANSI_X = 0X07
KVK_ANSI_C = 0X08
KVK_ANSI_V = 0X09
KVK_ANSI_B = 0X0B
KVK_ANSI_Q = 0X0C
KVK_ANSI_W = 0X0D
KVK_ANSI_E = 0X0E
KVK_ANSI_R = 0X0F
KVK_ANSI_Y = 0X10
KVK_ANSI_T = 0X11
KVK_ANSI_1 = 0X12
KVK_ANSI_2 = 0X13
KVK_ANSI_3 = 0X14
KVK_ANSI_4 = 0X15
KVK_ANSI_6 = 0X16
KVK_ANSI_5 = 0X17
KVK_ANSI_EQUAL = 0X18
KVK_ANSI_9 = 0X19
KVK_ANSI_7 = 0X1A
KVK_ANSI_MINUS = 0X1B
KVK_ANSI_8 = 0X1C
KVK_ANSI_0 = 0X1D
KVK_ANSI_RIGHTBRACKET = 0X1E
KVK_ANSI_O = 0X1F
KVK_ANSI_U = 0X20
KVK_ANSI_LEFTBRACKET = 0X21
KVK_ANSI_I = 0X22
KVK_ANSI_P = 0X23
KVK_ANSI_L = 0X25
KVK_ANSI_J = 0X26
KVK_ANSI_QUOTE = 0X27
KVK_ANSI_K = 0X28
KVK_ANSI_SEMICOLON = 0X29
KVK_ANSI_BACKSLASH = 0X2A
KVK_ANSI_COMMA = 0X2B
KVK_ANSI_SLASH = 0X2C
KVK_ANSI_N = 0X2D
KVK_ANSI_M = 0X2E
KVK_ANSI_PERIOD = 0X2F
KVK_ANSI_GRAVE = 0X32
KVK_ANSI_KEYPADDECIMAL = 0X41
KVK_ANSI_KEYPADMULTIPLY = 0X43
KVK_ANSI_KEYPADPLUS = 0X45
KVK_ANSI_KEYPADCLEAR = 0X47
KVK_ANSI_KEYPADDIVIDE = 0X4B
KVK_ANSI_KEYPADENTER = 0X4C
KVK_ANSI_KEYPADMINUS = 0X4E
KVK_ANSI_KEYPADEQUALS = 0X51
KVK_ANSI_KEYPAD0 = 0X52
KVK_ANSI_KEYPAD1 = 0X53
KVK_ANSI_KEYPAD2 = 0X54
KVK_ANSI_KEYPAD3 = 0X55
KVK_ANSI_KEYPAD4 = 0X56
KVK_ANSI_KEYPAD5 = 0X57
KVK_ANSI_KEYPAD6 = 0X58
KVK_ANSI_KEYPAD7 = 0X59
KVK_ANSI_KEYPAD8 = 0X5B
KVK_ANSI_KEYPAD9 = 0X5C
KVK_RETURN = 0X24
KVK_TAB = 0X30
KVK_SPACE = 0X31
KVK_DELETE = 0X33
KVK_ESCAPE = 0X35
KVK_RIGHTCOMMAND = 0X36
KVK_COMMAND = 0X37
KVK_SHIFT = 0X38
KVK_CAPSLOCK = 0X39
KVK_OPTION = 0X3A
KVK_CONTROL = 0X3B
KVK_RIGHTSHIFT = 0X3C
KVK_RIGHTOPTION = 0X3D
KVK_RIGHTCONTROL = 0X3E
KVK_FUNCTION = 0X3F
KVK_F17 = 0X40
KVK_VOLUMEUP = 0X48
KVK_VOLUMEDOWN = 0X49
KVK_MUTE = 0X4A
KVK_F18 = 0X4F
KVK_F19 = 0X50
KVK_F20 = 0X5A
KVK_F5 = 0X60
KVK_F6 = 0X61
KVK_F7 = 0X62
KVK_F3 = 0X63
KVK_F8 = 0X64
KVK_F9 = 0X65
KVK_F11 = 0X67
KVK_F13 = 0X69
KVK_F16 = 0X6A
KVK_F14 = 0X6B
KVK_F10 = 0X6D
KVK_F12 = 0X6F
KVK_F15 = 0X71
KVK_HELP = 0X72
KVK_HOME = 0X73
KVK_PAGEUP = 0X74
KVK_FORWARDDELETE = 0X75
KVK_F4 = 0X76
KVK_END = 0X77
KVK_F2 = 0X78
KVK_PAGEDOWN = 0X79
KVK_F1 = 0X7A
KVK_LEFTARROW = 0X7B
KVK_RIGHTARROW = 0X7C
KVK_DOWNARROW = 0X7D
KVK_UPARROW = 0X7E
# ===== MacOS virtual keys =====


# Map name to MacOS virtual key
MAP_NAME_TO_MAC_VK = dict(
    (k, v) for k, v in globals().items() if k.startswith('KVK_')
)


# Map Windows virtual key to MacOS virtual key
MAP_WIN_VK_TO_MAC_VK = {
    VK_ESCAPE: KVK_ESCAPE,
    VK_BACK: KVK_DELETE,
    VK_RETURN: KVK_RETURN,
    VK_TAB: KVK_TAB,
    VK_CAPITAL: KVK_CAPSLOCK,
    VK_LSHIFT: KVK_SHIFT,
    VK_RSHIFT: KVK_RIGHTSHIFT,
    VK_LCONTROL: KVK_CONTROL,
    VK_RCONTROL: KVK_RIGHTCONTROL,
    VK_LWIN: KVK_COMMAND,
    VK_RWIN: KVK_RIGHTCOMMAND,
    VK_LMENU: KVK_OPTION,
    VK_RMENU: KVK_RIGHTOPTION,
    VK_F1: KVK_F1,
    VK_F2: KVK_F2,
    VK_F3: KVK_F3,
    VK_F4: KVK_F4,
    VK_F5: KVK_F5,
    VK_F6: KVK_F6,
    VK_F7: KVK_F7,
    VK_F8: KVK_F8,
    VK_F9: KVK_F9,
    VK_F10: KVK_F10,
    VK_F11: KVK_F11,
    VK_F12: KVK_F12,
    VK_F13: KVK_F13,
    VK_F14: KVK_F14,
    VK_F15: KVK_F15,
    VK_F16: KVK_F16,
    VK_F17: KVK_F17,
    VK_F18: KVK_F18,
    VK_F19: KVK_F19,
    VK_F20: KVK_F20,
    VK_KEY_0: KVK_ANSI_0,
    VK_KEY_1: KVK_ANSI_1,
    VK_KEY_2: KVK_ANSI_2,
    VK_KEY_3: KVK_ANSI_3,
    VK_KEY_4: KVK_ANSI_4,
    VK_KEY_5: KVK_ANSI_5,
    VK_KEY_6: KVK_ANSI_6,
    VK_KEY_7: KVK_ANSI_7,
    VK_KEY_8: KVK_ANSI_8,
    VK_KEY_9: KVK_ANSI_9,
    VK_KEY_A: KVK_ANSI_A,
    VK_KEY_B: KVK_ANSI_B,
    VK_KEY_C: KVK_ANSI_C,
    VK_KEY_D: KVK_ANSI_D,
    VK_KEY_E: KVK_ANSI_E,
    VK_KEY_F: KVK_ANSI_F,
    VK_KEY_G: KVK_ANSI_G,
    VK_KEY_H: KVK_ANSI_H,
    VK_KEY_I: KVK_ANSI_I,
    VK_KEY_J: KVK_ANSI_J,
    VK_KEY_K: KVK_ANSI_K,
    VK_KEY_L: KVK_ANSI_L,
    VK_KEY_M: KVK_ANSI_M,
    VK_KEY_N: KVK_ANSI_N,
    VK_KEY_O: KVK_ANSI_O,
    VK_KEY_P: KVK_ANSI_P,
    VK_KEY_Q: KVK_ANSI_Q,
    VK_KEY_R: KVK_ANSI_R,
    VK_KEY_S: KVK_ANSI_S,
    VK_KEY_T: KVK_ANSI_T,
    VK_KEY_U: KVK_ANSI_U,
    VK_KEY_V: KVK_ANSI_V,
    VK_KEY_W: KVK_ANSI_W,
    VK_KEY_X: KVK_ANSI_X,
    VK_KEY_Y: KVK_ANSI_Y,
    VK_KEY_Z: KVK_ANSI_Z,
    VK_OEM_3: KVK_ANSI_GRAVE,
    VK_OEM_MINUS: KVK_ANSI_MINUS,
    VK_OEM_PLUS: KVK_ANSI_EQUAL,
    VK_OEM_4: KVK_ANSI_LEFTBRACKET,
    VK_OEM_6: KVK_ANSI_RIGHTBRACKET,
    VK_OEM_5: KVK_ANSI_BACKSLASH,
    VK_OEM_1: KVK_ANSI_SEMICOLON,
    VK_OEM_7: KVK_ANSI_QUOTE,
    VK_OEM_COMMA: KVK_ANSI_COMMA,
    VK_OEM_PERIOD: KVK_ANSI_PERIOD,
    VK_OEM_2: KVK_ANSI_SLASH,
    VK_DELETE: KVK_FORWARDDELETE,
    VK_HOME: KVK_HOME,
    VK_END: KVK_END,
    VK_PRIOR: KVK_PAGEUP,
    VK_NEXT: KVK_PAGEDOWN,
    VK_UP: KVK_UPARROW,
    VK_LEFT: KVK_LEFTARROW,
    VK_RIGHT: KVK_RIGHTARROW,
    VK_DOWN: KVK_DOWNARROW,
    VK_DIVIDE: KVK_ANSI_KEYPADDIVIDE,
    VK_MULTIPLY: KVK_ANSI_KEYPADMULTIPLY,
    VK_SUBTRACT: KVK_ANSI_KEYPADMINUS,
    VK_ADD: KVK_ANSI_KEYPADPLUS,
    VK_DECIMAL: KVK_ANSI_KEYPADDECIMAL,
    VK_NUMPAD1: KVK_ANSI_KEYPAD1,
    VK_NUMPAD2: KVK_ANSI_KEYPAD2,
    VK_NUMPAD3: KVK_ANSI_KEYPAD3,
    VK_NUMPAD4: KVK_ANSI_KEYPAD4,
    VK_NUMPAD5: KVK_ANSI_KEYPAD5,
    VK_NUMPAD6: KVK_ANSI_KEYPAD6,
    VK_NUMPAD7: KVK_ANSI_KEYPAD7,
    VK_NUMPAD8: KVK_ANSI_KEYPAD8,
    VK_NUMPAD9: KVK_ANSI_KEYPAD9,
}


# Extended virtual keys.
#
# Extended virtual keys are not pre-defined by OSes. Their values should not
# clash with pre-defined virtual keys.
EVK_CTRL = 10001
EVK_WIN = 10002
EVK_ALT = 10003
EVK_SHIFT = 10004

# VK_MOUSE_WHEEL event will be converted to either EVK_MOUSE_WHEEL_UP or
# EVK_MOUSE_WHEEL_DOWN, by hotkey manager at 4BIVS.
EVK_MOUSE_WHEEL_UP = 11001

EVK_MOUSE_WHEEL_DOWN = 11002


# Map mouse button-up virtual key to corresponding button-down virtual key
MAP_MOUSE_UP_VK_TO_DN_VK = {
    VK_MOUSE_LEFT_UP: VK_MOUSE_LEFT_DOWN,
    VK_MOUSE_RIGHT_UP: VK_MOUSE_RIGHT_DOWN,
    VK_MOUSE_MIDDLE_UP: VK_MOUSE_MIDDLE_DOWN,
}
