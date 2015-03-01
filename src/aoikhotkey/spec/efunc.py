# coding: utf-8
from __future__ import absolute_import

import sys

from aoikhotkey.runtime import manager_get
from aoikvirkey import VK_MOUSE_MOVE
from aoikvirkey import vk_to_char


#/
def efunc(event):
    #/
    manager = manager_get()

    #/
    if 'mouse' in event.MessageName:
        vk = event.Message
    else:
        vk = event.KeyID

    #/
    if 'mouse wheel' in event.MessageName:
        wheel_up = event.Wheel > 0

        wheel_side = 'up' if wheel_up else 'down'
    else:
        wheel_side = None

    #/
    up = 'up' in event.MessageName

    #/
    dn_vk_txt_s = [manager._vk_ctn(_vk) or str(_vk) for _vk in manager.hotkey_get_down()]

    if up:
        dn_vk_txt_s.append((manager._vk_ctn(vk) or str(vk)) + '(-)')
    else:
        dn_vk_txt_s[-1] += '(+)'

    msg = '#/ ' + ' '.join(dn_vk_txt_s) + '\n'

    sys.stderr.write(msg)

    #/
    vk_name = manager._vk_ctn(vk)

    char = vk_to_char(vk)

    #/
    msg = '{vk:<4}{vk_hex}{vk_name}{char} {msg_name}{wheel_side}\n\n'\
        .format(
            vk=vk,
            vk_hex=hex(vk),
            vk_name=' '+repr(vk_name) if vk_name is not None else '',
            msg_name=event.MessageName,
            char=' '+repr(char) if char is not None else '',
            wheel_side=' '+wheel_side if wheel_side is not None else '',
        )

    sys.stderr.write(msg)

#/
def efunc_no_mouse(event):
    #/
    if 'mouse' in event.MessageName:
        #/
        return

    #/
    return efunc(event)

#/
def efunc_no_mouse_move(event):
    #/
    if 'mouse' in event.MessageName:
        #/
        if event.Message == VK_MOUSE_MOVE:
            #/
            return

    #/
    return efunc(event)
