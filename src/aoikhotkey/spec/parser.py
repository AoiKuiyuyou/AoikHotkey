# coding: utf-8
from __future__ import absolute_import

import functools
import os.path
import re
import webbrowser

from aoikhotkey.const import HOTKEY_TYPE_V_DN
from aoikhotkey.const import HOTKEY_TYPE_V_HS
from aoikhotkey.const import HOTKEY_TYPE_V_UP
from aoikhotkey.spec.const import OPT_THREAD
from aoikhotkey.spec.const import OPT_UP
from aoikhotkey.spec.util import CallAll
from aoikhotkey.spec.util import Cmd
from aoikhotkey.spec.util import Cmd2
from aoikhotkey.spec.util import NeedHotkeyInfo
from aoikhotkey.virkey import EVK_WIN
from aoikhotkey.virkey import VK_TRAN_SIDE_V_LEFT
from aoikhotkey.virkey import VK_TRAN_SIDE_V_NONE
from aoikhotkey.virkey import VK_TRAN_SIDE_V_RIGHT
from aoikvirkey import VK_CONTROL
from aoikvirkey import VK_MENU
from aoikvirkey import VK_SHIFT


try:
    from thread import start_new_thread # Py2
except ImportError:
    from _thread import start_new_thread # Py3

#/
def spec_parse(spec):
    """Parse "spec" into a list of (hotkey, hotkey_type, func) items that are
     ready for hotkey manager's "hotkey_add" method.

    For each spec item, "spec_parse" does a few things:
    - Extract special syntax in the hotkey into spec options, at 3sIjFrf.
      However, it does not parse the hotkey into virtual keys.
      Parsing into virtual keys is done in hotkey manager's "hotkey_add" method.

    - Normalizes a non-function into a function, at 3f7E98e.

    - Normalizes the list of functions into one function, at 3fsY1yO.

    See "spec" example at 3qMmsJ5.

    See "spec_parse" example at 3srFStM.
    """
    #/
    res_item_s = []

    #/
    for spec_item in spec:
        #/
        hotkey_spec, func_spec = spec_item[0], spec_item[1:]

        #/
        is_hotseq = False

        #/ 3sIjFrf
        if isinstance(hotkey_spec, str):
            #/
            hotkey, opt_s = hotkey_spec, []

            #/
            while True:
                #/
                if hotkey.startswith('@'):
                    #/
                    hotkey = hotkey[1:]

                    #/
                    opt_s.append(OPT_THREAD)

                #/
                elif hotkey.startswith('~'):
                    #/
                    hotkey = hotkey[1:]

                    #/
                    opt_s.append(OPT_UP)
                #/
                else:
                    break

            #/
            if hotkey.startswith('::'):
                #/
                if hotkey in ('::', ':::', '::::'):
                    raise ValueError('Hot sequence can not be empty: {}'\
                        .format(repr(hotkey)))

                #/
                is_hotseq = True

                #/
                if hotkey.endswith('::'):
                    hotkey = hotkey[2:-2]
                else:
                    hotkey = hotkey[2:]

                #/
                assert hotkey
        #/ If is list, treat as a list of virtual keys. Require code at 4jpy2JA.
        elif isinstance(hotkey_spec, list):
            #/
            hotkey, opt_s = hotkey_spec, []
        #/ If is tuple, treat the first tuple item as hotkey, and the remaining
        ##  as spec options.
        elif isinstance(hotkey_spec, tuple):
            #/
            hotkey, opt_s = hotkey_spec[0], hotkey_spec[1:]
        #/ If is None, means the user wants to add event func, not hotkey func.
        ## Require code at 4qTr9wr.
        elif hotkey_spec is None:
            #/
            hotkey, opt_s = hotkey_spec, []
        #/
        else:
            #/
            assert 0, hotkey_spec

        #/
        func_spec_2 = []

        for func_spec_item in func_spec:
            #/ 3f7E98e
            #/ convert "str" item to "Cmd"
            if isinstance(func_spec_item, str):
                #/
                if func_spec_item.startswith('http://') \
                or func_spec_item.startswith('https://'):
                    url = func_spec_item

                    #/
                    ## "webbrowser.open" returns True so need to wrap it in "f".
                    def f(url=url):
                        webbrowser.open(url)

                    #/
                    func_spec_item = f
                #/
                elif os.path.isdir(func_spec_item):
                    #/ if '/' is in the path, what is opened is always the
                    ##  user's "Documents" dir.
                    dir_path = func_spec_item.replace('/', '\\')

                    #/
                    func_spec_item = Cmd2('explorer.exe', dir_path)
                #/
                else:
                    func_spec_item = Cmd(func_spec_item)
            #/
            elif isinstance(func_spec_item, NeedHotkeyInfo):
                #/ 2cZm56O
                func_spec_item.hotkey_info_set(hotkey)
            #/
            else:
                func_spec_item = func_spec_item

            #/
            func_spec_2.append(func_spec_item)

        #/
        if len(func_spec_2) == 1:
            #/
            func = func_spec_2[0]
        else:
            #/ 3fsY1yO
            #/ combine multiple functions into one
            func = CallAll(func_spec_2)

        #/
        if OPT_THREAD in opt_s:
            func = functools.partial(start_new_thread, func, ())

        #/
        up = OPT_UP in opt_s

        #/
        if is_hotseq:
            #/
            if up:
                raise ValueError('Can not use OPT_UP with hot sequence.')

            #/
            hotkey_type = HOTKEY_TYPE_V_HS
        elif up:
            #/
            hotkey_type = HOTKEY_TYPE_V_UP
        else:
            #/
            hotkey_type = HOTKEY_TYPE_V_DN

        #/
        res_item_s.append((hotkey, hotkey_type, func))

    #/
    return res_item_s

#/
_HKP_CHAR_TO_VK = {
     '^': VK_CONTROL,
     '!': VK_MENU,
     '+': VK_SHIFT,
     '#': EVK_WIN,
}

#/ F1 to F12
_HKP_FKEY_REO = re.compile('1[0-2]|[1-9]')

#/
def hotkey_parse(txt, vk_ntc, vk_tran):
    #/
    vk_s = []

    #/
    txt_len = len(txt)

    idx = 0

    last_is_left = last_is_right = False

    while idx < txt_len:
        #/
        char = txt[idx]

        #/
        idx += 1

        #/
        is_left = is_right = False

        #/
        if char == '<':
            #/
            is_left = True
        elif char == '>':
            #/
            is_right = True
        elif char == '}':
            #/
            raise ValueError('"}" has no matching "{" before it.')
        else:
            #/
            if char == '{':
                #/ "idx + 1" to cover the "{}}" case
                idx_end = txt.find('}', idx + 1)

                #/
                if idx_end == -1:
                    raise ValueError('"{" has no matching "}" after it.')

                #/
                name = txt[idx:idx_end]

                #/
                idx = idx_end + 1

                #/
                vk = vk_ntc(name)
            #/
            elif char == 'F':
                #/ F1-F12
                next_2chars = txt[idx:idx+2]

                m_res = _HKP_FKEY_REO.match(next_2chars)

                if not m_res:
                    raise ValueError('Met "F" but is not one of F1 to F12.')

                #/
                m_txt = m_res.group()

                m_len = len(m_txt)

                idx += m_len

                #/
                name = 'F' + m_txt

                #/ require the vk_ntc in use to be able to resolve F1 to F12.
                vk = vk_ntc(name)
            #/
            else:
                #/ check if the char is a special char.
                ## can None
                vk = _HKP_CHAR_TO_VK.get(char, None)

                #/ if the char is not a special char
                if vk is None:
                    #/ treat the char as a single-char name.
                    ## can None
                    vk = vk_ntc(char)

            #/
            if vk is None:
                raise ValueError('{name} has no virtual key.'\
                    .format(name=repr(name)))

            #/
            assert vk is not None

            #/ allow "vk_ntc" to return more than one virtual key
            ## e.g. "A" -> "Shift a"
            if isinstance(vk, (list, tuple)):
                vk_new_s = vk
            else:
                vk_new_s = [vk]

            #/
            if last_is_left:
                side = VK_TRAN_SIDE_V_LEFT
            elif last_is_right:
                side = VK_TRAN_SIDE_V_RIGHT
            else:
                side = VK_TRAN_SIDE_V_NONE

            #/
            vk_new_s = [vk_tran(x, side=side) for x in vk_new_s]

            #/
            for vk_new in vk_new_s:
                #/ allow "vk_tran" to return more than one virtual key
                if isinstance(vk_new, (list, tuple)):
                    vk_s.extend(vk_new)
                else:
                    vk_s.append(vk_new)

        #/
        last_is_left = is_left

        last_is_right = is_right

    #/
    return vk_s
