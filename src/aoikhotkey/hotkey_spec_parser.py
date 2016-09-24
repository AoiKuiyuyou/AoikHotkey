# coding: utf-8
"""
This module contains hotkey spec parse function.
"""
from __future__ import absolute_import

# Standard imports
import os.path
from subprocess import Popen
import webbrowser

# Local imports
from .const import HOTKEY_INFO_K_HOTKEY_FUNC
from .const import HOTKEY_INFO_K_HOTKEY_ORIG_SPEC
from .const import HOTKEY_INFO_K_HOTKEY_PATTERN
from .const import HOTKEY_INFO_K_HOTKEY_TYPE
from .const import HOTKEY_INFO_K_NEED_HOTKEY_INFO_LIST
from .const import HOTKEY_TYPE_V_DN
from .const import HOTKEY_TYPE_V_KS
from .const import HOTKEY_TYPE_V_UP


class _CallAll(object):
    """
    Call all given functions.
    """

    def __init__(self, funcs):
        """
        Constructor.

        :param funcs: Function list.

        :return: None.
        """
        # Store given function list
        self._funcs = funcs

    def __call__(self):
        """
        Call all given functions.

        :return: False if any called function returns False, or the last \
            called function's result.
        """
        # Result
        res = None

        # For the function list's each function
        for func in self._funcs:
            # Call the function
            res = func()

            # If the call result is False
            if res is False:
                # Return False
                return False

        # Return the last called function's result
        return res


class NeedHotkeyInfo(object):
    """
    Mixin class for marking a hotkey function class as `need hotkey info`.
    """

    def hotkey_info_set(self, hotkey_info):
        """
        Set hotkey info. Will be called by hotkey manager.

        :param hotkey_info: Hotkey info.

        :return: None.
        """
        # Raise error
        raise NotImplementedError()


# `call in main thread` tag's attribute name
_TAG_CALL_IN_MAIN_THREAD = '_AOIKHOTKEY_TAG_CALL_IN_MAIN_THREAD'


def tag_call_in_main_thread(func):
    """
    Decorator that adds `call in main thread` tag attribute to decorated \
        function.

    :param func: Decorated function.

    :return: Decorated function.
    """
    # Set tag attribute on given function
    setattr(func, _TAG_CALL_IN_MAIN_THREAD, True)

    # Return given function
    return func


def tag_call_in_main_thread_exists(func):
    """
    Test whether given function has `call in main thread` tag.
    """
    # Return tag attribute's value
    return getattr(func, _TAG_CALL_IN_MAIN_THREAD, False)


# `call with info` tag's attribute name
_TAG_CALL_WITH_INFO = '_AOIKHOTKEY_TAG_CALL_WITH_INFO'


def tag_call_with_info(func):
    """
    Decorator that adds `call with info` tag attribute to decorated function.

    :param func: Decorated function.

    :return: Decorated function.
    """
    # Set tag attribute on given function
    setattr(func, _TAG_CALL_WITH_INFO, True)

    # Return given function
    return func


def tag_call_with_info_exists(func):
    """
    Test whether given function has `call with info` tag.
    """
    # Return tag attribute's value
    return getattr(func, _TAG_CALL_WITH_INFO, False)


def spec_parse(specs):
    """
    Parse hotkey spec list into hotkey info list.

    :param specs: Hotkey spec list.

    :return: Hotkey info list.
    """
    # `Call in main thread` option
    _OPT_CALL_IN_MAIN_THREAD = '_OPT_CALL_IN_MAIN_THREAD'

    # `Key-up hotkey` option
    _OPT_KEY_UP_HOTKEY = '_OPT_KEY_UP_HOTKEY'

    # Hotkey info list
    hotkey_info_s = []

    # For given hotkey spec list's each hotkey spec
    for spec in specs:
        # Get hotkey pattern
        hotkey_pattern = spec[0]

        # Get hotkey function list
        func_list = spec[1:]

        # Whether the hotkey type is key-sequence
        is_hotseq = False

        # Option list
        opt_s = []

        # If the hotkey pattern is None,
        # it means to add event function, not hotkey function.
        # This aims to co-work with code at 4QTR9.
        if hotkey_pattern is None:
            # Use the hotkey pattern as-is
            pass

        # If the hotkey pattern is list,
        # it is assumed to be a list of virtual keys.
        # This aims to co-work with code at 4JPY2.
        elif isinstance(hotkey_pattern, list):
            # Use the hotkey pattern as-is
            pass

        # If the hotkey pattern is string
        elif isinstance(hotkey_pattern, str):
            # If the hotkey pattern starts with `$`
            if hotkey_pattern.startswith('$'):
                # Add `call in main thread` option
                opt_s.append(_OPT_CALL_IN_MAIN_THREAD)

                # Remove the special character
                hotkey_pattern = hotkey_pattern[1:]

            # If the hotkey pattern starts with `~`
            if hotkey_pattern.startswith('~'):
                # Add `key-up hotkey` option
                opt_s.append(_OPT_KEY_UP_HOTKEY)

                # Remove the special character
                hotkey_pattern = hotkey_pattern[1:]

            # If the hotkey pattern starts with `::`,
            # it means key-sequence hotkey.
            if hotkey_pattern.startswith('::'):
                # If the key sequence is empty
                if hotkey_pattern in ('::', ':::', '::::'):
                    # Get error message
                    msg = 'Hot sequence can not be empty: {}.'.format(
                        repr(hotkey_pattern)
                    )

                    # Raise error
                    raise ValueError(msg)

                # If the key sequence is not empty.

                # Set is key-sequence be True
                is_hotseq = True

                # If the key sequence ends with `::`
                if hotkey_pattern.endswith('::'):
                    # Remove starting and ending `::`.
                    # This aims to be compatible with AutoHotkey.
                    hotkey_pattern = hotkey_pattern[2:-2]

                # If the key sequence not ends with `::`
                else:
                    # Remove starting `::`
                    hotkey_pattern = hotkey_pattern[2:]

                # Assert the key sequence is not empty
                assert hotkey_pattern

        # If the hotkey pattern is none of above
        else:
            # Raise error
            assert 0, hotkey_pattern

        # Normalized function list
        norm_func_s = []

        # NeedHotkeyInfo instance list
        need_info_instance_s = []

        # For the hotkey function list's each function item
        for func_item in func_list:
            # If the function item is string
            if isinstance(func_item, str):
                # If the string starts with `http://` or `https://`
                if func_item.startswith('http://') \
                        or func_item.startswith('https://'):
                    # Use the string as URL
                    url = func_item

                    # Create a function that opens the URL.
                    # `webbrowser.open` returns True so can not use `partial`.
                    def new_func(url=url):
                        # Open given URL
                        webbrowser.open(url)

                    # Use the created function as function item
                    func_item = new_func

                # If the string is existing directory path
                elif os.path.isdir(func_item):
                    # Prefix the string with `file://` protocol
                    url = 'file://' + func_item

                    # Create a function that opens the URL.
                    # `webbrowser.open` returns True so can not use `partial`.
                    def new_func(url=url):
                        # Open given URL
                        webbrowser.open(url)

                    # Use the created function as function item
                    func_item = new_func

                # If the string is none of above,
                # assume it is a command.
                else:
                    # Create a function that runs the command
                    def new_func(cmd=func_item):
                        # Split the command into parts
                        cmd_part_s = cmd.split()

                        # Run the command
                        Popen(cmd_part_s, shell=True)

                    # Use the created function as function item
                    func_item = new_func

            # If the function item is `NeedHotkeyInfo` instance
            elif isinstance(func_item, NeedHotkeyInfo):
                # Add the function item to the instance list
                need_info_instance_s.append(func_item)

            # If the function item is none of above
            else:
                # Use the function item as-is
                func_item = func_item

            # Add the function item to the normalized function list
            norm_func_s.append(func_item)

        # If the normalized function list contains only one item
        if len(norm_func_s) == 1:
            # Use the only item as hotkey function
            hotkey_func = norm_func_s[0]

        # If the normalized function list not contains only one item
        else:
            # Combine all functions into one
            hotkey_func = _CallAll(norm_func_s)

        # If `call in main thread` option is enabled
        if _OPT_CALL_IN_MAIN_THREAD in opt_s:
            # Tag the function as `call in main thread`
            hotkey_func = tag_call_in_main_thread(hotkey_func)

        # Whether is key-up hotkey
        is_key_up = _OPT_KEY_UP_HOTKEY in opt_s

        # If is key-sequence hotkey
        if is_hotseq:
            # If is key-up hotkey
            if is_key_up:
                # Get error message
                msg = 'Hot sequence can not be key-up hotkey.'

                # Raise error
                raise ValueError(msg)

            # If is not key-up hotkey

            # Set hotkey type be key-sequence
            hotkey_type = HOTKEY_TYPE_V_KS

        # If is key-up hotkey
        elif is_key_up:
            # Set hotkey type be key-up
            hotkey_type = HOTKEY_TYPE_V_UP

        # If is not key-up hotkey
        else:
            # Set hotkey type be key-down
            hotkey_type = HOTKEY_TYPE_V_DN

        # Get hotkey info
        hotkey_info = {
            HOTKEY_INFO_K_HOTKEY_TYPE: hotkey_type,
            HOTKEY_INFO_K_HOTKEY_PATTERN: hotkey_pattern,
            HOTKEY_INFO_K_HOTKEY_FUNC: hotkey_func,
            HOTKEY_INFO_K_HOTKEY_ORIG_SPEC: spec,
            HOTKEY_INFO_K_NEED_HOTKEY_INFO_LIST: need_info_instance_s,
        }

        # Add the hotkey info to the hotkey info list
        hotkey_info_s.append(hotkey_info)

    # Return the hotkey info list
    return hotkey_info_s
