# coding: utf-8
from __future__ import absolute_import

from argparse import ArgumentParser

from aoikargutil import bool_0or1
from aoikhotkey.main.argpsr_const import ARG_DBG_MSG_D
from aoikhotkey.main.argpsr_const import ARG_DBG_MSG_F
from aoikhotkey.main.argpsr_const import ARG_DBG_MSG_H
from aoikhotkey.main.argpsr_const import ARG_DBG_MSG_K
from aoikhotkey.main.argpsr_const import ARG_DBG_MSG_V
from aoikhotkey.main.argpsr_const import ARG_HOTKEY_PARSE_URI_D
from aoikhotkey.main.argpsr_const import ARG_HOTKEY_PARSE_URI_F
from aoikhotkey.main.argpsr_const import ARG_HOTKEY_PARSE_URI_H
from aoikhotkey.main.argpsr_const import ARG_HOTKEY_PARSE_URI_K
from aoikhotkey.main.argpsr_const import ARG_HOTKEY_PARSE_URI_V
from aoikhotkey.main.argpsr_const import ARG_HOTKEY_TFUNC_URI_D
from aoikhotkey.main.argpsr_const import ARG_HOTKEY_TFUNC_URI_F
from aoikhotkey.main.argpsr_const import ARG_HOTKEY_TFUNC_URI_H
from aoikhotkey.main.argpsr_const import ARG_HOTKEY_TFUNC_URI_K
from aoikhotkey.main.argpsr_const import ARG_HOTKEY_TFUNC_URI_V
from aoikhotkey.main.argpsr_const import ARG_REPEAT_ON_D
from aoikhotkey.main.argpsr_const import ARG_REPEAT_ON_F
from aoikhotkey.main.argpsr_const import ARG_REPEAT_ON_H
from aoikhotkey.main.argpsr_const import ARG_REPEAT_ON_K
from aoikhotkey.main.argpsr_const import ARG_REPEAT_ON_V
from aoikhotkey.main.argpsr_const import ARG_SPEC_ID_A
from aoikhotkey.main.argpsr_const import ARG_SPEC_ID_D
from aoikhotkey.main.argpsr_const import ARG_SPEC_ID_F
from aoikhotkey.main.argpsr_const import ARG_SPEC_ID_H
from aoikhotkey.main.argpsr_const import ARG_SPEC_ID_K
from aoikhotkey.main.argpsr_const import ARG_SPEC_ID_V
from aoikhotkey.main.argpsr_const import ARG_SPEC_PARSE_URI_D
from aoikhotkey.main.argpsr_const import ARG_SPEC_PARSE_URI_F
from aoikhotkey.main.argpsr_const import ARG_SPEC_PARSE_URI_H
from aoikhotkey.main.argpsr_const import ARG_SPEC_PARSE_URI_K
from aoikhotkey.main.argpsr_const import ARG_SPEC_PARSE_URI_V
from aoikhotkey.main.argpsr_const import ARG_SPEC_URI_A
from aoikhotkey.main.argpsr_const import ARG_SPEC_URI_D
from aoikhotkey.main.argpsr_const import ARG_SPEC_URI_F
from aoikhotkey.main.argpsr_const import ARG_SPEC_URI_H
from aoikhotkey.main.argpsr_const import ARG_SPEC_URI_K
from aoikhotkey.main.argpsr_const import ARG_SPEC_URI_V
from aoikhotkey.main.argpsr_const import ARG_VER_ON_A
from aoikhotkey.main.argpsr_const import ARG_VER_ON_F
from aoikhotkey.main.argpsr_const import ARG_VER_ON_H
from aoikhotkey.main.argpsr_const import ARG_VER_ON_K
from aoikhotkey.main.argpsr_const import ARG_VK_CTN_URI_D
from aoikhotkey.main.argpsr_const import ARG_VK_CTN_URI_F
from aoikhotkey.main.argpsr_const import ARG_VK_CTN_URI_H
from aoikhotkey.main.argpsr_const import ARG_VK_CTN_URI_K
from aoikhotkey.main.argpsr_const import ARG_VK_CTN_URI_V
from aoikhotkey.main.argpsr_const import ARG_VK_EXPAND_URI_D
from aoikhotkey.main.argpsr_const import ARG_VK_EXPAND_URI_F
from aoikhotkey.main.argpsr_const import ARG_VK_EXPAND_URI_H
from aoikhotkey.main.argpsr_const import ARG_VK_EXPAND_URI_K
from aoikhotkey.main.argpsr_const import ARG_VK_EXPAND_URI_V
from aoikhotkey.main.argpsr_const import ARG_VK_NTC_URI_D
from aoikhotkey.main.argpsr_const import ARG_VK_NTC_URI_F
from aoikhotkey.main.argpsr_const import ARG_VK_NTC_URI_H
from aoikhotkey.main.argpsr_const import ARG_VK_NTC_URI_K
from aoikhotkey.main.argpsr_const import ARG_VK_NTC_URI_V
from aoikhotkey.main.argpsr_const import ARG_VK_TRAN_URI_D
from aoikhotkey.main.argpsr_const import ARG_VK_TRAN_URI_F
from aoikhotkey.main.argpsr_const import ARG_VK_TRAN_URI_H
from aoikhotkey.main.argpsr_const import ARG_VK_TRAN_URI_K
from aoikhotkey.main.argpsr_const import ARG_VK_TRAN_URI_V


#/
def parser_make():
    #/
    parser = ArgumentParser(add_help=True)

    #/
    parser.add_argument(
        ARG_SPEC_URI_F,
        dest=ARG_SPEC_URI_K,
        action=ARG_SPEC_URI_A,
        default=ARG_SPEC_URI_D,
        metavar=ARG_SPEC_URI_V,
        help=ARG_SPEC_URI_H,
    )

    #/
    parser.add_argument(
        ARG_SPEC_ID_F,
        dest=ARG_SPEC_ID_K,
        action=ARG_SPEC_ID_A,
        default=ARG_SPEC_ID_D,
        metavar=ARG_SPEC_ID_V,
        help=ARG_SPEC_ID_H,
    )

    #/
    parser.add_argument(
        ARG_SPEC_PARSE_URI_F,
        dest=ARG_SPEC_PARSE_URI_K,
        default=ARG_SPEC_PARSE_URI_D,
        metavar=ARG_SPEC_PARSE_URI_V,
        help=ARG_SPEC_PARSE_URI_H,
    )

    #/
    parser.add_argument(
        ARG_HOTKEY_PARSE_URI_F,
        dest=ARG_HOTKEY_PARSE_URI_K,
        default=ARG_HOTKEY_PARSE_URI_D,
        metavar=ARG_HOTKEY_PARSE_URI_V,
        help=ARG_HOTKEY_PARSE_URI_H,
    )

    #/
    parser.add_argument(
        ARG_HOTKEY_TFUNC_URI_F,
        dest=ARG_HOTKEY_TFUNC_URI_K,
        default=ARG_HOTKEY_TFUNC_URI_D,
        metavar=ARG_HOTKEY_TFUNC_URI_V,
        help=ARG_HOTKEY_TFUNC_URI_H,
    )

    #/
    parser.add_argument(
        ARG_VK_NTC_URI_F,
        dest=ARG_VK_NTC_URI_K,
        default=ARG_VK_NTC_URI_D,
        metavar=ARG_VK_NTC_URI_V,
        help=ARG_VK_NTC_URI_H,
    )

    #/
    parser.add_argument(
        ARG_VK_TRAN_URI_F,
        dest=ARG_VK_TRAN_URI_K,
        default=ARG_VK_TRAN_URI_D,
        metavar=ARG_VK_TRAN_URI_V,
        help=ARG_VK_TRAN_URI_H,
    )

    #/
    parser.add_argument(
        ARG_VK_EXPAND_URI_F,
        dest=ARG_VK_EXPAND_URI_K,
        default=ARG_VK_EXPAND_URI_D,
        metavar=ARG_VK_EXPAND_URI_V,
        help=ARG_VK_EXPAND_URI_H,
    )

    #/
    parser.add_argument(
        ARG_VK_CTN_URI_F,
        dest=ARG_VK_CTN_URI_K,
        default=ARG_VK_CTN_URI_D,
        metavar=ARG_VK_CTN_URI_V,
        help=ARG_VK_CTN_URI_H,
    )

    #/
    parser.add_argument(
        ARG_REPEAT_ON_F,
        dest=ARG_REPEAT_ON_K,
        type=bool_0or1,
        nargs='?',
        const=True,
        default=ARG_REPEAT_ON_D,
        metavar=ARG_REPEAT_ON_V,
        help=ARG_REPEAT_ON_H,
    )

    #/
    parser.add_argument(
        ARG_DBG_MSG_F,
        dest=ARG_DBG_MSG_K,
        type=bool_0or1,
        nargs='?',
        const=True,
        default=ARG_DBG_MSG_D,
        metavar=ARG_DBG_MSG_V,
        help=ARG_DBG_MSG_H,
    )

    #/
    parser.add_argument(
        ARG_VER_ON_F,
        dest=ARG_VER_ON_K,
        action=ARG_VER_ON_A,
        help=ARG_VER_ON_H,
    )

    #/
    return parser
