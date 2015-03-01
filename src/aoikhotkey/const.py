# coding: utf-8
from __future__ import absolute_import


#/
HOTKEY_TYPE_V_DN = 'dn'

HOTKEY_TYPE_V_UP = 'up'

#/ "HS" means hot sequence
HOTKEY_TYPE_V_HS = 'hs'

#/
EMASK_V_NONE = 0

EMASK_V_EFUNC = 1

EMASK_V_HOTKEY = 2

EMASK_V_HOTSEQ = 4

EMASK_V_ALL = \
    EMASK_V_EFUNC \
    | EMASK_V_HOTKEY \
    | EMASK_V_HOTSEQ

#/
ELOOP_END_CODE_V_SPEC_RELOAD = 1

ELOOP_END_CODE_V_SPEC_SWITCH = 2

#/
class SpecReloadExc(Exception): pass

#/ use tuple to avoid clashing with custom spec ids specified by user.
SPEC_SWITCH_V_PREV = ('prev',)

SPEC_SWITCH_V_NEXT = ('next',)

SPEC_SWITCH_V_FIRST = ('first',)

SPEC_SWITCH_V_LAST = ('last',)

#/
class SpecSwitchExc(Exception):

    #/
    def __init__(self, spec_id):
        self.spec_id = spec_id
