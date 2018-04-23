# coding: utf-8
"""
This module contains event manager for Windows platform.
"""
from __future__ import absolute_import

# Standard imports
import ctypes
from ctypes import byref

# External imports
from PyHook3 import HookManager


user32 = ctypes.cdll.LoadLibrary('user32.dll')

LONG = ctypes.c_int32
DWORD = ctypes.c_ulong
UINT = ctypes.c_uint
BOOL = ctypes.c_int
HANDLE = ctypes.c_void_p
HWND = HANDLE

if ctypes.sizeof(ctypes.c_long) == ctypes.sizeof(ctypes.c_void_p):
    WPARAM = ctypes.c_ulong
    LPARAM = ctypes.c_long
elif ctypes.sizeof(ctypes.c_longlong) == ctypes.sizeof(ctypes.c_void_p):
    WPARAM = ctypes.c_ulonglong
    LPARAM = ctypes.c_longlong


class POINT(ctypes.Structure):
    _fields_ = [
        ("x", LONG),
        ("y", LONG)]


class MSG(ctypes.Structure):
    _fields_ = [
        ("hWnd", HWND),
        ("message", UINT),
        ("wParam", WPARAM),
        ("lParam", LPARAM),
        ("time", DWORD),
        ("pt", POINT)]


GetMessageW = user32.GetMessageW

PostQuitMessage = user32.PostQuitMessage


class EventManager(object):
    """
    Event manager that runs event loop and calls event handlers.
    """

    def __init__(self):
        """
        Constructor.

        :return: None.
        """
        # Create hook manager
        self._hook_manager = HookManager()

        # Add attributes `mouse_hook` and `keyboard_hook`.
        # Without the two attributes, the hook manager's method `__del__`
        # will raise AttributeError if its methods `HookKeyboard` and
        # `HookMouse` have not been called.
        self._hook_manager.mouse_hook = False

        self._hook_manager.keyboard_hook = False

    def start_event_loop(self):
        """
        Start event loop.

        This method will not return until the event loop is stopped by \
        calling :paramref:`stop_event_loop`.

        :return: None.
        """
        # Start hooking key events
        self._hook_manager.HookKeyboard()

        # Start hooking mouse events
        self._hook_manager.HookMouse()

        # Create MSG structure
        msg = MSG()

        # Run event loop
        GetMessageW(byref(msg), 0, 0, 0)

        # Stop hooking key events
        self._hook_manager.UnhookKeyboard()

        # Stop hooking mouse events
        self._hook_manager.UnhookMouse()

    def stop_event_loop(self):
        """
        Stop event loop.

        :return: None.
        """
        # Post a WM_QUIT message to this thread's message queue
        PostQuitMessage(0)

    # Map event handler type to handler attribute name
    _EVENT_HANDLER_TYPE_TO_ATTR_NAME = {
        'KeyDown': 'KeyDown',
        'KeyUp': 'KeyUp',
        'MouseDown': 'MouseAllButtonsDown',
        'MouseUp': 'MouseAllButtonsUp',
        'MouseMove': 'MouseMove',
        'MouseWheel': 'MouseWheel',
    }

    def add_handler(self, handler_type, handler):
        """
        Add event handler.

        :param handler_type: Event handler type.

        Allowed values:
            - 'KeyDown'
            - 'KeyUp'
            - 'MouseDown'
            - 'MouseUp'
            - 'MouseMove'
            - 'MouseWheel'

        :param handler: Event handler.

        :return: None.
        """
        # Get handler attribute name
        attr_name = self._EVENT_HANDLER_TYPE_TO_ATTR_NAME.get(
            handler_type, None
        )

        # If handler attribute name is not found,
        # it means given handler type is not valid.
        if attr_name is None:
            # Get error message
            msg = 'Error: Invalid handler type: {0}'.format(
                repr(handler_type)
            )

            # Raise error
            raise ValueError(msg)

        # If handler attribute name is found.

        # Set the handler attribute on the hook manager
        setattr(self._hook_manager, attr_name, handler)

    def remove_handlers(self):
        """
        Remove all event handlers.

        :return: None.
        """
        # Set handler attributes on the hook manager be None
        self._hook_manager.KeyDown = None

        self._hook_manager.KeyUp = None

        self._hook_manager.MouseAllButtonsDown = None

        self._hook_manager.MouseAllButtonsUp = None

        self._hook_manager.MouseMove = None

        self._hook_manager.MouseWheel = None
