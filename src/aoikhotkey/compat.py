# coding: utf-8
"""
This module contains compatibility utility.
"""
from __future__ import absolute_import

# Standard imports
import sys


# Whether the platform is Linux
IS_LINUX = sys.platform.startswith('linux')

# Whether the platform is MacOS
IS_MACOS = sys.platform.startswith('darwin')

# Whether the platform is Windows
IS_WINOS = sys.platform.startswith('win')

# Error to raise for an unsupported platform
UNSUPPORTED_PLATFORM_ERROR = ValueError(
    'Unsupported platform: {}.'.format(repr(sys.platform))
)
