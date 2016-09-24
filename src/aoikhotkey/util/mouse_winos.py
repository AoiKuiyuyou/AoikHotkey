# coding: utf-8
#
# Modified from http://schurpf.com/python-mouse-control/
"""
This module contains mouse utility for Windows platform.
"""
from __future__ import absolute_import

# Standard imports
import ctypes
from ctypes import byref
from ctypes.wintypes import POINT
from ctypes.wintypes import RECT
import time


_GetCursorPos = ctypes.windll.user32.GetCursorPos

_GetForegroundWindow = ctypes.windll.user32.GetForegroundWindow

_GetSystemMetrics = ctypes.windll.user32.GetSystemMetrics

_GetWindowRect = ctypes.windll.user32.GetWindowRect

_mouse_event = ctypes.windll.user32.mouse_event

_SetCursorPos = ctypes.windll.user32.SetCursorPos


class Mouse:
    """
    Mouse utility class.
    """

    # Mouse move event
    MOUSEEVENTF_MOVE = 0x0001

    # Mouse left button down event
    MOUSEEVENTF_LEFTDOWN = 0x0002

    # Mouse left button up event
    MOUSEEVENTF_LEFTUP = 0x0004

    # Mouse right button down event
    MOUSEEVENTF_RIGHTDOWN = 0x0008

    # Mouse right button up event
    MOUSEEVENTF_RIGHTUP = 0x0010

    # Mouse left middle down event
    MOUSEEVENTF_MIDDLEDOWN = 0x0020

    # Mouse left middle up event
    MOUSEEVENTF_MIDDLEUP = 0x0040

    # Mouse wheel event
    MOUSEEVENTF_WHEEL = 0x0800

    # Absolute move
    MOUSEEVENTF_ABSOLUTE = 0x8000

    # Screen width
    SM_CXSCREEN = 0

    # Screen height
    SM_CYSCREEN = 1

    def _send_mouse_event(self, flags, x_pos, y_pos, data, extra_info):
        """
        Send mouse event.

        :param flags: Flags.

        :param x_pos: X coordinate.

        :param y_pos: Y coordinate.

        :param data: Data.

        :param extra_info: Extra info.

        :return: None.
        """
        # Get x coordinate
        x_calc = 65536 * x_pos // _GetSystemMetrics(self.SM_CXSCREEN) + 1

        # Get y coordinate
        y_calc = 65536 * y_pos // _GetSystemMetrics(self.SM_CYSCREEN) + 1

        # Send mouse event
        _mouse_event(flags, x_calc, y_calc, data, extra_info)

    def _get_mouse_event_flags(self, button_name, button_up=False):
        """
        Get mouse event flags.

        :param button_name: Button name.

        :param button_up: Whether is button up.

        :return: Flags.
        """
        # Flags
        flags = 0

        # If is left button
        if button_name.find('left') >= 0:
            # Add flag
            flags += self.MOUSEEVENTF_LEFTDOWN

        # If is right button
        if button_name.find('right') >= 0:
            # Add flag
            flags += self.MOUSEEVENTF_RIGHTDOWN

        # If is middle button
        if button_name.find('middle') >= 0:
            # Add flag
            flags += flags + self.MOUSEEVENTF_MIDDLEDOWN

        # If is button up
        if button_up:
            # Left-shift the flags by one bit
            flags = flags << 1

        # Return the flags
        return flags

    def move_cursor(self, position):
        """
        Move cursor to given position.

        :param position: Position tuple of (x, y).

        :return: None.
        """
        # Get x and y coordinates
        x, y = position

        # Get old position
        old_pos = self.get_cursor_position()

        # Get x coordinate
        x = x if (x != -1) else old_pos[0]

        # Get y coordinate
        y = y if (y != -1) else old_pos[1]

        # Send mouse event
        self._send_mouse_event(
            self.MOUSEEVENTF_MOVE + self.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0
        )

    def get_cursor_position(self):
        """
        Get cursor position.

        :return: A tuple of (x, y).
        """
        # Create point structure
        point = POINT()

        # Get cursor position
        _GetCursorPos(byref(point))

        # Return position tuple
        return (point.x, point.y)

    def click(self, button_name='left'):
        """
        Click at current position.
        """
        # Send press and release button events
        self._send_mouse_event(
            self._get_mouse_event_flags(button_name, False) +
            self._get_mouse_event_flags(button_name, True),
            0, 0, 0, 0
        )

    def click_screen_position(
        self,
        position,
        button_name='left',
        pre_click_wait=0,
        post_click_move=False,
    ):
        """
        Click a absolute position.

        :param position: Position tuple of (x, y).

        :param button_name: Button name.

        :param pre_click_wait: Pre-click wait time.

        :param post_click_move: Whether restore old cursor position after \
            click.

        :return: None.
        """
        # If need restore old position after click
        if post_click_move:
            # Store old cursor position
            x_old, y_old = self.get_cursor_position()

        # Set new cursor position
        _SetCursorPos(position[0], position[1])

        # If have pre-click wait time
        if pre_click_wait:
            # Sleep
            time.sleep(pre_click_wait)

        # Click
        self.click(button_name)

        # If need restore old position after click
        if post_click_move:
            # Restore old cursor position
            _SetCursorPos(x_old, y_old)

    def click_window_position(
        self,
        position,
        button_name='left',
        pre_click_wait=0,
        post_click_move=False,
        hwnd=None,
    ):
        """
        Click relative position in a window.

        :param position: Position tuple of (x_offset, y_offset).

        :param button_name: Button name.

        :param post_click_move: Whether restore old cursor position after \
            click.

        :param pre_click_wait: Pre-click wait time.

        :param hwnd: Window handle.

        :return: None.
        """
        # If window handle is not given
        if hwnd is None:
            # Get foreground window's handle
            hwnd = _GetForegroundWindow()

        # Get window's rectangle coordinates
        x_left, y_top, _, _ = self.get_window_rect(hwnd)

        # Get absolute x
        abs_x = x_left + position[0]

        # Get absolute y
        abs_y = y_top + position[1]

        # Click at the position
        self.click_screen_position(
            position=(abs_x, abs_y),
            button_name=button_name,
            pre_click_wait=pre_click_wait,
            post_click_move=post_click_move,
        )

    def get_window_rect(self, hwnd):
        """
        Get window's rectangle coordinates.

        :param hwnd: Window handle.

        :return: A tuple of (x_left, y_top, x_right, y_bottom).
        """
        # Create RECT structure
        rect = RECT()

        # Get given window's rectangle
        _GetWindowRect(hwnd, byref(rect))

        # Create rectangle tuple
        rect_tuple = (rect.left, rect.top, rect.right, rect.bottom)

        # Return the rectangle tuple
        return rect_tuple
