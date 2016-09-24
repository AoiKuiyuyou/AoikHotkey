# coding: utf-8
"""
This module contains hotkey functions and utility.
"""
from __future__ import absolute_import

# Standard imports
from functools import partial
from subprocess import Popen
from time import sleep

# Internal imports
from aoikhotkey.const import SpecReloadExc
from aoikhotkey.const import SpecSwitchExc
from aoikhotkey.hotkey_spec_parser import tag_call_in_main_thread
from aoikhotkey.runtime import hotkey_manager_get


@tag_call_in_main_thread
def Quit():
    """
    Hotkey function that stops hotkey manager's event loop.

    :return: None.
    """
    # Stop hotkey manager's event loop
    hotkey_manager_get().eloop_stop()


@tag_call_in_main_thread
def SpecReload():
    """
    Hotkey function that reloads hotkey spec.

    :return: None.
    """
    # Create event loop stop callback
    def stop_callback():
        # Raise special exception to notify upper context to reload hotkey spec
        raise SpecReloadExc()

    # Get hotkey manager
    hotkey_manager = hotkey_manager_get()

    # Set hotkey manager's event loop stop callback
    hotkey_manager.eloop_stop_callback_set(stop_callback)

    # Stop hotkey manager's event loop
    hotkey_manager.eloop_stop()


def spec_switch(spec_id):
    """
    Switch hotkey spec.

    :param spec_id: Hotkey spec ID or index.

    :return: None.
    """
    # Create event loop stop callback
    def stop_callback():
        # Raise special exception to notify upper context to switch hotkey spec
        raise SpecSwitchExc(spec_id)

    # Get hotkey manager
    hotkey_manager = hotkey_manager_get()

    # Set hotkey manager's event loop stop callback
    hotkey_manager.eloop_stop_callback_set(stop_callback)

    # Stop hotkey manager's event loop
    hotkey_manager.eloop_stop()


def SpecSwitch(spec_id):
    """
    Create hotkey function that switches hotkey spec.

    :param spec_id: Hotkey spec ID or index.

    :return: Hotkey function.
    """
    # Create hotkey function that switches hotkey spec
    func = partial(spec_switch, spec_id)

    # Add `call in main thread` tag
    func = tag_call_in_main_thread(func)

    # Return the hotkey function
    return func


def EventPropagate():
    """
    Hotkey function that returns True to propagate the event that triggers \
    the hotkey.

    :return: True.
    """
    # Return True
    return True


def EventStop():
    """
    Hotkey function that returns False to discard the event that triggers \
    the hotkey.

    :return: False.
    """
    # Return False
    return False


class Cmd(object):
    """
    Hotkey function class that runs a command.
    """

    def __init__(self, *cmd_part_s):
        """
        Constructor.
        """
        # Assert command part list is not empty
        assert cmd_part_s

        # Get the first part
        first_part = cmd_part_s[0]

        # If the first part is list,
        # e.g. Cmd(['echo', 'hello'])
        if isinstance(first_part, list):
            # Assert it is the only part
            assert len(cmd_part_s) == 1

            # Use the list as command part list
            cmd_part_s = first_part

        # Store command parts
        self._cmd_part_s = cmd_part_s

    def __call__(self):
        """
        Hotkey function that runs the command.

        :return: None.
        """
        # Run the command
        Popen(self._cmd_part_s, shell=True)


def Sleep(duration):
    """
    Create hotkey function that sleeps for given duration.

    :param duration: Sleep duration.

    :return: Created function.
    """
    # Return hotkey function that sleeps for given duration
    return partial(sleep, duration)
