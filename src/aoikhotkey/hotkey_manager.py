# coding: utf-8
"""
This module contains hotkey manager.
"""
from __future__ import absolute_import

# Standard imports
from collections import OrderedDict
from collections import deque
from contextlib import contextmanager
from functools import partial
import sys
import time
from traceback import format_exc

# Local imports
from .compat import IS_LINUX
from .const import EMASK_V_ALL
from .const import EMASK_V_EFUNC
from .const import EMASK_V_HOTKEY
from .const import EMASK_V_HOTSEQ
from .const import HOTKEY_INFO_K_HOTKEY_FUNC
from .const import HOTKEY_INFO_K_HOTKEY_ORIG_SPEC
from .const import HOTKEY_INFO_K_HOTKEY_PATTERN
from .const import HOTKEY_INFO_K_HOTKEY_TUPLES
from .const import HOTKEY_INFO_K_HOTKEY_TYPE
from .const import HOTKEY_INFO_K_NEED_HOTKEY_INFO_LIST
from .const import HOTKEY_TYPE_V_DN
from .const import HOTKEY_TYPE_V_KS
from .const import HOTKEY_TYPE_V_UP
from .const import HOTKEY_TYPES
from .event_manager import EventManager
from .hotkey_spec_parser import tag_call_in_main_thread_exists
from .hotkey_spec_parser import tag_call_with_info_exists
from .task_manager import add_task
from .virtualkey import EVK_MOUSE_WHEEL_DOWN
from .virtualkey import EVK_MOUSE_WHEEL_UP
from .virtualkey import MAP_MOUSE_UP_VK_TO_DN_VK
from .virtualkey import MAP_X11_NAME_TO_WIN_VK
from .virtualkey import VK_MOUSE_WHEEL


class HotkeyManager(object):
    """
    Hotkey manager.
    """

    #
    def __init__(
        self,
        hotkey_parse,
        hotkey_tfunc,
        vk_ctn,
    ):
        """
        Constructor.

        :param hotkey_parse: Hotkey parse function.

        :param hotkey_tfunc: Hotkey trigger function.

        :vk_ctn: Virtual key code-to-name function.

        :return: None.
        """
        # Hotkey parse function
        self._hotkey_parse = hotkey_parse

        # Hotkey trigger function
        self._hotkey_tfunc = hotkey_tfunc

        # Virtual key code-to-name function
        self._vk_ctn = vk_ctn

        # Virtual keys that have been pressed down
        self._vk_s_dn = []

        # Virtual keys that have been pressed down in sequence
        self._vk_s_dn_queue = deque()

        # Event mask
        self._emask = EMASK_V_ALL

        # Event loop stop callback
        self._eloop_stop_callback = None

        # Event function list
        self._efunc_s = []

        # Map virtual key tuple to key-down hotkey info
        self._hotkey_info_by_vk_map_for_key_down = OrderedDict()

        # Map virtual key tuple to key-up hotkey info
        self._hotkey_info_by_vk_map_for_key_up = OrderedDict()

        # Map virtual key tuple to key-sequence hotkey info
        self._hotkey_info_by_vk_map_for_key_seq = OrderedDict()

        # Map hotkey ID to hotkey info
        self._hotkey_info_by_id_map = {}

        # Create event manager
        self._event_manager = EventManager()

        # Get bound method
        key_dn_hdlr = self._key_dn_hdlr

        # Get bound method
        key_up_hdlr = self._key_up_hdlr

        # Get bound method
        mouse_wm_func = partial(key_dn_hdlr, mouse_wm=True)

        # Add event handlers to the event manager
        self._event_manager.add_handler('KeyDown', key_dn_hdlr)

        self._event_manager.add_handler('KeyUp', key_up_hdlr)

        self._event_manager.add_handler('MouseDown', key_dn_hdlr)

        self._event_manager.add_handler('MouseUp', key_up_hdlr)

        self._event_manager.add_handler('MouseMove', mouse_wm_func)

        self._event_manager.add_handler('MouseWheel', mouse_wm_func)

    def efunc_add(self, func):
        """
        Add event function.

        :param func: Event function.

        :return: None.
        """
        # Add given event function to event function list
        self._efunc_s.append(func)

    def efunc_remove(self, func):
        """
        Remove event function.

        :param func: Event function.

        :return: None.
        """
        # Remove given event function from event function list
        self._efunc_s.remove(func)

    def _efunc_call_all(self, event, propagate=None):
        """
        Call all event functions.

        :param event: Event object.

        :param propagate: Whether propagate the event.

        :return: Whether propagate the event.
        """
        # If the event function list is not empty
        if self._efunc_s:
            # For the event function list's each event function
            for efunc in self._efunc_s:
                try:
                    # Call the event function.
                    # Use the call result to decide whether propagate the
                    # event.
                    propagate = efunc(event)

                    # If the propagate value is False,
                    # it means discard the event.
                    if propagate is False:
                        # Stop calling remaining event functions
                        break

                # If have error
                except Exception:
                    # Get traceback message
                    tb_msg = format_exc()

                    # Get error message
                    msg = (
                        '# Error when calling event function:\n---\n{0}---\n'
                    ).format(tb_msg)

                    # Print error message
                    sys.stderr.write(msg)

        # Return whether propagate the event
        return propagate

    def eloop_start(self):
        """
        Start event loop.

        This method will not return until the event loop is stopped by \
        calling :paramref:`eloop_stop`.

        :return: None.
        """
        # Set event loop stop callback be None before starting event loop
        self._eloop_stop_callback = None

        try:
            # Start event loop.
            # This method will not return until the event loop is stopped.
            self._event_manager.start_event_loop()
        finally:
            # Remove event handlers
            self._event_manager.remove_handlers()

        # Get event loop stop callback
        eloop_stop_callback = self._eloop_stop_callback

        # Set event loop stop callback be None
        self._eloop_stop_callback = None

        # If the event loop stop callback is not None
        if eloop_stop_callback is not None:
            # Call the event loop stop callback
            eloop_stop_callback()

    def eloop_stop(self):
        """
        Stop event loop.

        :return: None.
        """
        # Remove event handlers
        self._event_manager.remove_handlers()

        # Stop event loop
        self._event_manager.stop_event_loop()

    def eloop_stop_callback_set(self, callback):
        """
        Set event loop stop callback.

        :param callback: Event loop stop callback.

        :return: None.
        """
        # Set event loop stop callback
        self._eloop_stop_callback = callback

    def emask_get(self):
        """
        Get event mask.

        :return: Event mask.
        """
        # Return event mask
        return self._emask

    def emask_set(self, mask):
        """
        Set event mask.

        :param mask: Event mask.

        :return: None.
        """
        # If given event mask is not valid
        if (mask | EMASK_V_ALL) != EMASK_V_ALL:
            # Get error message
            msg = 'Invalid event mask: {0}'.format(repr(mask))

            # Raise error
            raise ValueError(msg)

        # If given event mask is valid.

        # Store given event mask
        self._emask = mask

    def emask_ctx(self, emask):
        """
        Create event mask context manager.

        :param mask: Event mask.

        :return: Event mask context manager.
        """
        # Create context manager factory
        @contextmanager
        def ctx_factory():
            # Store old mask
            old_mask = self._emask

            # Set new mask
            self._emask = emask

            # This is before entering the context
            yield
            # This is after exiting the context

            # Restore old mask
            self._emask = old_mask

        # Return event mask context manager
        return ctx_factory()

    def hotkey_parse(self, pattern):
        """
        Parse hotkey pattern to virtual key lists.

        :param pattern: Hotkey pattern.

        :return: Virtual key lists.
        """
        # Parse hotkey pattern to virtual key lists
        return self._hotkey_parse(pattern)

    def hotkey_add(self, hotkey_info):
        """
        Add hotkey.

        :param hotkey_info: Hotkey info.

        :return: Hotkey ID.
        """
        # Ensure given hotkey info is valid
        assert HOTKEY_INFO_K_HOTKEY_TYPE in hotkey_info

        assert HOTKEY_INFO_K_HOTKEY_PATTERN in hotkey_info

        assert HOTKEY_INFO_K_HOTKEY_FUNC in hotkey_info

        assert HOTKEY_INFO_K_HOTKEY_ORIG_SPEC in hotkey_info

        assert HOTKEY_INFO_K_NEED_HOTKEY_INFO_LIST in hotkey_info

        # Get hotkey type
        hotkey_type = hotkey_info[HOTKEY_INFO_K_HOTKEY_TYPE]

        # Ensure the hotkey type is valid
        assert hotkey_type in HOTKEY_TYPES

        # Get hotkey pattern
        pattern = hotkey_info[HOTKEY_INFO_K_HOTKEY_PATTERN]

        # 4QTR9
        # If hotkey pattern is not specified,
        # it means add event function instead of hotkey function.
        if not pattern:
            # Get event function
            event_func = hotkey_info[HOTKEY_INFO_K_HOTKEY_FUNC]

            # Add event function
            self.efunc_add(event_func)

            # Return
            return

        # If given hotkey pattern is not string or virtual key list
        if not isinstance(pattern, (str, list)):
            # Get error message
            msg = 'Expected string or a list of virtual keys. Got: {0}.'\
                .format(repr(pattern))

            # Raise error
            raise TypeError(msg)

        # If given hotkey pattern is string or virtual key list.

        # If given hotkey pattern is string
        if isinstance(pattern, str):
            # Parse given hotkey pattern to hotkey list.
            # Each hotkey is a virtual key list.
            hotkey_s = self._hotkey_parse(pattern)

        # 4JPY2
        # If given hotkey pattern is list
        elif isinstance(pattern, list):
            # If given list is empty
            if not pattern:
                # Set hotkey list be empty
                hotkey_s = []
            else:
                # If given list's first item is list
                if isinstance(pattern[0], list):
                    # Use given list as hotkey list
                    hotkey_s = pattern

                # If given list's first item is not list
                else:
                    # Use given list as single hotkey
                    hotkey_s = [pattern]

        # If given hotkey pattern is not string or list
        else:
            # Raise error
            assert 0, pattern

        # Print parsed hotkeys
        print('Hotkey: {0} -> VK: {1}'.format(pattern, hotkey_s))

        # Convert virtual key lists to virtual key tuples
        hotkey_tuple_s = [
            self._hotkey_to_tuple(x, hotkey_type=hotkey_type)
            for x in hotkey_s
        ]

        # Get hotkey info map.
        # Key is virtual key tuple.
        hotkey_info_by_vk_map = self._hotkey_info_by_vk_map_get(hotkey_type)

        # Store virtual key tuples in the hotkey info
        hotkey_info[HOTKEY_INFO_K_HOTKEY_TUPLES] = hotkey_tuple_s

        # For each virtual key tuple
        for hotkey_tuple in hotkey_tuple_s:
            # If the virtual key tuple exists in the hotkey info map,
            # it means the hotkey has been occupied.
            if hotkey_tuple in hotkey_info_by_vk_map:
                # If is key-down event
                if hotkey_type == HOTKEY_TYPE_V_DN:
                    # Get up or down text
                    up_dn_txt = ' down '
                # If is key-up event
                elif hotkey_type == HOTKEY_TYPE_V_UP:
                    # Get up or down text
                    up_dn_txt = ' up '
                # If is not key-down or key-up event
                else:
                    # Get up or down text
                    up_dn_txt = ' '

                # Get error message
                msg = (
                    '{hotkey_type}{up_dn}is occupied: Hotkey: {hotkey} -> VK:'
                    ' {hotkey_tuple}'
                ).format(
                    hotkey_type='Hotseq'
                    if hotkey_type == HOTKEY_TYPE_V_KS else 'Hotkey',
                    up_dn=up_dn_txt,
                    hotkey=repr(pattern),
                    hotkey_tuple=repr(hotkey_tuple),
                )

                # Raise error
                raise ValueError(msg)

            # If the virtual key tuple not exists in the hotkey info map
            else:
                # Add the hotkey info to the map
                hotkey_info_by_vk_map[hotkey_tuple] = hotkey_info

        # Create hotkey ID
        hotkey_id = self._hotkey_id_factory()

        # Add the hotkey info to the map
        self._hotkey_info_by_id_map[hotkey_id] = hotkey_info

        # For each NeedHotkeyInfo instance
        for item in hotkey_info[HOTKEY_INFO_K_NEED_HOTKEY_INFO_LIST]:
            # Set the instance's hotkey info
            item.hotkey_info_set(hotkey_info)

        # Return the hotkey ID
        return hotkey_id

    def hotkey_remove(self, hotkey_id):
        """
        Remove hotkey.

        :param hotkey_id: Hotkey ID that was returned by \
            :paramref:`hotkey_add`.

        :return: Hotkey info, or None if not found.
        """
        # If given hotkey ID is not int
        if not isinstance(hotkey_id, int):
            # Get error message
            msg = 'Expected int. Got: {0}.'.format(repr(hotkey_id))

            # Raise error
            raise TypeError(msg)

        # If given hotkey ID is int.

        # Pop hotkey info from the hotkey info map
        hotkey_info = self._hotkey_info_by_id_map.pop(hotkey_id, None)

        # If hotkey info is not found
        if hotkey_info is None:
            # Return None
            return None

        # If hotkey info is found
        else:
            # Get hotkey type
            hotkey_type = hotkey_info[HOTKEY_INFO_K_HOTKEY_TYPE]

            # Get hotkey's virtual key tuples
            hotkey_tuple_s = hotkey_info[HOTKEY_INFO_K_HOTKEY_TUPLES]

            # Get hotkey info map
            hotkey_info_by_vk_map = self._hotkey_info_by_vk_map_get(
                hotkey_type
            )

            # For the hotkey's each virtual key tuple
            for hotkey_tuple in hotkey_tuple_s:
                # Pop the virtual key tuple from the map
                hotkey_info_by_vk_map.pop(hotkey_tuple, None)

            # Return the hotkey info
            return hotkey_info

    def _hotkey_info_by_vk_map_get(self, hotkey_type):
        """
        Get hotkey info by-VK map for given hotkey type.

        :param hotkey_type: Hotkey type.

        :return: Hotkey info by-VK map for given hotkey type.
        """
        # If is key-down hotkey
        if hotkey_type == HOTKEY_TYPE_V_DN:
            # Use key-down map
            hotkey_info_by_vk_map = self._hotkey_info_by_vk_map_for_key_down

        # If is key-up hotkey
        elif hotkey_type == HOTKEY_TYPE_V_UP:
            # Use key-up map
            hotkey_info_by_vk_map = self._hotkey_info_by_vk_map_for_key_up

        # If is key-sequence hotkey
        elif hotkey_type == HOTKEY_TYPE_V_KS:
            # Use key-sequence map
            hotkey_info_by_vk_map = self._hotkey_info_by_vk_map_for_key_seq

        # If is none of above
        else:
            # Raise error
            assert 0, hotkey_type

        # Return the map
        return hotkey_info_by_vk_map

    def _hotkey_to_tuple(self, hotkey, hotkey_type):
        """
        Convert given hotkey to virtual key tuple.

        :param hotkey: Virtual key list.

        :param hotkey_type: Hotkey type.

        :param return: Virtual key tuple.
        """
        # If given hotkey type is key-sequence
        if hotkey_type == HOTKEY_TYPE_V_KS:
            # Get virtual key tuple
            hotkey_tuple = tuple(hotkey)
        else:
            # Get sorted virtual key tuple
            hotkey_tuple = tuple(sorted(hotkey))

        # Return the virtual key tuple
        return hotkey_tuple

    def _hotkey_id_factory(self):
        """
        Create hotkey info ID.

        :return: Hotkey info ID.
        """
        # If the hotkey info is empty
        if not self._hotkey_info_by_id_map:
            # Return 1
            return 1

        # If the hotkey info is not empty
        else:
            # Return the existing max value plus 1
            return max(self._hotkey_info_by_id_map.keys()) + 1

    def _hotkey_info_get_by_hotkey(self, hotkey, hotkey_type):
        """
        Get hotkey info for given hotkey.

        :param hotkey: Virtual key list.

        :param hotkey_type: Hotkey type.

        :param return: Hotkey info.
        """
        # Get given hotkey's virtual key tuple
        hotkey_tuple = self._hotkey_to_tuple(hotkey, hotkey_type=hotkey_type)

        # Get hotkey info map
        hotkey_info_by_vk_map = self._hotkey_info_by_vk_map_get(hotkey_type)

        # Get hotkey info
        hotkey_tuple_info = hotkey_info_by_vk_map.get(hotkey_tuple, None)

        # Return the hotkey info
        return hotkey_tuple_info

    def _key_dn_hdlr(self, event, mouse_wm=False):
        """
        Key-down event handler.

        :param event: Event object.

        :param mouse_wm: Whether is handler for mouse wheel or mouse move \
            events.

        :return: Whether propagate the event.
        """
        # If given event is mouse event
        if 'mouse' in event.MessageName:
            # Get the mouse event's virtual key
            vk = event.Message

            # 4BIVS
            # If the virtual key is mouse wheel
            if vk == VK_MOUSE_WHEEL:
                # If mouse wheel is scrolling up
                if event.Wheel > 0:
                    # Use wheel-up extended virtual key
                    vk = EVK_MOUSE_WHEEL_UP

                # If mouse wheel is scrolling down
                elif event.Wheel < 0:
                    # Use wheel-down extended virtual key
                    vk = EVK_MOUSE_WHEEL_DOWN

                # If mouse wheel is not scrolling up or down
                else:
                    # Raise error
                    assert 0, event.Wheel

        # If given event is not mouse event
        else:
            # If the platform is Linux,
            # it means the event object's `Key` field contains the key name but
            # `KeyID` field not contains virtual key.
            if IS_LINUX:
                # Convert the key name to virtual key
                event.KeyID = MAP_X11_NAME_TO_WIN_VK.get(event.Key, 0)

            # Get the event's virtual key
            vk = event.KeyID

        # Remove the virtual key from the currently down list to avoid adding
        # duplicate below
        self._vk_down_remove(vk)

        # Remove outdated virtual keys from currently down list
        self._vk_down_remove_outdated()

        # Add the virtual key to the currently down list
        self._vk_down_add(vk)

        # Whether propagate the event.
        # None means use the default.
        propagate = None

        # If event function mask is enabled
        if self._emask & EMASK_V_EFUNC:
            # Call all event functions
            propagate = self._efunc_call_all(event, propagate=propagate)

        # Whether hotkey is found
        hotkey_is_found = False

        # If propagation is not stopped,
        # and hotkey function mask is enabled.
        if (propagate is not False) and (self._emask & EMASK_V_HOTKEY):
            # Find and call hotkey function
            hotkey_is_found, propagate = self._hotkey_find_and_call(
                hotkey=self.vk_down_list(),
                hotkey_type=HOTKEY_TYPE_V_DN,
                event=event,
                propagate=propagate,
            )

        # If is not mouse wheel or mouse move event handler,
        # and hotkey is not found,
        # and propagation is not stopped,
        # and key-sequence function mask is enabled.
        if (not mouse_wm) \
                and (not hotkey_is_found) \
                and (propagate is not False) \
                and (self._emask & EMASK_V_HOTSEQ):
            # Find and call key-sequence function
            hotkey_is_found, propagate = self._hotseq_find_and_call(
                vk=vk, event=event, propagate=propagate
            )

        # If is mouse wheel or mouse move event handler
        if mouse_wm:
            # Remove the mouse event's virtual key because it has no
            # corresponding up event
            self._vk_down_remove(vk)

        # Decide whether propagate the event
        propagate = (not hotkey_is_found) or (propagate is True)

        # Return whether propagate the event
        return propagate

    def _key_up_hdlr(self, event):
        """
        Key-up event handler.

        :param event: Event object.

        :return: Whether propagate the event.
        """
        # If given event is mouse event
        if 'mouse' in event.MessageName:
            # Get the mouse event's virtual key
            vk = event.Message

            # Get the up event's corresponding down event's virtual key
            vk_dn = MAP_MOUSE_UP_VK_TO_DN_VK.get(vk, None)

            # Ensure the down event's virtual key is found
            assert vk_dn is not None
        else:
            # If the platform is Linux,
            # it means the event object's `Key` field contains the key name but
            # `KeyID` field not contains virtual key.
            if IS_LINUX:
                # Convert the key name to virtual key
                event.KeyID = MAP_X11_NAME_TO_WIN_VK.get(event.Key, 0)

            # Get the event's virtual key
            vk = event.KeyID

            # Use the same virtual key as corresponding down event's virtual
            # key
            vk_dn = vk

        # Remove outdated virtual keys from currently down list
        self._vk_down_remove_outdated()

        # Remember old currently down list
        old_vk_s_dn = list(self.vk_down_list())

        # Remove corresponding down event's virtual key from currently down
        # list
        self._vk_down_remove(vk_dn)

        # Whether propagate the event.
        # None means use the default.
        propagate = None

        # If event function mask is enabled
        if self._emask & EMASK_V_EFUNC:
            # Call all event functions
            propagate = self._efunc_call_all(event, propagate=propagate)

            # If propagation is stopped
            if propagate is False:
                # Return False
                return propagate

        # Whether hotkey is found
        hotkey_is_found = False

        # If hotkey function mask is enabled
        if self._emask & EMASK_V_HOTKEY:
            # Find and call hotkey function
            hotkey_is_found, propagate = self._hotkey_find_and_call(
                hotkey=old_vk_s_dn,
                hotkey_type=HOTKEY_TYPE_V_UP,
                event=event,
                propagate=propagate,
            )

        # Decide whether propagate the event
        propagate = (not hotkey_is_found) or (propagate is True)

        # Return whether propagate the event
        return propagate

    def _hotkey_find_and_call(
        self, hotkey, hotkey_type, event, propagate=None
    ):
        """
        Find hotkey and call hotkey function.

        :param hotkey: Hotkey's virtual key list.

        :param hotkey_type: Hotkey type.

        :param event: Event object.

        :param propagate: Whether propagate the event.

        :return: A two-item tuple.

        Tuple format is:
        (
            Item 0,     # Whether hotkey is found.
            Item 1:     # Whether propagate the event.
        )
        """
        # Find hotkey info
        hotkey_info = self._hotkey_info_get_by_hotkey(
            hotkey=hotkey, hotkey_type=hotkey_type
        )

        # If hotkey info is not found
        if hotkey_info is None:
            # Return result
            return (False, propagate)

        # If hotkey info is found.

        # Call the hotkey function.
        # Use the call result to decide whether propagate the event.
        propagate = self._hotkey_call(
            hotkey=hotkey,
            hotkey_type=hotkey_type,
            hotkey_info=hotkey_info,
            event=event,
            propagate=propagate,
        )

        # Return result
        return (True, propagate)

    def _hotkey_call(
        self, hotkey, hotkey_type, hotkey_info, event, propagate=None
    ):
        """
        Call hotkey function, catching errors.

        :param hotkey: Hotkey's virtual key list.

        :param hotkey_type: Hotkey type.

        :param hotkey_info: Hotkey info.

        :param event: Event object.

        :param propagate: Whether propagate the event.

        :return: Whether propagate the event.
        """
        # If have hotkey trigger function
        if self._hotkey_tfunc is not None:
            try:
                # Call the hotkey trigger function
                self._hotkey_tfunc(
                    self, hotkey, hotkey_type, hotkey_info, event
                )

            # If have error
            except Exception:
                # Get traceback message
                tb_msg = format_exc()

                # Get error message
                msg = (
                    '# Error when calling trigger function\n'
                    '---\n{}---\n'
                ).format(tb_msg)

                # Print error message
                sys.stderr.write(msg)

        # Get hotkey function
        func = hotkey_info[HOTKEY_INFO_K_HOTKEY_FUNC]

        try:
            # If the hotkey function needs call in main thread
            if tag_call_in_main_thread_exists(func):
                # If the hotkey function needs call with event info
                if tag_call_with_info_exists(func):
                    # Call the hotkey function with event info.
                    # Use the call result to decide whether propagate the
                    # event.
                    propagate = func(
                        hotkey,
                        hotkey_type,
                        hotkey_info,
                        event,
                    )

                # If the hotkey function not needs call with event info
                else:
                    # Call the hotkey function.
                    # Use the call result to decide whether propagate the
                    # event.
                    propagate = func()

            # If the hotkey function not needs call in main thread
            else:
                # If the hotkey function needs call with event info
                if tag_call_with_info_exists(func):
                    # Wrap the hotkey function with event info
                    func = partial(
                        func,
                        hotkey,
                        hotkey_type,
                        hotkey_info,
                        event,
                    )

                # Add the hotkey function to task queue
                add_task(func)

        # If have error
        except Exception:
            # Get traceback message
            tb_msg = format_exc()

            # Get error message
            msg = '# Error calling function in main thread:\n---\n{}---\n'\
                .format(tb_msg)

            # Print error message
            sys.stderr.write(msg)

        # Return whether propagate the event
        return propagate

    def _hotseq_find_and_call(self, vk, event, propagate=None):
        """
        Find and call key-sequence function.

        :param vk: Current down event's virtual key.

        :param event: Event object.

        :param propagate: Whether propagate the event.

        :return: A two-item tuple.

        Tuple format is:
        (
            Item 0,     # Whether hot-sequence is found.
            Item 1:     # Whether propagate the event.
        )
        """
        # Whether key-sequence is found
        hotseq_is_found = False

        # If the hotkey info map is empty
        if not self._hotkey_info_by_vk_map_for_key_seq:
            # Return result
            return (hotseq_is_found, propagate)

        # Add the virtual key to queue
        self._vk_s_dn_queue.append(vk)

        # Key-sequence's max length
        hotseq_len_max = 0

        # For the map's each key-sequence
        for hotseq, hotkey_info in \
                self._hotkey_info_by_vk_map_for_key_seq.items():
            # Get the key-sequence's length
            hotseq_len = len(hotseq)

            # If the key-sequence's length is GT the max length
            if hotseq_len > hotseq_len_max:
                # Use as max length
                hotseq_len_max = hotseq_len

            # If the key-sequence is triggered
            if self._hotseq_is_triggered(hotseq):
                # Set key-sequence is found
                hotseq_is_found = True

                # Call the key-sequence function
                propagate = self._hotkey_call(
                    hotkey=hotseq,
                    hotkey_type=HOTKEY_TYPE_V_KS,
                    hotkey_info=hotkey_info,
                    event=event,
                    propagate=propagate,
                )

                # Stop finding
                break

        # Get the queue length
        queue_len = len(self._vk_s_dn_queue)

        # Get the queue's extra length compared to key-sequence's max length
        extra_len = queue_len - hotseq_len_max

        # If have extra length,
        # it means the queue has stored more than needed number of virtual
        # keys.
        while extra_len > 0:
            # Pop the first item off the queue
            self._vk_s_dn_queue.popleft()

            # Decrement the extra length
            extra_len -= 1

        # Return the result
        return (hotseq_is_found, propagate)

    def _hotseq_is_triggered(self, hotseq):
        """
        Test whether given key-sequence is triggered.

        :param hotseq: Key-sequence's virtual key list.

        :return: Whether given key-sequence is triggered.
        """
        # Get given key-sequence's length
        hotseq_len = len(hotseq)

        # Compare with the newest virtual keys in the queue
        try:
            # For given key-sequence's each virtual key
            for idx, vk in enumerate(hotseq):
                # Get the corresponding virtual key's index in the queue.
                # E.g. `hotseq_len` is 2, then 0 -> -2, 1 -> -1.
                queue_idx = -hotseq_len + idx

                # May raise IndexError if the queue is not long enough
                queue_vk = self._vk_s_dn_queue[queue_idx]

                # If the virtual key is not EQ the corresponding virtual key
                if vk != queue_vk:
                    # Return False
                    return False

        # If the queue is not long enough
        except IndexError:
            # Return False
            return False

        # Return True
        return True

    def _vk_down_add(self, vk):
        """
        Add given virtual key to currently down list.

        :param vk: Virtual key.

        :return: None.
        """
        # Get virtual key info
        vk_info = (vk, time.time())

        # Add virtual key info to currently down list
        self._vk_s_dn.append(vk_info)

    def _vk_down_remove(self, vk):
        """
        Remove given virtual key from currently down list.

        :param vk: Virtual key.

        :return: None.
        """
        # New virtual key down list
        new_down_list = []

        # For each virtual key info in currently down list
        for vk_info in self._vk_s_dn:
            # If the virtual key is not given virtual key
            if vk_info[0] != vk:
                # Add the virtual key info to the new list
                new_down_list.append(vk_info)

        # Replace the old list with the new list
        self._vk_s_dn = new_down_list

    def _vk_down_remove_outdated(self):
        """
        Remove outdated virtual keys from currently down list.

        :return: None.
        """
        # Get timestamp min value before which virtual keys are considered
        # outdated
        timestamp_min = time.time() - 1

        # New virtual key down list
        new_down_list = []

        # For each virtual key info in currently down list
        for vk_info in self._vk_s_dn:
            # If the virtual key's timestamp is not outdated
            if vk_info[1] > timestamp_min:
                # Add the virtual key info to the new list
                new_down_list.append(vk_info)

        # Replace the old list with the new list
        self._vk_s_dn = new_down_list

    def vk_down_list(self):
        """
        Get currently down virtual key list.

        :return: Currently down virtual key list.
        """
        # Return currently down virtual key list
        return [x[0] for x in self._vk_s_dn]

    def vk_to_name(self, vk):
        """
        Convert virtual key to name.

        :param vk: Virtual key.

        :return: Virtual key's name.
        """
        # Convert virtual key to name
        return self._vk_ctn(vk)
