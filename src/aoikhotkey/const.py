# coding: utf-8
"""
This module contains constants.
"""
from __future__ import absolute_import


# Hotkey types.
#
# Hotkey type: key-down
HOTKEY_TYPE_V_DN = 'dn'

# Hotkey type: key-up
HOTKEY_TYPE_V_UP = 'up'

# Hotkey type: key-sequence
HOTKEY_TYPE_V_KS = 'ks'

# Hotkey type set
HOTKEY_TYPES = {
    HOTKEY_TYPE_V_DN,
    HOTKEY_TYPE_V_UP,
    HOTKEY_TYPE_V_KS,
}


# Hotkey info keys.
#
# Hotkey type
HOTKEY_INFO_K_HOTKEY_TYPE = 'hotkey_type'

# Hotkey pattern
HOTKEY_INFO_K_HOTKEY_PATTERN = 'hotkey_pattern'

# Hotkey function
HOTKEY_INFO_K_HOTKEY_FUNC = 'hotkey_func'

# Hotkey's virtual key tuples
HOTKEY_INFO_K_HOTKEY_TUPLES = 'hotkey_tuples'

# Hotkey's original spec
HOTKEY_INFO_K_HOTKEY_ORIG_SPEC = 'hotkey_orig_spec'

# List of hotkey functions that are NeedHotkeyInfo instances
HOTKEY_INFO_K_NEED_HOTKEY_INFO_LIST = 'need_hotkey_info_list'


# Event masks.
#
# Event mask for none
EMASK_V_NONE = 0

# Event mask for event functions
EMASK_V_EFUNC = 1

# Event mask for hotkey events
EMASK_V_HOTKEY = 2

# Event mask for key-sequence events
EMASK_V_HOTSEQ = 4

# Event mask for all
EMASK_V_ALL = \
    EMASK_V_EFUNC \
    | EMASK_V_HOTKEY \
    | EMASK_V_HOTSEQ


class SpecReloadExc(Exception):
    """
    Exception raised to inform upper context to reload hotkey spec.
    """


# Special spec IDs.
# Use tuple to avoid clashing with custom spec ids specified by user.
#
# Special spec ID for previous spec
SPEC_SWITCH_V_PREV = ('prev',)

# Special spec ID for next spec
SPEC_SWITCH_V_NEXT = ('next',)

# Special spec ID for first spec
SPEC_SWITCH_V_FIRST = ('first',)

# Special spec ID for last spec
SPEC_SWITCH_V_LAST = ('last',)


class SpecSwitchExc(Exception):
    """
    Exception raised to inform upper context to switch hotkey spec.
    """

    def __init__(self, spec_id):
        """
        Constructor.

        :param spec_id: Hotkey spec ID.

        :return: None.
        """
        # Store given hotkey spec ID.
        self.spec_id = spec_id
