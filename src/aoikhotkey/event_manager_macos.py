# coding: utf-8
"""
This module contains event manager for MacOS platform.
"""
from __future__ import absolute_import

# Standard imports
import sys
from traceback import format_exc

# External imports
from AppKit import NSDate
from AppKit import NSEvent
from AppKit import NSProcessInfo
import Quartz

# Local imports
from .virtualkey import KVK_CAPSLOCK
from .virtualkey import KVK_COMMAND
from .virtualkey import KVK_CONTROL
from .virtualkey import KVK_OPTION
from .virtualkey import KVK_RIGHTCOMMAND
from .virtualkey import KVK_RIGHTCONTROL
from .virtualkey import KVK_RIGHTOPTION
from .virtualkey import KVK_RIGHTSHIFT
from .virtualkey import KVK_SHIFT


class _Event(object):
    """
    Cross-platform event class. Event instances are passed to event handlers.
    """


class EventManager(object):
    """
    Event manager that runs event loop and calls event handlers.
    """

    def __init__(self):
        """
        Constructor.

        :return: None.
        """
        # Create event tap
        self._tap = Quartz.CGEventTapCreate(
            # The tap is for session events
            Quartz.kCGSessionEventTap,
            # The tap is inserted before existing event taps
            Quartz.kCGHeadInsertEventTap,
            # The tap is active filter
            Quartz.kCGEventTapOptionDefault,
            # The tap listens to all events
            Quartz.kCGEventMaskForAllEvents,
            # The tap calls this callback
            self._tap_callback,
            # User-defined data
            None
        )

        # Create run loop source
        run_loop_source = Quartz.CFMachPortCreateRunLoopSource(
            None, self._tap, 0
        )

        # Add run loop source to the current run loop
        Quartz.CFRunLoopAddSource(
            Quartz.CFRunLoopGetCurrent(),
            run_loop_source,
            Quartz.kCFRunLoopDefaultMode
        )

        # Key-down event handler
        self.KeyDown = None

        # Key-up event handler
        self.KeyUp = None

        # Mouse-down event handler
        self.MouseDown = None

        # Mouse-up event handler
        self.MouseUp = None

        # Mouse wheel event handler
        self.MouseWheel = None

        # Mouse move event handler
        self.MouseMove = None

        # Modifier states that indicate whether each modifier is on or off.
        self._modifier_states = {
            'LCTRL': 0,
            'RCTRL': 0,
            'LCMD': 0,
            'RCMD': 0,
            'LALT': 0,
            'RALT': 0,
            'LSHIFT': 0,
            'RSHIFT': 0,
            'CAPSLOCK': 0,
        }

        # Get current timestamp
        current_timestamp = NSDate.date().timeIntervalSince1970()

        # Get interval since the system boot time
        system_up_interval = NSProcessInfo.processInfo().systemUptime()

        # Get the system boot time's timestamp.
        # This is used for calculating each event's timestamp.
        self._system_up_timestamp = current_timestamp - system_up_interval

    def start_event_loop(self):
        """
        Start event loop.

        This method will not return until the event loop is stopped by \
        calling :paramref:`stop_event_loop`.

        :return: None.
        """
        # Enable the tap
        Quartz.CGEventTapEnable(self._tap, True)

        # Run the current run loop
        Quartz.CFRunLoopRun()

    def stop_event_loop(self):
        """
        Stop event loop.

        :return: None.
        """
        # Stop the current run loop
        Quartz.CFRunLoopStop(Quartz.CFRunLoopGetCurrent())

    def _tap_callback(self, proxy, type_, event, refcon):
        """
        Event tap callback.

        This callback delegates call to :paramref:`_tap_callback_inner`. If \
        any exception is raised inside `_tap_callback_inner`, the exception \
        will be caught, stack trace will be printed, and given event object \
        will be returned to let the event propagate, without being affected \
        by the exception.

        :param proxy: Event tap proxy.

        :param type_: Event type.

        :param event: CGEvent object.

        :param refcon: User-defined data.

        :return: Given event object to propagate the event, or None to \
        discard the event.
        """
        try:
            # Delegate call to `_tap_callback_inner`
            return self._tap_callback_inner(proxy, type_, event, refcon)

        # If have error
        except Exception:
            # Print stack trace
            sys.stderr.write(format_exc())

            # Return the event object to let the event propagate
            return event

    # Mouse button event type set
    _MOUSE_BUTTON_EVENTS = {
        Quartz.kCGEventLeftMouseDown,
        Quartz.kCGEventLeftMouseUp,
        Quartz.kCGEventRightMouseDown,
        Quartz.kCGEventRightMouseUp,
        Quartz.kCGEventOtherMouseDown,
        Quartz.kCGEventOtherMouseUp,
    }

    # Mouse move and wheel event type set
    _MOUSE_MOVE_WHEEL_EVENTS = {
        Quartz.kCGEventMouseMoved,
        Quartz.kCGEventScrollWheel,
    }

    def _tap_callback_inner(self, proxy, type_, event, refcon):
        """
        Event tap callback :paramref:`_tap_callback`'s inner function.

        :param proxy: Event tap proxy.

        :param type_: Event type.

        :param event: CGEvent object.

        :param refcon: User-defined data.

        :return: Given event object to propagate the event, or None to \
        discard the event.
        """
        # Convert given CGEvent into NSEvent
        ns_event = NSEvent.eventWithCGEvent_(event)

        # Get event type
        event_type = ns_event.type()

        # Whether propagate the event
        propagate = True

        # If is modifier key event
        if event_type == Quartz.kCGEventFlagsChanged:
            # Handle the event
            propagate = self._handle_modifier_key_event(
                event=event,
                ns_event=ns_event,
                propagate=propagate,
            )

        # If is key event
        elif (
            event_type == Quartz.kCGEventKeyDown or
            event_type == Quartz.kCGEventKeyUp
        ):
            # Handle the event
            propagate = self._handle_key_event(
                event=event,
                ns_event=ns_event,
                propagate=propagate,
            )

        # If is mouse button event
        elif event_type in self._MOUSE_BUTTON_EVENTS:
            # Handle the event
            propagate = self._handle_mouse_button_event(
                event=event,
                ns_event=ns_event,
                propagate=propagate,
            )

        # If is mouse move or wheel event
        elif event_type in self._MOUSE_MOVE_WHEEL_EVENTS:
            # Handle the event
            propagate = self._handle_mouse_move_wheel_event(
                event=event,
                ns_event=ns_event,
                propagate=propagate,
            )

        # If is none of above
        else:
            # Ignore
            pass

        # If need propagate the event
        if propagate:
            # Return the event object
            return event

        # If not need propagate the event
        else:
            # Return None
            return None

    # Map modifier type to virtual key
    _MODIFIER_TYPE_TO_VK = {
        'LCTRL': KVK_CONTROL,
        'RCTRL': KVK_RIGHTCONTROL,
        'LCMD': KVK_COMMAND,
        'RCMD': KVK_RIGHTCOMMAND,
        'LALT': KVK_OPTION,
        'RALT': KVK_RIGHTOPTION,
        'LSHIFT': KVK_SHIFT,
        'RSHIFT': KVK_RIGHTSHIFT,
        'CAPSLOCK': KVK_CAPSLOCK,
    }

    def _handle_modifier_key_event(
        self,
        event,
        ns_event,
        propagate,
        dim=False,
    ):
        """
        Modifier key event handler called by :paramref:`_tap_callback_inner`.

        This handler translates platform-specific event to cross-platform event
        object. And then calls `self.KeyDown` or `self.KeyUp` with the
        cross-platform event object.

        :param event: CGEvent object.

        :param ns_event: NSEvent object.

        :param propagate: Whether propagate the event.

        :param dim: Whether use device independent modifier.

        :return: Given event object to propagate the event, or None to \
        discard the event.
        """
        # Get modifier flags
        flags = ns_event.modifierFlags()

        # If use device independent modifier
        if dim:
            # Filter the flags using DIM flags mask
            flags &= Quartz.NSDeviceIndependentModifierFlagsMask

        # If use device independent modifier
        if dim:
            # Use general mask to test for LCTRL
            lctrl_bits = Quartz.kCGEventFlagMaskControl

            # Do not test for RCTRL
            rctrl_bits = 0

            # Use general mask to test for LCMD
            lcmd_bits = Quartz.kCGEventFlagMaskCommand

            # Do not test for RCMD
            rcmd_bits = 0

            # Use general mask to test for LALT
            lalt_bits = Quartz.kCGEventFlagMaskAlternate

            # Do not test for RALT
            ralt_bits = 0

            # Use general mask to test for LSHIFT
            lshift_bits = Quartz.kCGEventFlagMaskShift

            # Do not test for RSHIFT
            rshift_bits = 0

        # If not use device independent modifier
        else:
            # Use specific mask to test for LCTRL
            lctrl_bits = Quartz.kCGEventFlagMaskControl | 1

            # Use specific mask to test for RCTRL
            rctrl_bits = Quartz.kCGEventFlagMaskControl | 0x2000

            # Use specific mask to test for LCMD
            lcmd_bits = Quartz.kCGEventFlagMaskCommand | 0b1000

            # Use specific mask to test for RCMD
            rcmd_bits = Quartz.kCGEventFlagMaskCommand | 0b10000

            # Use specific mask to test for LALT
            lalt_bits = Quartz.kCGEventFlagMaskAlternate | 0b100000

            # Use specific mask to test for RALT
            ralt_bits = Quartz.kCGEventFlagMaskAlternate | 0b1000000

            # Use specific mask to test for LSHIFT
            lshift_bits = Quartz.kCGEventFlagMaskShift | 0b10

            # Use specific mask to test for RSHIFT
            rshift_bits = Quartz.kCGEventFlagMaskShift | 0b100

        # Get new modifier states
        new_modifier_states = {
            'LCTRL': int(
                lctrl_bits and ((flags & lctrl_bits) == lctrl_bits)
            ),
            'RCTRL': int(
                rctrl_bits and ((flags & rctrl_bits) == rctrl_bits)
            ),
            'LCMD': int((flags & lcmd_bits) == lcmd_bits),
            'RCMD': int((flags & rcmd_bits) == rcmd_bits),
            'LALT': int(lalt_bits and ((flags & lalt_bits) == lalt_bits)),
            'RALT': int(ralt_bits and ((flags & ralt_bits) == ralt_bits)),
            'LSHIFT': int(
                lshift_bits and ((flags & lshift_bits) == lshift_bits)
            ),
            'RSHIFT': int(
                rshift_bits and ((flags & rshift_bits) == rshift_bits)),
            'CAPSLOCK': int(bool(flags & Quartz.kCGEventFlagMaskAlphaShift)),
        }

        # For each modifier key
        for key in [
            'LCTRL', 'RCTRL',
            'LCMD', 'RCMD',
            'LALT', 'RALT',
            'LSHIFT', 'RSHIFT',
            'CAPSLOCK',
        ]:
            # Get the modifier's old state
            old_state = self._modifier_states[key]

            # Get the modifier's new state
            new_state = new_modifier_states[key]

            # If the old state is smaller,
            # it means the modifier key is being pressed.
            if old_state < new_state:
                # If have key-down handler
                if self.KeyDown:
                    # Create event object
                    hotkey_event = _Event()

                    # Store the NSEvent
                    hotkey_event.Event = ns_event

                    # Store the modifier key's name
                    hotkey_event.Key = key

                    # Store the modifier key's virtual key
                    hotkey_event.KeyID = self._MODIFIER_TYPE_TO_VK[key]

                    # Set `Message` field be None
                    hotkey_event.Message = None

                    # Store event type
                    hotkey_event.MessageName = 'key down'

                    # Call the key-down handler.
                    # Use the call result to decide whether propagate the
                    # event.
                    propagate = self.KeyDown(hotkey_event)

            # If the old state is greater,
            # it means the modifier key is being released.
            elif old_state > new_state:
                # If have key-up handler
                if self.KeyUp:
                    # Create event object
                    hotkey_event = _Event()

                    # Store the NSEvent
                    hotkey_event.Event = ns_event

                    # Store the modifier key's name
                    hotkey_event.Key = key

                    # Store the modifier key's virtual key
                    hotkey_event.KeyID = self._MODIFIER_TYPE_TO_VK[key]

                    # Set `Message` field be None
                    hotkey_event.Message = None

                    # Store event type
                    hotkey_event.MessageName = 'key up'

                    # Call the key-up handler.
                    # Use the call result to decide whether propagate the
                    # event.
                    propagate = self.KeyUp(hotkey_event)

        # Store the new modifier states
        self._modifier_states = new_modifier_states

        # Return whether propagate the event
        return propagate

    def _handle_key_event(self, event, ns_event, propagate):
        """
        Key event handler called by :paramref:`_tap_callback_inner`.

        This handler translates platform-specific event to cross-platform event
        object. And then calls `self.KeyDown` or `self.KeyUp` with the
        cross-platform event object.

        :param event: CGEvent object.

        :param ns_event: NSEvent object.

        :param propagate: Whether propagate the event.

        :return: Given event object to propagate the event, or None to \
        discard the event.
        """
        # Get event type
        event_type = ns_event.type()

        # Get the key's name
        key = str(ns_event.charactersIgnoringModifiers())

        # Get the key's virtual key
        key_id = ns_event.keyCode()

        # If is key-down event
        if event_type == Quartz.kCGEventKeyDown:
            # If have key-down handler
            if self.KeyDown:
                # Create event object
                hotkey_event = _Event()

                # Store the NSEvent
                hotkey_event.Event = ns_event

                # Store the key's name
                hotkey_event.Key = key

                # Store the key's virtual key
                hotkey_event.KeyID = key_id

                # Set `Message` field be None
                hotkey_event.Message = None

                # Store event type
                hotkey_event.MessageName = 'key down'

                # Call the key down handler.
                # Use the call result to decide whether propagate the event.
                propagate = self.KeyDown(hotkey_event)

        # If is key-up event
        elif event_type == Quartz.kCGEventKeyUp:
            # If have key-up handler
            if self.KeyUp:
                # Create event object
                hotkey_event = _Event()

                # Store the NSEvent
                hotkey_event.Event = ns_event

                # Store the key's name
                hotkey_event.Key = key

                # Store the key's virtual key
                hotkey_event.KeyID = key_id

                # Set `Message` field be None
                hotkey_event.Message = None

                # Store event type
                hotkey_event.MessageName = 'key up'

                # Call the key up handler.
                # Use the call result to decide whether propagate the event.
                propagate = self.KeyUp(hotkey_event)

        # If is not key-down or key-up event
        else:
            # Raise error
            assert 0, event_type

        # Return whether propagate the event
        return propagate

    # Map mouse event type to info tuple.
    #
    # The info tuple's format is:
    # (
    #     Event object's `Message` field value,
    #     Event object's `MessageName` field value,
    #     Event handler attribute name,
    # )
    #
    # The `Message` field values are consistent with what pyHook event object
    # contains on Windows platform.
    _MOUSE_EVENT_TYPE_TO_INFO_TUPLE = {
        Quartz.kCGEventLeftMouseDown: (513, 'mouse left down', 'MouseDown'),
        Quartz.kCGEventLeftMouseUp: (514, 'mouse left up', 'MouseUp'),
        Quartz.kCGEventRightMouseDown: (516, 'mouse right down', 'MouseDown'),
        Quartz.kCGEventRightMouseUp: (517, 'mouse right up', 'MouseUp'),
        Quartz.kCGEventOtherMouseDown: (519, 'mouse middle down', 'MouseDown'),
        Quartz.kCGEventOtherMouseUp: (520, 'mouse middle up', 'MouseUp'),
        Quartz.kCGEventMouseMoved: (512, 'mouse move', 'MouseMove'),
        Quartz.kCGEventScrollWheel: (522, 'mouse wheel', 'MouseWheel'),
    }

    def _handle_mouse_button_event(self, event, ns_event, propagate):
        """
        Mouse button event handler called by :paramref:`_tap_callback_inner`.

        This handler translates platform-specific event to cross-platform event
        object. And then calls `self.MouseDown` or `self.MouseUp` with the
        cross-platform event object.

        :param event: CGEvent object.

        :param ns_event: NSEvent object.

        :param propagate: Whether propagate the event.

        :return: Given event object to propagate the event, or None to \
        discard the event.
        """
        # Get event type
        event_type = ns_event.type()

        # Get event object's `Message` and `MessageName` field values, and
        # event handler attribute name
        message, message_name, handler_attr_name = \
            self._MOUSE_EVENT_TYPE_TO_INFO_TUPLE[event_type]

        # Get event handler
        event_handler = getattr(self, handler_attr_name, None)

        # If the event handler is not None
        if event_handler is not None:
            # Get location x coordinate
            location_x = ns_event.locationInWindow().x

            # Get location y coordinate
            location_y = ns_event.locationInWindow().y

            # Get position tuple
            position = (location_x, location_y)

            # Get click count
            click_count = ns_event.clickCount()

            # Get timestamp
            timestamp = self._system_up_timestamp + ns_event.timestamp()

            # Create event object
            hotkey_event = _Event()

            # Store the NSEvent
            hotkey_event.Event = ns_event

            # Store the message value
            hotkey_event.Message = message

            # Store the message name value
            hotkey_event.MessageName = message_name

            # Store the position tuple
            hotkey_event.Position = position

            # Store the click count
            hotkey_event.ClickCount = click_count

            # Set `Wheel` field be 0
            hotkey_event.Wheel = 0

            # Store the timestamp
            hotkey_event.Time = timestamp

            # Call the event handler.
            # Use the call result to decide whether propagate the event.
            propagate = event_handler(hotkey_event)

        # Return whether propagate the event
        return propagate

    def _handle_mouse_move_wheel_event(self, event, ns_event, propagate):
        """
        Mouse move or wheel event handler called by \
        :paramref:`_tap_callback_inner`.

        This handler translates platform-specific event to cross-platform event
        object. And then calls `self.MouseMove` or `self.MouseWheel` with the
        cross-platform event object.

        :param event: CGEvent object.

        :param ns_event: NSEvent object.

        :param propagate: Whether propagate the event.

        :return: Given event object to propagate the event, or None to \
        discard the event.
        """
        # Get event type
        event_type = ns_event.type()

        # Get event object's `Message` and `MessageName` field values, and
        # event handler attribute name
        message, message_name, handler_attr_name = \
            self._MOUSE_EVENT_TYPE_TO_INFO_TUPLE[event_type]

        # Get event handler
        event_handler = getattr(self, handler_attr_name, None)

        # If the event handler is not None
        if event_handler is not None:
            # Get location x coordinate
            location_x = ns_event.locationInWindow().x

            # Get location y coordinate
            location_y = ns_event.locationInWindow().y

            # Get position tuple
            position = (location_x, location_y)

            # Get mouse wheel's deltaY value
            wheel = int(ns_event.deltaY())

            # Get timestamp
            timestamp = self._system_up_timestamp + ns_event.timestamp()

            # Create event object
            hotkey_event = _Event()

            # Store the NSEvent
            hotkey_event.Event = ns_event

            # Store the message value
            hotkey_event.Message = message

            # Store the message name value
            hotkey_event.MessageName = message_name

            # Store the position tuple
            hotkey_event.Position = position

            # Set `ClickCount` field be 0
            hotkey_event.ClickCount = 0

            # Store the mouse wheel's deltaY value
            hotkey_event.Wheel = wheel

            # Store the timestamp
            hotkey_event.Time = timestamp

            # Call the event handler.
            # Use the call result to decide whether propagate the event.
            propagate = event_handler(hotkey_event)

        # Return whether propagate the event
        return propagate

    # Event handler attribute name set
    _EVENT_HANDLER_TYPES = {
        'KeyDown',
        'KeyUp',
        'MouseDown',
        'MouseUp',
        'MouseMove',
        'MouseWheel',
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
        # If given handler type is not valid
        if handler_type not in self._EVENT_HANDLER_TYPES:
            # Get error message
            msg = 'Error: Invalid handler type: {0}'.format(
                repr(handler_type)
            )

            # Raise error
            raise ValueError(msg)

        # If given handler type is valid.

        # Set the handler attribute
        setattr(self, handler_type, handler)

    def remove_handlers(self):
        """
        Remove all event handlers.

        :return: None.
        """
        # Set handler attributes be None
        self.KeyDown = None

        self.KeyUp = None

        self.MouseDown = None

        self.MouseUp = None

        self.MouseWheel = None

        self.MouseMove = None
