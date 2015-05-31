# coding: utf-8

#/
from __future__ import absolute_import

from threading import Thread

import gntp.notifier

from aoikhotkey.const import HOTKEY_TYPE_V_DN
from aoikhotkey.const import HOTKEY_TYPE_V_HS
from aoikhotkey.const import HOTKEY_TYPE_V_UP
from aoikhotkey.spec.tfunc import hotkey_tfunc as hotkey_tfunc_dft


#/
_GROWL_NOTI = gntp.notifier.GrowlNotifier(
    applicationName = 'AoikHotkey',
    notifications = ['New Messages'],
    defaultNotifications = ['New Messages'],
)
_GROWL_NOTI.register()

#/
def hotkey_tfunc(manager, hotkey, spec, type, event):
    #/ Arguments format is determined at 6xn3KOu

    #/ Call default one to print info to command console
    hotkey_tfunc_dft(manager, hotkey, spec, type, event)

    #/
    if type == HOTKEY_TYPE_V_DN:
        up_dn_txt = ' down '
    elif type == HOTKEY_TYPE_V_UP:
        up_dn_txt = ' up '
    else:
        up_dn_txt = ' '

    #/ Spec format is determined at 7asgYVg, 6tC5Ktw and 9o2zOGe
    spec_orig = spec[1]

    #/
    title = '{type}{up_dn}triggered'.format(
        type='Hotseq' if type == HOTKEY_TYPE_V_HS else 'Hotkey',
        up_dn=up_dn_txt,
    )

    #/
    hotkey_def = spec_orig[0]

    #/
    description = '{hotkey_def}\n{virkey}'.format(
        hotkey_def=hotkey_def,
        virkey=' '.join(manager._vk_ctn(x) or str(x) for x in hotkey),
    )

    #/
    th_obj = Thread(target=_GROWL_NOTI.notify, kwargs=dict(
        noteType='New Messages',
        title=title,
        description=description,
    ))

    th_obj.setDaemon(True)

    th_obj.start()
