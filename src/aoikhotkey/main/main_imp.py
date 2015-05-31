# coding: utf-8
from __future__ import absolute_import

import sys

from aoikargutil import ensure_spec
from aoikexcutil import get_traceback_stxt
from aoikhotkey.const import SPEC_SWITCH_V_FIRST
from aoikhotkey.const import SPEC_SWITCH_V_LAST
from aoikhotkey.const import SPEC_SWITCH_V_NEXT
from aoikhotkey.const import SPEC_SWITCH_V_PREV
from aoikhotkey.const import SpecReloadExc
from aoikhotkey.const import SpecSwitchExc
from aoikhotkey.main.argpsr import parser_make
from aoikhotkey.main.argpsr_const import ARG_DBG_MSG_K
from aoikhotkey.main.argpsr_const import ARG_HOTKEY_PARSE_URI_K
from aoikhotkey.main.argpsr_const import ARG_HOTKEY_TFUNC_URI_K
from aoikhotkey.main.argpsr_const import ARG_REPEAT_ON_K
from aoikhotkey.main.argpsr_const import ARG_SPEC
from aoikhotkey.main.argpsr_const import ARG_SPEC_ID_K
from aoikhotkey.main.argpsr_const import ARG_SPEC_PARSE_URI_K
from aoikhotkey.main.argpsr_const import ARG_SPEC_URI_F
from aoikhotkey.main.argpsr_const import ARG_SPEC_URI_K
from aoikhotkey.main.argpsr_const import ARG_VER_ON_K
from aoikhotkey.main.argpsr_const import ARG_VK_CTN_URI_K
from aoikhotkey.main.argpsr_const import ARG_VK_EXPAND_URI_K
from aoikhotkey.main.argpsr_const import ARG_VK_NTC_URI_K
from aoikhotkey.main.argpsr_const import ARG_VK_TRAN_URI_K
from aoikhotkey.main.main_const import HOTKEY_PARSE_DYN_MOD_NAME
from aoikhotkey.main.main_const import HOTKEY_TFUNC_DYN_MOD_NAME
from aoikhotkey.main.main_const import MAIN_RET_V_EXC_LEAK_ER
from aoikhotkey.main.main_const import MAIN_RET_V_KBINT_OK
from aoikhotkey.main.main_const import MAIN_RET_V_OK
from aoikhotkey.main.main_const import MAIN_RET_V_SPEC_ID_DUPLICATE_ER
from aoikhotkey.main.main_const import MAIN_RET_V_SPEC_ID_EXCEED_ER
from aoikhotkey.main.main_const import MAIN_RET_V_SPEC_URI_ZERO_ER
from aoikhotkey.main.main_const import MAIN_RET_V_VER_SHOW_OK
from aoikhotkey.main.main_const import SPEC_DYN_MOD_NAME
from aoikhotkey.main.main_const import SPEC_PARSE_DYN_MOD_NAME
from aoikhotkey.main.main_const import VK_CTN_DYN_MOD_NAME
from aoikhotkey.main.main_const import VK_EXPAND_DYN_MOD_NAME
from aoikhotkey.main.main_const import VK_NTC_DYN_MOD_NAME
from aoikhotkey.main.main_const import VK_TRAN_DYN_MOD_NAME
from aoikhotkey.manager import HotkeyManager
from aoikhotkey.runtime import manager_set
from aoikhotkey.spec.parser import spec_parse as recovery_spec_parse
from aoikhotkey.spec.util import Quit
from aoikhotkey.spec.util import SpecReload
from aoikhotkey.spec.util import SpecSwitch
from aoikhotkey.version import __version__
from aoikimportutil import load_obj_local_or_remote
from aoikimportutil import uri_split


#/
def main_imp():
    #/
    parser = parser_make()

    #/
    args_obj = parser.parse_args()

    #/
    ensure_spec(parser, ARG_SPEC)

    #/
    dbg_msg_on = getattr(args_obj, ARG_DBG_MSG_K)

    #/
    ver_on = getattr(args_obj, ARG_VER_ON_K)

    #/
    if ver_on:
        #/
        print(__version__)

        #/
        return MAIN_RET_V_VER_SHOW_OK

    #/
    spec_uri_s = getattr(args_obj, ARG_SPEC_URI_K)

    #/
    if not spec_uri_s:
        #/
        msg = (
            '#/ Error\n'
            'No hotkey spec is given.\n'
            'Please specify at least one using option {option}.\n'
        ).format(option=ARG_SPEC_URI_F)

        sys.stderr.write(msg)

        #/
        return MAIN_RET_V_SPEC_URI_ZERO_ER

    #/
    assert len(spec_uri_s) > 0

    #/
    spec_uri_idx_max = len(spec_uri_s) - 1

    assert spec_uri_idx_max >= 0

    #/
    spec_id_s = getattr(args_obj, ARG_SPEC_ID_K)

    #/
    spec_id_s_len = len(spec_id_s)

    spec_uri_s_len = len(spec_uri_s)

    #/
    if spec_id_s_len > spec_uri_s_len:
        #/
        msg = (
            '#/ Error\n'
            '{} ids specified for {} spec{}.\n'
        ).format(
            spec_id_s_len,
            spec_uri_s_len,
            's' if spec_uri_s_len > 1 else '',
        )

        sys.stderr.write(msg)

        #/
        return MAIN_RET_V_SPEC_ID_EXCEED_ER

    assert spec_id_s_len <= spec_uri_s_len

    #/
    spec_id_to_idx_d = dict((spec_id, idx) for idx, spec_id in enumerate(spec_id_s))

    #/
    if len(spec_id_to_idx_d) != spec_id_s_len:
        #/
        msg = (
            '#/ Error\n'
            'Duplicates exist in spec ids.\n'
        )

        sys.stderr.write(msg)

        #/
        return MAIN_RET_V_SPEC_ID_DUPLICATE_ER

    #/
    is_recovery = False

    #/
    recovery_spec = [
        ('^q', Quit),
        ('^r', SpecReload),
        ('^[', SpecSwitch(SPEC_SWITCH_V_PREV)),
        ('^]', SpecSwitch(SPEC_SWITCH_V_NEXT)),
    ]

    #/
    spec_uri_idx = 0

    #/
    repeat_on = getattr(args_obj, ARG_REPEAT_ON_K)

    #/
    manager = None

    #/
    def sys_use_decide(uri, mod_uri_s_reloaded):
        #/
        _, mod_uri, _ = uri_split(uri)

        #/
        if mod_uri in mod_uri_s_reloaded:
            sys_use = True
        else:
            sys_use = False

            mod_uri_s_reloaded.append(mod_uri)

        #/
        return sys_use

    #/ loop is for implementing "reloading spec" on catching a SpecReloadExc or
    ##  SpecSwitchExc
    while True:#/
        #/
        mod_uri_s_reloaded = []

        #/
        hotkey_parse = None

        hotkey_parse_mod = None

        hotkey_tfunc = None

        hotkey_tfunc_mod = None

        vk_ntc = None

        vk_ntc_mod = None

        vk_ctn = None

        vk_ctn_mod = None

        vk_tran = None

        vk_tran_mod = None

        vk_expand = None

        vk_expand_mod = None

        #/
        if not is_recovery:
            #/
            hotkey_parse_uri = getattr(args_obj, ARG_HOTKEY_PARSE_URI_K)

            #/
            try:
                #/ "sys_use", "sys_add", and "retn_mod" are explained at 2mnIesz.
                hotkey_parse_mod, hotkey_parse = load_obj_local_or_remote(
                    hotkey_parse_uri,
                    mod_name=HOTKEY_PARSE_DYN_MOD_NAME,
                    sys_use=sys_use_decide(hotkey_parse_uri,
                        mod_uri_s_reloaded),
                    sys_add=False,
                    retn_mod=True,
                )
            except Exception:
                #/
                msg = (
                    '#/ Error\n'
                    'Failed loading spec parse function.\n'
                    'Function URI is: {func_uri}.\n'
                ).format(func_uri=hotkey_parse_uri)

                sys.stderr.write(msg)

                #/
                if dbg_msg_on:
                    #/
                    tb_msg = get_traceback_stxt()

                    sys.stderr.write('---\n{}---\n'\
                        .format(tb_msg))

                #/
                is_recovery = True

                continue

            #/
            hotkey_tfunc_uri = getattr(args_obj, ARG_HOTKEY_TFUNC_URI_K)

            #/
            try:
                #/ "sys_use", "sys_add", and "retn_mod" are explained at 2mnIesz.
                hotkey_tfunc_mod, hotkey_tfunc = load_obj_local_or_remote(
                    hotkey_tfunc_uri,
                    mod_name=HOTKEY_TFUNC_DYN_MOD_NAME,
                    sys_use=sys_use_decide(hotkey_tfunc_uri,
                        mod_uri_s_reloaded),
                    sys_add=False,
                    retn_mod=True,
                )
            except Exception:
                #/
                msg = (
                    '#/ Error\n'
                    'Failed loading hotkey trigger function.\n'
                    'Function URI is: {func_uri}.\n'
                ).format(func_uri=hotkey_tfunc_uri)

                sys.stderr.write(msg)

                #/
                if dbg_msg_on:
                    #/
                    tb_msg = get_traceback_stxt()

                    sys.stderr.write('---\n{}---\n'\
                        .format(tb_msg))

                #/
                is_recovery = True

                continue

            #/
            vk_ntc_uri = getattr(args_obj, ARG_VK_NTC_URI_K)

            #/
            try:
                #/ "sys_use", "sys_add", and "retn_mod" are explained at 2mnIesz.
                vk_ntc_mod, vk_ntc = load_obj_local_or_remote(
                    vk_ntc_uri,
                    mod_name=VK_NTC_DYN_MOD_NAME,
                    sys_use=sys_use_decide(vk_ntc_uri,
                        mod_uri_s_reloaded),
                    sys_add=False,
                    retn_mod=True,
                )
            except Exception:
                #/
                msg = (
                    '#/ Error\n'
                    'Failed loading virtual key name-to-code function.\n'
                    'Function URI is: {func_uri}.\n'
                ).format(func_uri=vk_ntc_uri)

                sys.stderr.write(msg)

                #/
                if dbg_msg_on:
                    #/
                    tb_msg = get_traceback_stxt()

                    sys.stderr.write('---\n{}---\n'\
                        .format(tb_msg))

                #/
                is_recovery = True

                continue

            #/
            vk_ctn_uri = getattr(args_obj, ARG_VK_CTN_URI_K)

            #/
            try:
                #/ "sys_use", "sys_add", and "retn_mod" are explained at 2mnIesz.
                vk_ctn_mod, vk_ctn = load_obj_local_or_remote(
                    vk_ctn_uri,
                    mod_name=VK_CTN_DYN_MOD_NAME,
                    sys_use=sys_use_decide(vk_ctn_uri,
                        mod_uri_s_reloaded),
                    sys_add=False,
                    retn_mod=True,
                )
            except Exception:
                #/
                msg = (
                    '#/ Error\n'
                    'Failed loading virtual key code-to-name function.\n'
                    'Function URI is: {func_uri}.\n'
                ).format(func_uri=vk_ctn_uri)

                sys.stderr.write(msg)

                #/
                if dbg_msg_on:
                    #/
                    tb_msg = get_traceback_stxt()

                    sys.stderr.write('---\n{}---\n'\
                        .format(tb_msg))

                #/
                is_recovery = True

                continue

            #/
            vk_tran_uri = getattr(args_obj, ARG_VK_TRAN_URI_K)

            #/
            try:
                #/ "sys_use", "sys_add", and "retn_mod" are explained at 2mnIesz.
                vk_tran_mod, vk_tran = load_obj_local_or_remote(
                    vk_tran_uri,
                    mod_name=VK_TRAN_DYN_MOD_NAME,
                    sys_use=sys_use_decide(vk_tran_uri,
                        mod_uri_s_reloaded),
                    sys_add=False,
                    retn_mod=True,
                )
            except Exception:
                #/
                msg = (
                    '#/ Error\n'
                    'Failed loading virtual key translate function.\n'
                    'Function URI is: {func_uri}.\n'
                ).format(func_uri=vk_tran_uri)

                sys.stderr.write(msg)

                #/
                if dbg_msg_on:
                    #/
                    tb_msg = get_traceback_stxt()

                    sys.stderr.write('---\n{}---\n'\
                        .format(tb_msg))

                #/
                is_recovery = True

                continue

            #/
            vk_expand_uri = getattr(args_obj, ARG_VK_EXPAND_URI_K)

            try:
                #/ "sys_use", "sys_add", and "retn_mod" are explained at 2mnIesz.
                vk_expand_mod, vk_expand = load_obj_local_or_remote(
                    vk_expand_uri,
                    mod_name=VK_EXPAND_DYN_MOD_NAME,
                    sys_use=sys_use_decide(vk_expand_uri,
                        mod_uri_s_reloaded),
                    sys_add=False,
                    retn_mod=True,
                )
            except Exception:
                #/
                msg = (
                    '#/ Error\n'
                    'Failed loading virtual key expand function.\n'
                    'Function URI is: {func_uri}.\n'
                ).format(func_uri=vk_expand_uri)

                sys.stderr.write(msg)

                #/
                if dbg_msg_on:
                    #/
                    tb_msg = get_traceback_stxt()

                    sys.stderr.write('---\n{}---\n'\
                        .format(tb_msg))

                #/
                is_recovery = True

                continue

        #/
        if manager is not None:
            manager.uninit()

            manager = None

        #/ 2mLinOP
        manager = HotkeyManager(
            hotkey_parse=hotkey_parse,
            hotkey_tfunc=hotkey_tfunc,
            vk_ntc=vk_ntc,
            vk_ctn=vk_ctn,
            vk_tran=vk_tran,
            vk_expand=vk_expand,
            repeat_on=repeat_on,
        )

        #/ 2styZ2U
        manager_set(manager)

        #/
        if is_recovery:
            #/
            spec_parse = recovery_spec_parse

            #/
            spec = recovery_spec
        #/
        else:
            #/
            spec_parse_uri = getattr(args_obj, ARG_SPEC_PARSE_URI_K)

            #/
            try:
                #/ "sys_use", "sys_add", and "retn_mod" are explained at 2mnIesz.
                spec_parse_mod, spec_parse = load_obj_local_or_remote(
                    spec_parse_uri,
                    mod_name=SPEC_PARSE_DYN_MOD_NAME,
                    sys_use=sys_use_decide(spec_parse_uri,
                        mod_uri_s_reloaded),
                    sys_add=False,
                    retn_mod=True,
                )
            except Exception:
                #/
                msg = (
                    '#/ Error\n'
                    'Failed loading spec parse function.\n'
                    'Function URI is: {func_uri}.\n'
                ).format(func_uri=spec_parse_uri)

                sys.stderr.write(msg)

                #/
                if dbg_msg_on:
                    #/
                    tb_msg = get_traceback_stxt()

                    sys.stderr.write('---\n{}---\n'\
                        .format(tb_msg))

                #/
                is_recovery = True

                continue

            #/
            spec_uri = spec_uri_s[spec_uri_idx]

            #/
            try:
                spec_id = spec_id_s[spec_uri_idx]
            except IndexError:
                spec_id = str(spec_uri_idx + 1)

            #/
            msg = '#/ Use spec {spec_id}\n{spec_uri}\n\n'\
                .format(spec_id=repr(spec_id), spec_uri=spec_uri)

            sys.stderr.write(msg)

            #/ spec must be loaded only after manager is initialized at 2styZ2U,
            ##  because spec items may access that value.
            try:
                #/ 2mnIesz
                ## "sys_use=False" forces reloading the module, instead of using
                ##  what's already in "sys.modules".
                ##
                ## "sys_add=False" avoids overriding an existing module.
                ##
                ## "retn_mod=True" keeps the module object from being gc-ed.
                spec_mod, spec = load_obj_local_or_remote(
                    spec_uri,
                    mod_name=SPEC_DYN_MOD_NAME,
                    sys_use=sys_use_decide(spec_uri,
                        mod_uri_s_reloaded),
                    sys_add=False,
                    retn_mod=True,
                )
            except Exception:
                #/
                msg = (
                    '#/ Error\n'
                    'Failed loading spec.\n'
                    'Spec URI is: {spec_uri}.\n'
                ).format(spec_uri=spec_uri)

                sys.stderr.write(msg)

                #/
                if dbg_msg_on:
                    #/
                    tb_msg = get_traceback_stxt()

                    sys.stderr.write('---\n{}---\n'\
                        .format(tb_msg))

                #/
                is_recovery = True

                continue

        #/
        try:
            #/ 3srFStM
            spec_item_s = spec_parse(spec)

            #/
            for spec_item in spec_item_s:
                #/
                if len(spec_item) == 4:
                    hotkey, hotkey_type, func, data = spec_item
                #/ To be compatible with old "spec_item" format
                elif len(spec_item) == 3:
                    hotkey, hotkey_type, func = spec_item

                    data = None
                else:
                    raise ValueError('Invalid spec item: {}'.format(spec_item))

                #/ 4qTr9wr
                #/ empty hotkey means the user wants to add event function
                if not hotkey:
                    #/
                    manager.efunc_add(func)
                else:
                    #/ 6tC5Ktw
                    manager.hotkey_add(hotkey, func=func, type=hotkey_type,
                        data=data)
        #/
        except Exception:
            #/
            msg = (
                '#/ Error\n'
                'Failed parsing spec.\n'
                'Spec URI is: {spec_uri}.\n'
            ).format(spec_uri=spec_uri)

            sys.stderr.write(msg)

            #/
            if dbg_msg_on:
                #/
                tb_msg = get_traceback_stxt()

                sys.stderr.write('---\n{}---\n'\
                    .format(tb_msg))

            #/
            is_recovery = True

            continue

        #/
        if is_recovery:
            #/
            msg = (
                '\n'
                '#/ Recovery mode\n'
                'Ctrl q: Quit the program.\n'
                'Ctrl r: Reload the current spec.\n'
                'Ctrl [: Switch to previous spec.\n'
                'Ctrl ]: Switch to next spec.\n'
                '\n'
            )

            sys.stderr.write(msg)

            #/
            is_recovery = False

        #/
        try:
            #/
            manager.eloop_run()

            #/ because SpecReloadExc or SpecSwitchExc has not been raised,
            ##  simply break out of the loop to end the program.
            break

        #/ 4tsHQTh
        except SpecReloadExc:
            #/
            continue
        #/
        except SpecSwitchExc as e:
            #/
            spec_id = e.spec_id

            #/
            error_msg = ('#/ Invalid spec id {spec_id}\n\n')\
                .format(spec_id=repr(spec_id))

            #/
            if spec_id == SPEC_SWITCH_V_FIRST:
                #/
                spec_uri_idx = 0

                #/
                assert 0 <= spec_uri_idx <= spec_uri_idx_max

                #/
                continue
            #/
            elif spec_id == SPEC_SWITCH_V_LAST:
                #/
                spec_uri_idx = spec_uri_idx_max

                #/
                assert 0 <= spec_uri_idx <= spec_uri_idx_max

                #/
                continue
            #/
            elif spec_id == SPEC_SWITCH_V_PREV:
                #/
                spec_uri_idx -= 1

                #/
                if spec_uri_idx < 0:
                    spec_uri_idx = spec_uri_idx_max

                #/
                assert 0 <= spec_uri_idx <= spec_uri_idx_max

                #/
                continue
            #/
            elif spec_id == SPEC_SWITCH_V_NEXT:
                #/
                spec_uri_idx += 1

                #/
                if spec_uri_idx > spec_uri_idx_max:
                    spec_uri_idx = 0

                #/
                assert 0 <= spec_uri_idx <= spec_uri_idx_max

                #/
                continue
            #/
            elif isinstance(spec_id, int):
                #/
                if not (0 <= spec_id <= spec_uri_idx_max):
                    #/
                    sys.stderr.write(error_msg)

                    #/
                    spec_uri_idx = spec_uri_idx
                #/
                else:
                    #/
                    spec_uri_idx = spec_id

                #/
                assert 0 <= spec_uri_idx <= spec_uri_idx_max

                #/
                continue

            elif isinstance(spec_id, str):
                #/
                idx_new = spec_id_to_idx_d.get(spec_id, None)

                #/
                if idx_new is None:
                    #/
                    sys.stderr.write(error_msg)

                    #/
                    spec_uri_idx = spec_uri_idx
                else:
                    #/
                    spec_uri_idx = idx_new

                #/
                assert 0 <= spec_uri_idx <= spec_uri_idx_max

                #/
                continue
            else:
                #/
                sys.stderr.write(error_msg)

                #/
                spec_uri_idx = spec_uri_idx

                #/
                assert 0 <= spec_uri_idx <= spec_uri_idx_max

                #/
                continue
        #/
        except Exception:
            #/
            tb_msg = get_traceback_stxt()

            sys.stderr.write('#/ Error\n---\n{}---\n'\
                .format(tb_msg))

            #/
            is_recovery = True

            continue
        #/
        finally:
            #/
            if manager is not None:
                manager.uninit()

                manager = None

    #/
    return MAIN_RET_V_OK

#/
def main():
    #/
    try:
        #/
        return main_imp()
    #/
    except KeyboardInterrupt:
        #/
        return MAIN_RET_V_KBINT_OK
    #/
    except Exception:
        #/
        tb_msg = get_traceback_stxt()

        sys.stderr.write('#/ Uncaught exception\n---\n{}---\n'.format(tb_msg))

        #/
        return MAIN_RET_V_EXC_LEAK_ER
