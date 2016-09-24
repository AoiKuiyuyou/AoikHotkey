# coding: utf-8
"""
This module contains hotkey trigger function that prints info to console.
"""
from __future__ import absolute_import

# Standard imports
import sys

# Internal imports
from aoikhotkey.const import HOTKEY_INFO_K_HOTKEY_ORIG_SPEC
from aoikhotkey.const import HOTKEY_TYPE_V_DN
from aoikhotkey.const import HOTKEY_TYPE_V_KS
from aoikhotkey.const import HOTKEY_TYPE_V_UP


def hotkey_tfunc(hotkey_manager, hotkey, hotkey_type, hotkey_info, event):
    """
    Hotkey trigger function that prints info to console.

    :param hotkey_manager: Hotkey manager.

    :param hotkey: Hotkey's virtual key list.

    :param hotkey_type: Hotkey type.

    :param hotkey_info: Hotkey info.

    :param event: Event object.

    :return: None.
    """
    # If hotkey type is key-down
    if hotkey_type == HOTKEY_TYPE_V_DN:
        # Get text
        up_dn_text = ' down '

    # If hotkey type is key-up
    elif hotkey_type == HOTKEY_TYPE_V_UP:
        # Get text
        up_dn_text = ' up '

    # If hotkey type is not key-down or key-up
    else:
        # Get text
        up_dn_text = ' '

    # Get original hotkey spec
    orig_spec = hotkey_info[HOTKEY_INFO_K_HOTKEY_ORIG_SPEC]

    # Get hotkey pattern
    hotkey_pattern = orig_spec[0]

    # Get message
    msg = (
        '# {hotkey_type}{up_dn_text}triggered\n{hotkey_pattern}\n'
        '{hotkey_vk_names}\n\n'
    ).format(
        hotkey_type='Hotseq' if hotkey_type == HOTKEY_TYPE_V_KS else 'Hotkey',
        up_dn_text=up_dn_text,
        hotkey_pattern=hotkey_pattern,
        hotkey_vk_names=' '.join(
            hotkey_manager.vk_to_name(vk) or str(vk) for vk in hotkey
        ),
    )

    # Print message
    sys.stderr.write(msg)
