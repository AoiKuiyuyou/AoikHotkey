# coding: utf-8
"""
This module is the program's main module.

This module is named ``__main__.py`` so that the program can be run via:
::

    python -m aoikhotkey
"""
from __future__ import absolute_import

# Standard imports
import os.path
import struct
import sys


def get_pyhook_dir_name():
    """
    Get pyHook directory name according to current Python version.

    E.g.
        - pyHook-py2.7-32bit
        - pyHook-py2.7-64bit
        - pyHook-py3.5-32bit
        - pyHook-py3.5-64bit

    :return: pyHook directory name.
    """
    # Get prefix part, e.g. `pyHook-py2.7`
    prefix = 'pyHook-py{0}.{1}'.format(
        sys.version_info[0],
        sys.version_info[1],
    )

    # Get integer width, e.g. 32 or 64
    int_width = struct.calcsize('P') * 8

    # If the integer width is 32
    if int_width == 32:
        # Get postfix part
        postfix = '-32bit'

    # If the integer width is 64
    elif int_width == 64:
        # Get postfix part
        postfix = '-64bit'

    # If the integer width is not 32 or 64
    else:
        # Get error message
        msg = 'Error: Unsupported integer width: {0}.'.format(int_width)

        # Raise error
        raise ValueError(msg)

    # Combine prefix and postfix parts to form the directory name
    dir_name = prefix + postfix

    # Return the directory name
    return dir_name


def syspath_init():
    """
    Prepare `sys.path` for import resolution.

    :return: None.
    """
    # Get this file's directory path
    my_dir = os.path.dirname(os.path.abspath(__file__))

    # Remove some paths from `sys.path` to avoid unexpected import resolution.
    #
    # For each path in the list.
    for path in ['', '.', my_dir]:
        # If the path is in `sys.path`
        if path in sys.path:
            # Remove the path from `sys.path`
            sys.path.remove(path)

    # Get `src` directory path
    src_dir = os.path.dirname(my_dir)

    # Get `aoikhotkeydep` directory path
    dep_dir = os.path.join(src_dir, 'aoikhotkeydep')

    # Assert the directory path exists
    assert os.path.isdir(dep_dir), dep_dir

    # If `aoikhotkeydep` directory path is not in `sys.path`
    if dep_dir not in sys.path:
        # Prepend the directory path to `sys.path`
        sys.path.insert(0, dep_dir)

    # If the platform is Windows or Cygwin
    if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
        # Get `pyHook` directory name according to current Python version
        pyhook_dir_name = get_pyhook_dir_name()

        # If the platform is Cygwin
        if sys.platform.startswith('cygwin'):
            # Add postfix
            pyhook_dir_name += '-cygwin'

        # Get `pyHook` directory path
        pyhook_dir = os.path.join(dep_dir, 'pyHook_versions', pyhook_dir_name)

        # If the `pyHook` directory path is not existing
        if not os.path.isdir(pyhook_dir):
            # Get error message
            msg = (
                'Error: `pyHook` directory for this Python version is'
                ' not found:\n{0}\n'
            ).format(pyhook_dir)

            # Print error message
            sys.stderr.write(msg)

            # Exit
            sys.exit(9)

        # If `pyHook` directory path is not in `sys.path`
        if pyhook_dir not in sys.path:
            # Prepend the directory path to `sys.path`
            sys.path.insert(0, pyhook_dir)

    # If `src` directory path is not in `sys.path`
    if src_dir not in sys.path:
        # Prepend the directory path to `sys.path`
        sys.path.insert(0, src_dir)


def check_deps():
    """
    Check whether dependency packages have been installed.

    :return: Error message for missing dependency, otherwise None.
    """
    # If the platform is MacOS
    if sys.platform.startswith('darwin'):
        try:
            # Import dependency module
            import AppKit

            # Suppress linter error
            id(AppKit)

        # If the dependency module is not found
        except ImportError:
            # Get error message
            msg = (
                'Error: Package `pyobjc` is not installed. Try:\n'
                'pip install pyobjc\n'
            )

            # Return error message
            return msg

    # If the platform is Linux
    if sys.platform.startswith('linux'):
        try:
            # Import dependency module
            import Xlib

            # Suppress linter error
            id(Xlib)

        # If the dependency module is not found
        except ImportError:
            # Get error message
            msg = (
                'Error: Package `python-xlib` is not installed. Try:\n'
                'pip install python-xlib\n'
            )

            # Return error message
            return msg

    # If the platform is Windows or Cygwin
    if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
        try:
            # Import dependency module
            try:
                import PyHook3

                # Suppress linter error
                id(PyHook3)
            except ImportError:
                import pyHook

                # Suppress linter error
                id(pyHook)

        # If the dependency module is not found
        except ImportError:
            # Get error message
            msg = (
                'Error: Package `PyHook3` or `pyHook` is not installed. Try:\n'
                'pip install PyHook3\n'
            )

            # Return error message
            return msg

    # Return None to mean no missing dependency
    return None


def main(args=None):
    """
    Main function that is the program entry point.

    This function does three things:

    - Prepares `sys.path` so that program users do not need set up PYTHONPATH.

    - Checks whether dependency packages have been installed.

    - Delegates call to :paramref:`aoikhotkey.mediator.main_wrap`.

    :param args: Argument list. Default is use `sys.argv[1:]`.

    :return: Exit code.
    """
    # Prepare `sys.path` for import resolution
    syspath_init()

    # Print title
    print('----- sys.path -----')

    # Print paths in `sys.path`
    print('\n'.join(sys.path))

    # Print title
    print('===== sys.path =====')

    # Check whether dependency packages are installed
    error_msg = check_deps()

    # If have error message for missing dependency
    if error_msg is not None:
        # Print error message
        sys.stderr.write(error_msg)

        # Return exit code
        return 8

    # If not have error message for missing dependency.

    # Import `main_wrap` function
    from aoikhotkey.mediator import main_wrap

    # Delegate call to `main_wrap` function
    return main_wrap(args=args)


# If this module is the main module
if __name__ == '__main__':
    # Call `main` function
    sys.exit(main())
