# coding: utf-8
from __future__ import absolute_import

from functools import partial
from subprocess import Popen
from time import sleep

from aoikhotkey.const import ELOOP_END_CODE_V_SPEC_RELOAD
from aoikhotkey.const import ELOOP_END_CODE_V_SPEC_SWITCH
from aoikhotkey.const import EMASK_V_NONE
from aoikhotkey.const import SpecReloadExc
from aoikhotkey.const import SpecSwitchExc
from aoikhotkey.runtime import manager_get
from aoikhotkey.virkey import EVK_WIN
from aoiksendkey import keys_stroke
from aoikvirkey import VK_CONTROL
from aoikvirkey import VK_LCONTROL
from aoikvirkey import VK_LMENU
from aoikvirkey import VK_LSHIFT
from aoikvirkey import VK_LWIN
from aoikvirkey import VK_MENU
from aoikvirkey import VK_SHIFT


#/
MAIN_THREAD_TAG_K = '_AOIKHOTKEY_MAIN_THREAD_TAG'

#/ Decorator
def main_thread(func):
    #/
    setattr(func, MAIN_THREAD_TAG_K, True)

    #/
    return func

#/
def main_thread_tag_is_on(func):
    return getattr(func, MAIN_THREAD_TAG_K, False)

#/
NEED_EVENT_INFO_TAG_K = '_AOIKHOTKEY_NEED_EVENT_INFO_TAG'

#/ Decorator
def need_event_info_tag_set(func):
    #/
    setattr(func, NEED_EVENT_INFO_TAG_K, True)

    #/
    return func

#/
def need_event_info_tag_get(func):
    return getattr(func, NEED_EVENT_INFO_TAG_K, False)

#/
@main_thread
def Quit():
    manager_get().eloop_end()

#/
@main_thread
def SpecReload():
    #/
    end_code = ELOOP_END_CODE_V_SPEC_RELOAD

    #/
    def end_func():
        raise SpecReloadExc()

    #/
    manager = manager_get()

    #/
    manager.eloop_end_func_set(
        code=end_code,
        func=end_func,
    )

    #/
    manager.eloop_end(code=end_code)

#/
@main_thread
def spec_switch(spec_id):
    #/
    end_code = ELOOP_END_CODE_V_SPEC_SWITCH

    #/
    def end_func():
        raise SpecSwitchExc(spec_id)

    #/
    manager = manager_get()

    #/
    manager.eloop_end_func_set(
        code=end_code,
        func=end_func,
    )

    #/
    manager.eloop_end(code=end_code)

#/
@main_thread
def SpecSwitch(spec_id):
    return partial(spec_switch, spec_id)

#/
def EventProp():
    """
    Return True so that an event is propagated to next handler.
    """
    return True

#/
def EventStop():
    """
    Return False so that an event is not propagated to next handler.
    """
    return False

#/ If the spec parser at 2cZm56O meets an object of this class, it will call
##  method "hotkey_info_set".
class NeedHotkeyInfo(object):

    def hotkey_info_set(self, hotkey):
        raise NotImplementedError()

#/
class CallAll(object):

    def __init__(self, func_s):
        #/
        self.func_s = func_s

    def __call__(self):
        #/
        res = None

        #/
        for func in self.func_s:
            #/
            res = func()

            #/
            if res is False:
                return False

        #/
        return res

#/
class Cmd(object):

    def __init__(self, cmd, sep=' '):
        #/
        assert cmd

        #/
        self._cmd_part_s = cmd.split(sep)

    def __call__(self):
        Popen(self._cmd_part_s, shell=True)

#/
class Cmd2(object):

    def __init__(self, *cmd_part_s):
        #/
        assert cmd_part_s

        #/
        part_0 = cmd_part_s[0]

        #/ if first part is a list or tuple
        if isinstance(part_0, (list, tuple)):
            #/
            assert len(cmd_part_s) == 1

            #/ cover use cases e.g.
            ## Run(['echo', 'hello'])
            ## Run('echo hello'.split())
            cmd_part_s = part_0

        #/
        self._cmd_part_s = cmd_part_s

    def __call__(self):
        Popen(self._cmd_part_s, shell=True)

#/
class Send(object):

    #/
    def __init__(self, hotkey, emask=None, **kwargs):
        #/
        self._hotkey_vk_s = self._hotkey_parse(hotkey)

        #/
        self._kwargs = kwargs

        #/
        self._emask = EMASK_V_NONE \
            if emask is None else emask

    #/
    _VK_TRAN_D = {
        VK_CONTROL: VK_LCONTROL,
        VK_MENU: VK_LMENU,
        VK_SHIFT: VK_LSHIFT,
        EVK_WIN: VK_LWIN,
    }

    def _hotkey_parse(self, hotkey):
        #/
        vk_s = manager_get().hotkey_parse(hotkey)

        #/
        vk_s_new = [self._VK_TRAN_D.get(vk, vk) for vk in vk_s]

        #/
        return vk_s_new

    #/
    def __call__(self):
        #/
        manager = manager_get()

        #/
        with manager.emask_ctx(self._emask):
            #/
            vk_s_dn = manager.hotkey_get_down()

            #/
            keys_stroke(
                vk_s=self._hotkey_vk_s,
                vk_s_dn=vk_s_dn,
                **self._kwargs
            )

#/
Send2 = partial(Send, imod_dn=True)

#/
## Does not work as expected if called in another thread.
## Because algorithm at 3xa2sHI and 3hhPwJW assumes being in the same thread.
class SendSubs(NeedHotkeyInfo):

    #/
    def __init__(self, keys, **kwargs):
        #/
        self._keys = keys

        #/ initialized by 3xa2sHI
        self._back_len = 0

        #/
        self._kwargs = kwargs

    #/
    def __call__(self):
        #/ 4o5hvxR
        key_s = '{VK_BACK}' * self._back_len + self._keys

        Send(key_s, **self._kwargs)()

    #/ 3xa2sHI
    #/ called by spec parser at 2cZm56O
    def hotkey_info_set(self, hotkey):
        #/
        hotkey_vk_s = manager_get().hotkey_parse(hotkey)

        #/ 3hhPwJW
        #/ The algorithm assumes all virtual keys are printable keys
        ##
        ## "-1" is because the event of last key that triggers this hotkey is
        ##  not propagated so no need to send a VK_BACK to delete it.
        self._back_len = len(hotkey_vk_s) - 1

#/
def Sleep(tlen):
    return partial(sleep, tlen)
