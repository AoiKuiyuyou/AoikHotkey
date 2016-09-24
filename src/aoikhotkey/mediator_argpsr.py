# coding: utf-8
"""
This module contains arguments parser.
"""
from __future__ import absolute_import

# Standard imports
from argparse import ArgumentParser


# Definition pf arguments.
#
# `F` means flag.
# `K` means destination key.
# `A` means action.
# `D` means default.
# `V` means meta variable.
# `H` means help.
#
# Help
ARG_HELP_ON_F = '-h'
ARG_HELP_ON_F2 = '--help'

# Hotkey spec URI
ARG_SPEC_URI_F = '-s'
ARG_SPEC_URI_K = 'ARG_SPEC_URI_K'
ARG_SPEC_URI_A = 'append'
ARG_SPEC_URI_D = []
ARG_SPEC_URI_V = 'SPEC_URI'
ARG_SPEC_URI_H = 'Spec URI. Can be used multiple times.'

# Hotkey spec ID
ARG_SPEC_ID_F = '-i'
ARG_SPEC_ID_K = 'ARG_SPEC_ID_K'
ARG_SPEC_ID_A = 'append'
ARG_SPEC_ID_D = []
ARG_SPEC_ID_V = 'SPEC_ID'
ARG_SPEC_ID_H = (
    'Spec ID given to a spec.'
    ' Can be used multiple times,'
    ' each time matching with one {spec_option} in order.'
    ' Spec IDs can be used by "aoikhotkey.util.cmd::SpecSwitch"'
    ' to identify the spec to swicth to.'
).format(spec_option=ARG_SPEC_URI_F)

# Hotkey spec parse function URI
ARG_SPEC_PARSE_URI_F = '-P'
ARG_SPEC_PARSE_URI_K = 'ARG_SPEC_PARSE_URI_K'
ARG_SPEC_PARSE_URI_D = 'aoikhotkey.hotkey_spec_parser::spec_parse'
ARG_SPEC_PARSE_URI_V = 'SPEC_PARSE'
ARG_SPEC_PARSE_URI_H = (
    'Spec parse function URI.'
    ' Default is "{default}".'
).format(default=ARG_SPEC_PARSE_URI_D)

# Hotkey parse function URI
ARG_HOTKEY_PARSE_URI_F = '-p'
ARG_HOTKEY_PARSE_URI_K = 'ARG_HOTKEY_PARSE_URI_K'
ARG_HOTKEY_PARSE_URI_D = 'aoikhotkey.hotkey_parser::hotkey_parse'
ARG_HOTKEY_PARSE_URI_V = 'HOTKEY_PARSE'
ARG_HOTKEY_PARSE_URI_H = (
    'Hotkey parse function URI.'
    ' Default is "{default}".'
).format(default=ARG_HOTKEY_PARSE_URI_D)

# Hotkey trigger function URI
ARG_HOTKEY_TFUNC_URI_F = '-t'
ARG_HOTKEY_TFUNC_URI_K = 'ARG_HOTKEY_TFUNC_URI_K'
ARG_HOTKEY_TFUNC_URI_D = 'aoikhotkey.util.tfunc::hotkey_tfunc'
ARG_HOTKEY_TFUNC_URI_V = 'HOTKEY_TFUNC'
ARG_HOTKEY_TFUNC_URI_H = (
    'Hotkey trigger function URI.'
    ' Default is "{default}".'
).format(default=ARG_HOTKEY_TFUNC_URI_D)

# Virtual key code-to-name function URI
ARG_VK_CTN_URI_F = '-n'
ARG_VK_CTN_URI_K = 'ARG_VK_CTN_URI_K'
ARG_VK_CTN_URI_D = 'aoikhotkey.hotkey_parser::vk_ctn'
ARG_VK_CTN_URI_V = 'VK_CTN'
ARG_VK_CTN_URI_H = (
    'Virtual key code-to-name function URI.'
    ' Used for printing user-friendly name for a virtual key.'
    ' Default is "{default}".'
).format(default=ARG_VK_CTN_URI_D)

# Debug mode
ARG_DBG_MSG_F = '-v'
ARG_DBG_MSG_K = 'ARG_DBG_MSG_K'
ARG_DBG_MSG_D = True
ARG_DBG_MSG_V = '1|0'
ARG_DBG_MSG_H = """Debug messages on/off. Default is {}."""\
    .format('on' if ARG_DBG_MSG_D else 'off')


# Show version
ARG_VER_ON_F = '--version'
ARG_VER_ON_K = 'ARG_VER_ON_K'
ARG_VER_ON_A = 'store_true'
ARG_VER_ON_H = 'Show version.'


def create_arguments_parser():
    """
    Create arguments parser.

    :return: Arguments parser.
    """
    # Create arguments parser
    parser = ArgumentParser(add_help=True)

    # Add arguments
    parser.add_argument(
        ARG_SPEC_URI_F,
        dest=ARG_SPEC_URI_K,
        action=ARG_SPEC_URI_A,
        default=ARG_SPEC_URI_D,
        metavar=ARG_SPEC_URI_V,
        help=ARG_SPEC_URI_H,
    )

    parser.add_argument(
        ARG_SPEC_ID_F,
        dest=ARG_SPEC_ID_K,
        action=ARG_SPEC_ID_A,
        default=ARG_SPEC_ID_D,
        metavar=ARG_SPEC_ID_V,
        help=ARG_SPEC_ID_H,
    )

    parser.add_argument(
        ARG_SPEC_PARSE_URI_F,
        dest=ARG_SPEC_PARSE_URI_K,
        default=ARG_SPEC_PARSE_URI_D,
        metavar=ARG_SPEC_PARSE_URI_V,
        help=ARG_SPEC_PARSE_URI_H,
    )

    parser.add_argument(
        ARG_HOTKEY_PARSE_URI_F,
        dest=ARG_HOTKEY_PARSE_URI_K,
        default=ARG_HOTKEY_PARSE_URI_D,
        metavar=ARG_HOTKEY_PARSE_URI_V,
        help=ARG_HOTKEY_PARSE_URI_H,
    )

    parser.add_argument(
        ARG_HOTKEY_TFUNC_URI_F,
        dest=ARG_HOTKEY_TFUNC_URI_K,
        default=ARG_HOTKEY_TFUNC_URI_D,
        metavar=ARG_HOTKEY_TFUNC_URI_V,
        help=ARG_HOTKEY_TFUNC_URI_H,
    )

    parser.add_argument(
        ARG_VK_CTN_URI_F,
        dest=ARG_VK_CTN_URI_K,
        default=ARG_VK_CTN_URI_D,
        metavar=ARG_VK_CTN_URI_V,
        help=ARG_VK_CTN_URI_H,
    )

    parser.add_argument(
        ARG_DBG_MSG_F,
        dest=ARG_DBG_MSG_K,
        nargs='?',
        const=True,
        default=ARG_DBG_MSG_D,
        metavar=ARG_DBG_MSG_V,
        help=ARG_DBG_MSG_H,
    )

    parser.add_argument(
        ARG_VER_ON_F,
        dest=ARG_VER_ON_K,
        action=ARG_VER_ON_A,
        help=ARG_VER_ON_H,
    )

    # Return the arguments parser
    return parser
