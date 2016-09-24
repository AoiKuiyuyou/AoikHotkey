# coding: utf-8
"""
This module contains keyboard-related hotkey functions for Windows platform.
"""
from __future__ import absolute_import

# Internal imports
from aoikhotkey.const import EMASK_V_EFUNC
from aoikhotkey.const import HOTKEY_INFO_K_HOTKEY_TUPLES
from aoikhotkey.hotkey_spec_parser import NeedHotkeyInfo
from aoikhotkey.runtime import hotkey_manager_get
from aoikhotkey.virtualkey import MAP_CHAR_TO_WIN_VK
from aoikhotkey.virtualkey import MAP_SHIFTED_CHAR_TO_WIN_VK
from aoikhotkey.virtualkey import VK_BACK
from aoikhotkey.virtualkey import VK_LSHIFT

# Local imports
from .sendkey_winos import keys_stroke


class SendKeys(object):
    """
    Hotkey function class that sends keys.
    """

    #
    def __init__(
        self, pattern, parse=True, emask=None, keys_stroke_kwargs=None
    ):
        """
        Constructor.

        :param pattern: Hotkey pattern.

        :param parse: Whether parse given hotkey pattern.

        :param emask: Event mask.

        :param keys_stroke_kwargs: Keyword arguments to be passed to \
            `keys_stroke` function.

        :return: None.
        """
        # If need parse given hotkey pattern
        if parse:
            # Parse given hotkey pattern to virtual key list
            self._vks = self._parse_hotkey(pattern)
        else:
            # Use given pattern as virtual key list
            self._vks = pattern

        # Store keyword arguments to be passed to `keys_stroke` function
        self._keys_stroke_kwargs = keys_stroke_kwargs or {}

        # Store event mask
        self._emask = EMASK_V_EFUNC if emask is None else emask

    def _parse_hotkey(self, pattern):
        """
        Parse hotkey pattern to virtual key list.

        :param pattern: Hotkey pattern.

        :return: Virtual key list.
        """
        # Parse given hotkey pattern to virtual key lists
        hotkey_s = hotkey_manager_get().hotkey_parse(pattern)

        # Use the first virtual key list
        hotkey = hotkey_s[0]

        # Return the first virtual key list
        return hotkey

    def __call__(self):
        """
        Hotkey function that sends keys.
        """
        # Get hotkey manager
        hotkey_manager = hotkey_manager_get()

        # Run in event mask context
        with hotkey_manager.emask_ctx(self._emask):
            # Get virtual keys that are currently pressed
            vks_pressed = hotkey_manager.vk_down_list()

            # Send keys
            keys_stroke(
                vks=self._vks,
                vks_pressed=vks_pressed,
                **self._keys_stroke_kwargs
            )


class SendSubs(NeedHotkeyInfo):
    """
    Hotkey function class that sends substitution text.

    Must be called in main thread.
    """

    #
    def __init__(self, keys, back_count=None, sendkeys_kwargs=None):
        """
        Constructor.

        :param keys: Substitution text to send.

        :param back_count: Number of backspaces to send to delete previously \
            entered text. If not given, will be automatically computed.

        :param sendkeys_kwargs: Keyword arguments to be passed to `SendKeys` \
            class constructor.

        :return: None.
        """
        # Call super class constructor
        super(NeedHotkeyInfo, self).__init__()

        # Store keyword arguments to be passed to `SendKeys` class constructor
        self._sendkeys_kwargs = sendkeys_kwargs or {}

        # Store the number of backspaces to send.
        # Specified by user or initialized in method `hotkey_info_set`
        self._back_count = back_count

        # Virtual key list
        self._vks = []

        # For given substitution text's each character
        for key in keys:
            # Map the character to virtual key
            vk = MAP_CHAR_TO_WIN_VK.get(key, None)

            # If virtual key is found
            if vk is not None:
                # Add the virtual key to the virtual key list
                self._vks.append(vk)

            # If virtual key is not found
            else:
                # Map the (assumed) shifted character to virtual key
                vk = MAP_SHIFTED_CHAR_TO_WIN_VK.get(key, None)

                # Assert virtual key is found
                assert vk is not None

                # Add LSHIFT to the virtual key list
                self._vks.append(VK_LSHIFT)

                # Add the virtual key found to the virtual key list
                self._vks.append(vk)

    def __call__(self):
        """
        Hotkey function that sends substitution text.
        """
        # Prepend backspace virtual keys to the virtual key list
        vks = [VK_BACK] * self._back_count + self._vks

        # Send keys
        SendKeys(vks, parse=False, **self._sendkeys_kwargs)()

    def hotkey_info_set(self, hotkey_info):
        """
        Set hotkey info. Will be called by hotkey manager.

        :param hotkey_info: Hotkey info.

        :return: None.
        """
        # If backspace count is given by user
        if self._back_count is not None:
            # Do not compute automatically
            return

        # If backspace count is not given by user.

        # Get the hotkey's virtual key tuples
        hotkey_tuple_s = hotkey_info[HOTKEY_INFO_K_HOTKEY_TUPLES]

        # Use the first virtual key tuple
        hotkey_tuple = hotkey_tuple_s[0]

        # Use the hotkey's number of virtual keys to decide the number of
        # backspaces to send. This assumes all virtual keys are printable keys.
        # `-1` is because the event of last key that triggers this hotkey is
        # not propagated so no need to send a backspace to delete it.
        self._back_count = len(hotkey_tuple) - 1
