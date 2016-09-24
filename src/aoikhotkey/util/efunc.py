# coding: utf-8
"""
This module contains event functions.
"""
from __future__ import absolute_import

# Standard imports
import sys

# Internal imports
from aoikhotkey.runtime import hotkey_manager_get
from aoikhotkey.virtualkey import VK_MOUSE_MOVE


def efunc(event):
    """
    Event function that prints all events.

    :param event: Event object.

    :return: None.
    """
    # Get hotkey manager
    hotkey_manager = hotkey_manager_get()

    # If given event is mouse event
    if 'mouse' in event.MessageName:
        # Get virtual key from `Message` field
        vk = event.Message

    # If given event is not mouse event
    else:
        # Get virtual key from `KeyID` field
        vk = event.KeyID

    # If given event is mouse wheel event
    if 'mouse wheel' in event.MessageName:
        # Whether mouse wheel is scrolling up
        wheel_up = event.Wheel > 0

        # Get wheel side text
        wheel_side = 'up' if wheel_up else 'down'

    # If given event is not mouse wheel event
    else:
        # Set wheel side text be None
        wheel_side = None

    # Whether is up event
    is_up_event = 'up' in event.MessageName

    # Get currently down virtual key list's text list
    down_vk_text_s = [
        hotkey_manager.vk_to_name(_vk) or str(_vk)
        for _vk in hotkey_manager.vk_down_list()
    ]

    # If is up event
    if is_up_event:
        # Add the event virtual key's text, plus `(-)`
        down_vk_text_s.append(
            (hotkey_manager.vk_to_name(vk) or str(vk)) + '(-)'
        )

    # If is not up event
    else:
        # Add `(+)` to the last virtual key's text
        down_vk_text_s[-1] += '(+)'

    # Get message for the currently down virtual key list
    # E.g. `# LCTRL A(+)`
    msg = '# ' + ' '.join(down_vk_text_s) + '\n'

    # Print message
    sys.stderr.write(msg)

    # Get the event virtual key's name
    vk_name = hotkey_manager.vk_to_name(vk)

    # Get message for event
    msg = (
        'VK={vk} ({vk_hex}) Name={vk_name} Event={msg_name}'
        '{wheel_side}\n\n'
    ).format(
        vk=vk,
        vk_hex=hex(vk),
        vk_name=repr(vk_name if vk_name is not None else ''),
        msg_name=event.MessageName,
        wheel_side=' ' + wheel_side if wheel_side is not None else '',
    )

    # Print message
    sys.stderr.write(msg)


def efunc_no_mouse(event):
    """
    Event function that prints all but mouse events.

    :param event: Event object.

    :return: None.
    """
    # If given event is mouse event
    if 'mouse' in event.MessageName:
        # Return
        return

    # If given event is not mouse event
    else:
        # Delegate call to `efunc`
        return efunc(event)


def efunc_no_mouse_move(event):
    """
    Event function that prints all but mouse move events.

    :param event: Event object.

    :return: None.
    """
    # If given event is mouse move event
    if 'mouse' in event.MessageName and event.Message == VK_MOUSE_MOVE:
        # Return
        return

    # If given event is not mouse move event
    else:
        # Delegate call to `efunc`
        return efunc(event)
