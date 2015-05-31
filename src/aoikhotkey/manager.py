# coding: utf-8
from __future__ import absolute_import

from collections import OrderedDict
from collections import deque
from contextlib import contextmanager
from copy import copy
import ctypes
from functools import partial
import sys

from aoikhotkey.const import EMASK_V_ALL
from aoikhotkey.const import EMASK_V_EFUNC
from aoikhotkey.const import EMASK_V_HOTKEY
from aoikhotkey.const import EMASK_V_HOTSEQ
from aoikhotkey.const import HOTKEY_TYPE_V_DN
from aoikhotkey.const import HOTKEY_TYPE_V_HS
from aoikhotkey.const import HOTKEY_TYPE_V_UP
from aoikhotkey.spec.parser import hotkey_parse as hotkey_parse_dft
from aoikhotkey.virkey import EVK_MOUSE_WHEEL_DOWN
from aoikhotkey.virkey import EVK_MOUSE_WHEEL_UP
from aoikhotkey.virkey import vk_ctn as vk_ctn_dft
from aoikhotkey.virkey import vk_expand as vk_expand_dft
from aoikhotkey.virkey import vk_mouse_up_to_dn
from aoikhotkey.virkey import vk_ntc as vk_ntc_dft
from aoikhotkey.virkey import vk_tran as vk_tran_dft
from pyHook import HookManager
from win32gui import PumpMessages

from aoikexcutil import get_traceback_stxt
from aoikvirkey import VK_MOUSE_WHEEL


#/
class HotkeyManager(object):

    #/
    def __init__(self,
        hotkey_parse=None,
        vk_ntc=None,
        vk_ctn=None,
        vk_tran=None,
        vk_expand=None,
        repeat_on=False,
        ):
        #/ virtuak keys that have been pressed down
        self._vk_s_dn = []

        #/ virtuak keys that have been pressed down in sequence
        self._vk_s_dn_queue = deque()

        #/ event functions
        self._efunc_s = []

        #/ hotkey down functions
        self._hk_spec_d_dn = OrderedDict()

        #/ hotkey up functions
        self._hk_spec_d_up = OrderedDict()

        #/ hot sequence functions
        self._hs_spec_d = OrderedDict()

        #/ 3c6XZC1
        ## It works like this:
        ## "hotkey_add" generates an "info id" and uses it as key to store
        ##   a hotkey's info in "self._hk_info_d".
        ## "hotkey_add" then returns this info id to the caller.
        ## "hotkey_remove" uses this info id to find the right hotkey to remove.
        self._hk_info_d = {}

        #/ end code to end func
        self._eloop_end_func_d = {}

        #/
        ## "vk_ntc" means "virtual key, name to code, function"
        self._vk_ntc = vk_ntc_dft if vk_ntc is None else vk_ntc

        #/
        ## "vk_ntc" means "virtual key, name to code, function"
        self._vk_ctn = vk_ctn_dft if vk_ctn is None else vk_ctn

        #/
        ## "vk_tran" means "virtual key, translate function"
        self._vk_tran = vk_tran_dft if vk_tran is None else vk_tran

        #/
        ## "vk_expand" means "virtual key, expand function"
        self._vk_expand = vk_expand_dft if vk_expand is None else vk_expand

        #/
        self._hotkey_parse = hotkey_parse_dft \
            if hotkey_parse is None else hotkey_parse

        #/ "emask" means "event mask"
        self._emask_v = EMASK_V_ALL

        #/ repeat mode on/off
        self._repeat_on = repeat_on

        #/ create hook manager
        self._hook_manager = HookManager()

        #/ add attributes "mouse_hook" and "keyboard_hook".
        ## Without the two attributes, a HookManager object's method "__del__"
        ##  will raise AttributeError if its methods "HookKeyboard" and
        ##  "HookMouse" have not been called.
        self._hook_manager.mouse_hook = False

        self._hook_manager.keyboard_hook = False

        #/ 2op1xV9
        #/ register event handlers with hook manager
        key_dn_hdlr = self._key_dn_hdlr

        key_up_hdlr = self._key_up_hdlr

        self._hook_manager.KeyDown = key_dn_hdlr

        self._hook_manager.KeyUp = key_up_hdlr

        self._hook_manager.MouseAllButtonsDown = key_dn_hdlr

        self._hook_manager.MouseAllButtonsUp = key_up_hdlr

        mouse_wm_func = partial(key_dn_hdlr, mouse_wm=True)

        self._hook_manager.MouseMove = mouse_wm_func

        self._hook_manager.MouseWheel = mouse_wm_func

    #/
    def uninit(self):
        """
        Object can not be reused after this method is called.
        """
        #/
        self._hook_manager.UnhookKeyboard()

        self._hook_manager.UnhookMouse()

        #/
        self._hook_manager.KeyDown = None

        self._hook_manager.KeyUp = None

        self._hook_manager.MouseAllButtonsDown = None

        self._hook_manager.MouseAllButtonsUp = None

        self._hook_manager.MouseMove = None

        self._hook_manager.MouseWheel = None

        #/
        self._hook_manager = None

        #/
        self._vk_s_dn = None

        #/
        self._vk_s_dn_queue = None

        #/
        self._efunc_s = None

        #/
        self._hk_spec_d_dn = None

        #/
        self._hk_spec_d_up = None

        #/
        self._hs_spec_d = None

        #/
        self._hk_info_d = None

        #/
        self._eloop_end_func_d = None

        #/
        self._hotkey_parse = None

        #/
        self._vk_ntc = None

        #/
        self._vk_ctn = None

        #/
        self._vk_tran = None

        #/
        self._vk_expand = None

    #/
    def efunc_add(self, func):
        #/
        self._efunc_s.append(func)

    #/
    def efunc_remove(self, func):
        #/
        self._efunc_s.remove(func)

    #/
    def _efunc_call_all(self, event, prop=None):
        #/
        if self._efunc_s:
            #/
            for efunc in self._efunc_s:
                #/
                try:
                    #/
                    prop = efunc(event)

                    #/
                    if prop is False:
                        break
                except Exception:
                    #/
                    tb_msg = get_traceback_stxt()

                    sys.stderr.write('#/ Error when calling function\n---\n{}---\n'\
                        .format(tb_msg))

        #/
        return prop

    #/
    def eloop_run(self):
        #/
        self._hook_manager.HookKeyboard()

        self._hook_manager.HookMouse()

        #/
        try:
            #/ 4hKoCbT
            #/ "PumpMessages" runs the event loop.
            end_code = PumpMessages()
        finally:
            #/
            self._hook_manager.UnhookKeyboard()

            self._hook_manager.UnhookMouse()

        #/
        end_func = self._eloop_end_func_d.pop(end_code, None)

        if end_func is not None:
             end_func()

    #/
    def eloop_end(self, code=0):
        #/ post a WM_QUIT to this thread's message queue
        ##  in order to cause the event loop running at 4hKoCbT to stop.
        ctypes.windll.user32.PostQuitMessage(code)

    #/
    def eloop_end_func_set(self, code, func):
        #/
        self._eloop_end_func_d[code] = func

    #/
    def emask_get(self):
        return self._emask_v

    #/
    def emask_set(self, mask):
        #/
        if (mask | EMASK_V_ALL) != EMASK_V_ALL:
            raise ValueError(mask)

        #/
        self._emask_v = mask

    #/
    def emask_ctx(self, emask):
        #/
        @contextmanager
        def ctx_mk():
            #/
            emask_v_old = self._emask_v

            #/
            self._emask_v = emask

            #/
            yield

            #/
            self._emask_v = emask_v_old

        #/
        return ctx_mk()

    #/
    def hotkey_parse(self, txt):
        return self._hotkey_parse(
            txt=txt,
            vk_ntc=self._vk_ntc,
            vk_tran=self._vk_tran,
        )

    #/
    def _hotkey_parse_if_str(self, hotkey):
        #/
        assert hotkey

        #/
        if isinstance(hotkey, str):
            #/
            hotkey = self.hotkey_parse(hotkey)

            assert hotkey

        #/
        return hotkey

    #/
    def _hotkey_expand(self, hotkey):
        """
        E.g. [VK_CONTROL, VK_KEY_A]
         to [[VK_LCONTROL, VK_KEY_A], [VK_RCONTROL, VK_KEY_A]]
        """
        #/
        ## The one empty list inside is for algorithm at 4ewmSrq
        item_s = [[]]

        #/
        for vk in hotkey:
            #/
            ## "exp_vk_s" is None if "vk" is not an one-to-many vk
            exp_vk_s = self._vk_expand(vk)

            if (exp_vk_s is None) or (exp_vk_s is vk):
                exp_vk_s = [vk]
            else:
                exp_vk_s = exp_vk_s

            #/
            item_new_s = []

            for exp_vk in exp_vk_s:
                #/ 4ewmSrq
                for item in item_s:
                    #/
                    item_new = copy(item)

                    item_new.append(exp_vk)

                    item_new_s.append(item_new)

            #/
            item_s = item_new_s

        #/
        return item_s

    #/
    def _hotkey_spec_d_get(self, type):
        #/
        if type == HOTKEY_TYPE_V_DN:
            res = self._hk_spec_d_dn
        elif type == HOTKEY_TYPE_V_UP:
            res = self._hk_spec_d_up
        elif type == HOTKEY_TYPE_V_HS:
            res = self._hs_spec_d
        else:
            assert 0, type

        #/
        return res

    #/
    def _hotkey_to_tup(self, hotkey, type):
        #/
        if type == HOTKEY_TYPE_V_HS:
            #/ do not sort
            hotkey_tup = tuple(hotkey)
        else:
            #/ sort
            hotkey_tup = tuple(sorted(hotkey))

        #/
        return hotkey_tup

    #/
    def _hotkey_info_id_mk(self):
        #/
        if not self._hk_info_d:
            return 1

        #/
        return max(self._hk_info_d.keys())+1

    #/
    def hotkey_add(self, hotkey, func, type=HOTKEY_TYPE_V_DN, data=None):
        #/
        hotkey_orig = hotkey

        #/ 4jpy2JA
        hotkey = self._hotkey_parse_if_str(hotkey)

        #/
        hotkey_s = self._hotkey_expand(hotkey)

        #/
        hk_spec_d = self._hotkey_spec_d_get(type)

        #/ 3ukuZyp
        hotkey_tup_s = [self._hotkey_to_tup(x, type=type) for x in hotkey_s]

        #/
        for hotkey_tup in hotkey_tup_s:
            #/
            if hotkey_tup in hk_spec_d:
                #/
                if type == HOTKEY_TYPE_V_DN:
                    up_dn_txt = ' down '
                elif type == HOTKEY_TYPE_V_UP:
                    up_dn_txt = ' up '
                else:
                    up_dn_txt = ' '

                #/
                raise ValueError(
                    ("{type}{up_dn}|{hotkey}|'s virtual keys {virkey}"
                    ' have been used already.'
                    ).format(
                        type='Hotseq' if type == HOTKEY_TYPE_V_HS else 'Hotkey',
                        up_dn=up_dn_txt,
                        hotkey=hotkey_orig,
                        virkey=hotkey_tup,
                    )
                )

            #/ 9o2zOGe
            hk_spec_d[hotkey_tup] = (func, data)

        #/ 3wTzCho
        info_tup = (hotkey, hotkey_tup_s, func, type)

        #/ Explained at 3c6XZC1
        info_id = self._hotkey_info_id_mk()

        self._hk_info_d[info_id] = info_tup

        #/
        return info_id

    #/
    def hotkey_remove(self, info_id):
        #/
        if not isinstance(info_id, int):
            #/
            raise ValueError(info_id)

        #/ "info_tup"'s format is at 3wTzCho.
        ##
        ## Can None.
        info_tup = self._hk_info_d.pop(info_id, None)

        #/
        if info_tup is None:
            return None

        #/
        _, hotkey_tup_s, _, hotkey_type = info_tup

        #/
        hk_func_pair_s = self._hotkey_spec_d_get(hotkey_type)

        #/
        for hotkey_tup in hotkey_tup_s:
            #/
            hk_func_pair_s.pop(hotkey_tup, None)

        #/
        return info_tup

    #/
    def _hotkey_spec_get(self, hotkey, type):
        #/
        hotkey_tup = self._hotkey_to_tup(hotkey, type=type)

        #/
        hotkey_func_d = self._hotkey_spec_d_get(type)

        #/ can None
        func = hotkey_func_d.get(hotkey_tup, None)

        #/
        return func

    def _hotkey_func_call(self, hotkey, type, event, prop=None):
            #/
            hotkey_is_on = False

            #/ can None
            spec = self._hotkey_spec_get(
                hotkey=hotkey, type=type)

            #/
            if spec is None:
                return (hotkey_is_on, prop)

            #/
            hotkey_is_on = True

            #/
            prop = self._hotkey_func_call_safe(
                hotkey=hotkey,
                spec=spec,
                type=type,
                event=event,
                prop=prop,
            )

            #/
            return (hotkey_is_on, prop)

    def _hotkey_func_call_safe(self, hotkey, spec, type, event, prop=None):
        #/
        if type == HOTKEY_TYPE_V_DN:
            up_dn_txt = ' down '
        elif type == HOTKEY_TYPE_V_UP:
            up_dn_txt = ' up '
        else:
            up_dn_txt = ' '

        msg = '#/ {type}{up_dn}triggered\n{virkey}\n\n'.format(
            type='Hotseq' if type == HOTKEY_TYPE_V_HS else 'Hotkey',
            up_dn=up_dn_txt,
            virkey=' '.join(self._vk_ctn(x) or str(x) for x in hotkey),
        )

        sys.stderr.write(msg)

        #/ Spec format is determined at 9o2zOGe
        func = spec[0]

        #/
        try:
            try:
                prop = func()
            #/ if TypeError occurs, assumes the function needs "event" argument
            except TypeError:
                prop = func(event)
        except Exception:
            #/
            tb_msg = get_traceback_stxt()

            sys.stderr.write('#/ Error when calling function\n---\n{}---\n'\
                .format(tb_msg))

        #/
        return prop

    #/
    def _hotseq_is_on(self, hotseq):
        #/
        hotseq_len = len(hotseq)

        #/ compare with the newest "hotseq_len" virtual keys in the queue
        try:
            for idx, vk in enumerate(hotseq):
                #/ e.g. "hotseq_len" is 2, then 0 => -2, 1 => -1
                que_idx = -hotseq_len + idx

                #/ can IndexError
                que_vk = self._vk_s_dn_queue[que_idx]

                #/
                if vk != que_vk:
                    #/
                    return False
        #/
        except IndexError:
            #/
            return False

        #/
        return True

    def _hotseq_func_call(self, vk, event, prop=None):
        """
        @param prop: propagate event
        """
        #/
        hotseq_is_on = False

        #/
        if not self._hs_spec_d:
            return (hotseq_is_on, prop)

        #/
        self._vk_s_dn_queue.append(vk)

        hotseq_len_max = 0

        for hotseq, spec in self._hs_spec_d.items():
            #/
            hotseq_len = len(hotseq)

            #/ update "hotseq_len_max"
            if hotseq_len > hotseq_len_max:
                hotseq_len_max = hotseq_len

            #/
            if self._hotseq_is_on(hotseq):
                #/
                hotseq_is_on = True

                #/
                prop = self._hotkey_func_call_safe(
                    hotkey=hotseq,
                    spec=spec,
                    type=HOTKEY_TYPE_V_HS,
                    event=event,
                    prop=prop,
                )

                #/
                break

        #/
        queue_len = len(self._vk_s_dn_queue)

        #/
        extra_len = queue_len - hotseq_len_max

        while extra_len > 0:
            #/
            self._vk_s_dn_queue.popleft()

            #/
            extra_len -= 1

        #/
        return (hotseq_is_on, prop)

    #/
    def hotkey_get_down(self):
        return self._vk_s_dn

    #/ Methods below are event handlers registered with pyhook at 2op1xV9s

    #/
    def _key_dn_hdlr(self, event, mouse_wm=False):
        """
        @mouse_wm: is handler for mouse wheel or move
        """
        #/
        if 'mouse' in event.MessageName:
            #/
            vk = event.Message

            #/ 4bIvsHS
            if vk == VK_MOUSE_WHEEL:
                #/
                if event.Wheel == 1:
                    vk = EVK_MOUSE_WHEEL_UP
                elif event.Wheel == -1:
                    vk = EVK_MOUSE_WHEEL_DOWN
                else:
                    assert 0, event.Wheel
        else:
            vk = event.KeyID

        #/
        vk_was_dn = vk in self._vk_s_dn

        #/
        try:
            self._vk_s_dn.remove(vk)
        except ValueError:
            pass

        #/
        self._vk_s_dn.append(vk)

        #/
        if vk_was_dn and not self._repeat_on:
            #/
            msg = '#/ Repeat: {}\n'.format(self._vk_ctn(vk))

            sys.stderr.write(msg)

            #/
            return True

        #/ whether propagate the event.
        ## The final decision is made at 2uq06Kk.
        prop = None

        #/
        if self._emask_v & EMASK_V_EFUNC:
            #/ can False
            prop = self._efunc_call_all(event, prop=prop)

        #/
        hotkey_is_on = False

        #/
        if (prop is not False) \
        and (self._emask_v & EMASK_V_HOTKEY):
            #/
            hotkey_is_on, prop = self._hotkey_func_call(
                hotkey=self._vk_s_dn,
                type=HOTKEY_TYPE_V_DN,
                event=event,
                prop=prop,
            )

        #/
        if (not mouse_wm) \
        and (not hotkey_is_on) \
        and (prop is not False) \
        and (self._emask_v & EMASK_V_HOTSEQ):
            #/
            hotkey_is_on, prop = self._hotseq_func_call(
                vk=vk, event=event, prop=prop)

        #/
        if mouse_wm:
            try:
                self._vk_s_dn.remove(vk)
            except ValueError:
                pass

        #/ 2uq06Kk
        prop = (not hotkey_is_on) or (prop is True)

        #/
        return prop

    #/
    def _key_up_hdlr(self, event):
        #/
        if 'mouse' in event.MessageName:
            vk = event.Message

            vk_dn = vk_mouse_up_to_dn(vk)

            assert vk_dn is not None
        else:
            vk = event.KeyID

            vk_dn = vk

        #/
        old_dn_vk_s = list(self._vk_s_dn)

        #/
        try:
            self._vk_s_dn.remove(vk_dn)
        except ValueError:
            pass

        #/ whether propagate the event.
        ## The final decision is made at 2o1h2kg.
        prop = None

        #/
        if self._emask_v & EMASK_V_EFUNC:
            #/ can False
            prop = self._efunc_call_all(event, prop=prop)

            #/
            if prop is False:
                return prop

        #/
        hotkey_is_on = False

        #/
        if self._emask_v & EMASK_V_HOTKEY:
            #/
            hotkey_is_on, prop = self._hotkey_func_call(
                hotkey=old_dn_vk_s,
                type=HOTKEY_TYPE_V_UP,
                event=event,
                prop=prop,
            )

        #/ 2o1h2kg
        prop = (not hotkey_is_on) or (prop is True)

        #/
        return prop
