# coding: utf-8
"""
This module contains event manager for X11 platform.
"""
from __future__ import absolute_import

# External imports
from pyxHook import HookManager


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

    def start_event_loop(self):
        """
        Start event loop.

        This method will not return until the event loop is stopped by \
        calling :paramref:`stop_event_loop`.

        :return: None.
        """
        # Start event loop
        self._hook_manager.run()

    def stop_event_loop(self):
        """
        Stop event loop.

        :return: None.
        """
        # If event loop is running.
        #
        # Attribute `ctx` is created in the hook manager's `run` method.
        if hasattr(self._hook_manager, 'ctx'):
            # Stop the event loop
            self._hook_manager.cancel()

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
        # Set handler attributes on the hook manager be noop function
        self._hook_manager.KeyDown = lambda x: True

        self._hook_manager.KeyUp = lambda x: True

        self._hook_manager.MouseAllButtonsDown = lambda x: True

        self._hook_manager.MouseAllButtonsUp = lambda x: True

        self._hook_manager.MouseMove = lambda x: True

        self._hook_manager.MouseWheel = lambda x: True
