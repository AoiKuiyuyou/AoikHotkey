# coding: utf-8
"""
This module contains runtime states.
"""
from __future__ import absolute_import


# This variable is set by mediator module at 2STYZ
_HOTKEY_MANAGER = None


def hotkey_manager_set(hotkey_manager):
    """
    Set hotkey manager.

    :param hotkey_manager: Hotkey manager.

    :return: None.
    """
    # Use global variable
    global _HOTKEY_MANAGER

    # Set hotkey manager
    _HOTKEY_MANAGER = hotkey_manager


def hotkey_manager_get():
    """
    Get hotkey manager.

    :return: Hotkey manager.
    """
    # Return hotkey manager
    return _HOTKEY_MANAGER
