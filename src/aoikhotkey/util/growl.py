# coding: utf-8
"""
This module contains hotkey trigger function that sends notifications to Growl.
"""
from __future__ import absolute_import

# Standard imports
import sys
from traceback import format_exc

# Internal imports
from aoikhotkey.const import HOTKEY_INFO_K_HOTKEY_ORIG_SPEC
from aoikhotkey.const import HOTKEY_TYPE_V_DN
from aoikhotkey.const import HOTKEY_TYPE_V_KS
from aoikhotkey.const import HOTKEY_TYPE_V_UP
from aoikhotkey.task_manager import add_task
from aoikhotkey.util.tfunc import hotkey_tfunc as hotkey_tfunc_default


# Growl notifier.
# This variable is initialized inside `hotkey_tfunc` below.
_GROWL_NOTI = None


def hotkey_tfunc(hotkey_manager, hotkey, hotkey_type, hotkey_info, event):
    """
    Hotkey trigger function that sends notification to Growl.

    :param hotkey_manager: Hotkey manager.

    :param hotkey: Hotkey's virtual key list.

    :param hotkey_type: Hotkey type.

    :param hotkey_info: Hotkey info.

    :param event: Event object.

    :return: None.
    """
    # Create task function
    def task_func():
        # Call default hotkey trigger function to print message to console
        hotkey_tfunc_default(
            hotkey_manager, hotkey, hotkey_type, hotkey_info, event
        )

        # Use global variable
        global _GROWL_NOTI

        # If the Growl notifier is False,
        # it means the initialization below failed.
        if _GROWL_NOTI is False:
            # Do not send message to Growl
            return

        # If the Growl notifier is not False.

        # If the Growl notifier is None,
        # it means the initialization is not done yet.
        if _GROWL_NOTI is None:
            try:
                # Import module
                import gntp.notifier

                # Create Growl notifier
                _GROWL_NOTI = gntp.notifier.GrowlNotifier(
                    applicationName='AoikHotkey',
                    notifications=['New Messages'],
                    defaultNotifications=['New Messages'],
                )

                # Register with Growl
                _GROWL_NOTI.register()

            # If have import error
            except ImportError:
                # Set the Growl notifier be False
                _GROWL_NOTI = False

                # Get error message
                msg = (
                    'Package `gntp` is not installed. Try:\n'
                    'pip install gntp\n'
                )

                # Print error message
                sys.stderr.write(msg)

                # Do not send message to Growl
                return

            # If have other error
            except Exception:
                # Set the Growl notifier be False
                _GROWL_NOTI = False

                # Get traceback message
                tb_msg = format_exc()

                # Get error message
                msg = (
                    '# Error: Failed initializing Growl notifier:\n'
                    '---\n{0}---\n'
                ).format(tb_msg)

                # Print error message
                sys.stderr.write(msg)

                # Do not send message to Growl
                return

        # Assert the Growl notifier is not False or None
        assert _GROWL_NOTI

        # If hotkey type is key-down
        if hotkey_type == HOTKEY_TYPE_V_DN:
            # Get text
            up_dn_text = ' down '

        # If hotkey type is key-up
        elif hotkey_type == HOTKEY_TYPE_V_UP:
            # Get text
            up_dn_text = ' up '

        # If hotkey type is not key-down or key-up
        else:
            # Get text
            up_dn_text = ' '

        # Get original hotkey spec
        orig_spec = hotkey_info[HOTKEY_INFO_K_HOTKEY_ORIG_SPEC]

        # Get notification title
        title = '{hotkey_type}{up_dn_text}triggered'.format(
            hotkey_type='Hotseq'
            if hotkey_type == HOTKEY_TYPE_V_KS else 'Hotkey',
            up_dn_text=up_dn_text,
        )

        # Get hotkey pattern
        hotkey_pattern = orig_spec[0]

        # Get notification description
        description = '{hotkey_pattern}\n{hotkey_vk_names}'.format(
            hotkey_pattern=hotkey_pattern,
            hotkey_vk_names=' '.join(
                hotkey_manager.vk_to_name(x) or str(x) for x in hotkey
            ),
        )

        # Create task function
        _GROWL_NOTI.notify(
            noteType='New Messages',
            title=title,
            description=description,
        )

    # Add task function to queue
    add_task(task_func)
