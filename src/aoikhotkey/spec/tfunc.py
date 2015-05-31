# coding: utf-8
from __future__ import absolute_import

import sys

from aoikhotkey.const import HOTKEY_TYPE_V_DN
from aoikhotkey.const import HOTKEY_TYPE_V_HS
from aoikhotkey.const import HOTKEY_TYPE_V_UP


#/ Arguments format is determined at 6xn3KOu
def hotkey_tfunc(manager, hotkey, spec, type, event):
    #/
    if type == HOTKEY_TYPE_V_DN:
        up_dn_txt = ' down '
    elif type == HOTKEY_TYPE_V_UP:
        up_dn_txt = ' up '
    else:
        up_dn_txt = ' '

    #/
    msg = '#/ {type}{up_dn}triggered\n{virkey}\n\n'.format(
        type='Hotseq' if type == HOTKEY_TYPE_V_HS else 'Hotkey',
        up_dn=up_dn_txt,
        virkey=' '.join(manager._vk_ctn(x) or str(x) for x in hotkey),
    )

    #/
    sys.stderr.write(msg)
