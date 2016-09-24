# coding: utf-8
"""
This mediator module puts together other modules to implement the program.
"""
from __future__ import absolute_import

# Standard imports
import sys
from traceback import format_exc

# External imports
from aoikimportutil import load_obj_local_or_remote
from aoikimportutil import uri_split

# Local imports
from .const import SPEC_SWITCH_V_FIRST
from .const import SPEC_SWITCH_V_LAST
from .const import SPEC_SWITCH_V_NEXT
from .const import SPEC_SWITCH_V_PREV
from .const import SpecReloadExc
from .const import SpecSwitchExc
from .hotkey_manager import HotkeyManager
from .hotkey_parser import hotkey_parse as recovery_mode_hotkey_parse
from .hotkey_spec_parser import spec_parse as recovery_mode_spec_parse
from .mediator_argpsr import ARG_DBG_MSG_K
from .mediator_argpsr import ARG_HOTKEY_PARSE_URI_K
from .mediator_argpsr import ARG_HOTKEY_TFUNC_URI_K
from .mediator_argpsr import ARG_SPEC_ID_K
from .mediator_argpsr import ARG_SPEC_PARSE_URI_K
from .mediator_argpsr import ARG_SPEC_URI_F
from .mediator_argpsr import ARG_SPEC_URI_K
from .mediator_argpsr import ARG_VER_ON_K
from .mediator_argpsr import ARG_VK_CTN_URI_K
from .mediator_argpsr import create_arguments_parser
from .runtime import hotkey_manager_set
from .util.cmd import Quit
from .util.cmd import SpecReload
from .util.cmd import SpecSwitch
from .version import __version__


try:
    # Python 2
    input = raw_input
except NameError:
    # Python 3
    pass


# Exit codes.
# Notice 1 and 2 are used by `argparse`.
#
# Exit code: No error
MAIN_RET_V_OK = 0

# Exit code: Exception leak
MAIN_RET_V_EXC_LEAK_ERR = 3

# Exit code: Hotkey spec is not given
MAIN_RET_V_SPEC_URI_ZERO_ERR = 4

# Exit code: Hotkey spec IDs count is GT spec URIs count
MAIN_RET_V_SPEC_ID_EXCEED_ERR = 5

# Exit code: Hotkey spec IDs contain duplicate
MAIN_RET_V_SPEC_ID_DUPLICATE_ERR = 6


# Dynamically-loaded module names.
#
# Hotkey spec dynamically-loaded module name
_HOTKEY_SPEC_DYN_MOD_NAME = 'aoikhotkey._spec_dyn'

# Hotkey spec parse function dynamically-loaded module name
_HOTKEY_SPEC_PARSE_DYN_MOD_NAME = 'aoikhotkey._hotkey_spec_parse_dyn'

# Hotkey parse function dynamically-loaded module name
_HOTKEY_PARSE_DYN_MOD_NAME = 'aoikhotkey._hotkey_parse_dyn'

# Hotkey trigger function dynamically-loaded module name
_HOTKEY_TFUNC_DYN_MOD_NAME = 'aoikhotkey._hotkey_tfunc_dyn'

# Virtual key code-to-name dynamically-loaded module name
_VK_CTN_DYN_MOD_NAME = 'aoikhotkey._vk_ctn_dyn'


def main_inner(args=None):
    """
    Main function's inner function.

    :param args: Argument list. Default is use `sys.argv[1:]`.

    :return: Exit code.
    """
    # Create arguments parser
    parser = create_arguments_parser()

    # If arguments are not given
    if args is None:
        # Use command line arguments
        args = sys.argv[1:]

    # Parse the arguments
    args_obj = parser.parse_args(args)

    # Get whether debug message is enabled
    dbg_msg_on = getattr(args_obj, ARG_DBG_MSG_K)

    # If the argument is EQ '0'
    if dbg_msg_on == '0':
        # Set debug message be disabled
        dbg_msg_on = False
    else:
        # Set debug message be enabled
        dbg_msg_on = True

    # Get whether show version
    ver_on = getattr(args_obj, ARG_VER_ON_K)

    # If need show version
    if ver_on:
        # Print version
        print(__version__)

        # Return exit code
        return MAIN_RET_V_OK

    # If not need show version.

    # Get hotkey spec URIs
    spec_uri_s = getattr(args_obj, ARG_SPEC_URI_K)

    # If hotkey spec URIs are not given
    if not spec_uri_s:
        # Get error message
        msg = (
            '# Error\n'
            'No hotkey spec is given.\n'
            'Please specify at least one using option {option}.\n'
        ).format(option=ARG_SPEC_URI_F)

        # Print error message
        sys.stderr.write(msg)

        # Return exit code
        return MAIN_RET_V_SPEC_URI_ZERO_ERR

    # If hotkey spec URIs are given.

    # Ensure spec URIs are given.
    assert len(spec_uri_s) > 0

    # Get max spec index
    spec_uri_idx_max = len(spec_uri_s) - 1

    # Ensure max spec index is GE 0
    assert spec_uri_idx_max >= 0

    # Get spec IDs
    spec_id_s = getattr(args_obj, ARG_SPEC_ID_K)

    # Get spec IDs count
    spec_id_s_len = len(spec_id_s)

    # Get spec URIs count
    spec_uri_s_len = len(spec_uri_s)

    # If spec IDs count is GT spec URIs count
    if spec_id_s_len > spec_uri_s_len:
        # Get error message
        msg = (
            '# Error\n'
            '{} ids specified for {} spec{}.\n'
        ).format(
            spec_id_s_len,
            spec_uri_s_len,
            's' if spec_uri_s_len > 1 else '',
        )

        # Print error message
        sys.stderr.write(msg)

        # Return exit code
        return MAIN_RET_V_SPEC_ID_EXCEED_ERR

    # If spec IDs count is not GT spec URIs count.

    # Ensure spec IDs count is LE spec URIs count
    assert spec_id_s_len <= spec_uri_s_len

    # Create map from spec ID to spec index
    map_spec_id_to_spec_idx = \
        dict((spec_id, spec_idx) for spec_idx, spec_id in enumerate(spec_id_s))

    # If the map length is not EQ the spec IDs count
    if len(map_spec_id_to_spec_idx) != spec_id_s_len:
        # Get error message
        msg = 'Error: Duplicates exist in spec IDs.\n'

        # Print error message
        sys.stderr.write(msg)

        # Return exit code
        return MAIN_RET_V_SPEC_ID_DUPLICATE_ERR

    # Whether is recovery mode
    is_recovery_mode = False

    # Recovery mode's hotkey spec list
    recovery_specs = [
        ('^q', Quit),
        ('^r', SpecReload),
        ('^[', SpecSwitch(SPEC_SWITCH_V_PREV)),
        ('^]', SpecSwitch(SPEC_SWITCH_V_NEXT)),
    ]

    # Current spec URI index
    spec_uri_idx = 0

    # Hotkey manager
    hotkey_manager = None

    #
    def sys_use_decide(uri, mod_uri_s_reloaded):
        """
        Decide whether use existing module or reload module for given URI.

        :param uri: Object URI.

        :param mod_uri_s_reloaded: List of module URIs that have been reloaded.

        :return: Whether use existing module.
        """
        # Get module URI from given object URI
        _, mod_uri, _ = uri_split(uri)

        # If the module URI starts with `aoikhotkey.`
        if mod_uri.startswith('aoikhotkey.'):
            # Set use existing module be True
            sys_use = True

        # If the module URI exists in the reloaded list
        elif mod_uri in mod_uri_s_reloaded:
            # Set use existing module be True
            sys_use = True

        # If the module URI not exists in the reloaded list
        else:
            # Set use existing module be False
            sys_use = False

            # Add the module URI to the reloaded list
            mod_uri_s_reloaded.append(mod_uri)

        # Return whether use existing module
        return sys_use

    # Loop until quit
    while True:
        # List of module URIs that have been reloaded
        mod_uri_s_reloaded = []

        # Hotkey parse function
        hotkey_parse = None

        # Hotkey parse function's module
        hotkey_parse_mod = None

        # Hotkey trigger function
        hotkey_tfunc = None

        # Hotkey trigger function's module
        hotkey_tfunc_mod = None

        # Virtual key code-to-name function
        vk_ctn = None

        # Virtual key code-to-name function's module
        vk_ctn_mod = None

        # If is recovery mode
        if is_recovery_mode:
            # Loop until the user enters a valid choice.
            # This loop aims to prevent endless loops when an internal function
            # like `recovery_mode_hotkey_parse` has bug.
            while True:
                # Get user input
                user_input = input(
                    'Enter r to enter recovery mode, q to quit: '
                )

                # Strip white-spaces
                user_input = user_input.strip()

                # If user input is `q`
                if user_input == 'q':
                    # Return exit code
                    return MAIN_RET_V_OK

                # If user input is `r`
                elif user_input == 'r':
                    # Break the loop to enter recovery mode
                    break

                # If user input is not `q` or `r`
                else:
                    # Continue the loop
                    continue

            # Use default hotkey parse function for recovery mode
            hotkey_parse = recovery_mode_hotkey_parse

        # If is not recovery mode
        else:
            # Get hotkey parse function URI
            hotkey_parse_uri = getattr(args_obj, ARG_HOTKEY_PARSE_URI_K)

            try:
                # 2MNIE
                # Load hotkey parse function.
                #
                # `sys_use=False` forces reloading the module, instead of using
                # what's already in `sys.modules`.
                #
                # `sys_add=False` avoids overriding an existing module.
                #
                # `retn_mod=True` keeps the module object from being GC-ed.
                hotkey_parse_mod, hotkey_parse = load_obj_local_or_remote(
                    hotkey_parse_uri,
                    mod_name=_HOTKEY_PARSE_DYN_MOD_NAME,
                    sys_use=sys_use_decide(
                        hotkey_parse_uri, mod_uri_s_reloaded
                    ),
                    sys_add=False,
                    retn_mod=True,
                )

            # If have error
            except Exception:
                # Get error message
                msg = (
                    '# Error\n'
                    'Failed loading hotkey parse function.\n'
                    'URI: {func_uri}.\n'
                ).format(func_uri=hotkey_parse_uri)

                # Print error message
                sys.stderr.write(msg)

                # If debug is enabled
                if dbg_msg_on:
                    # Get traceback message
                    tb_msg = format_exc()

                    # Print traceback message
                    sys.stderr.write('---\n{}---\n'.format(tb_msg))

                # Set recovery mode be True
                is_recovery_mode = True

                # Continue the loop
                continue

            # Get hotkey trigger function URI
            hotkey_tfunc_uri = getattr(args_obj, ARG_HOTKEY_TFUNC_URI_K)

            try:
                # Load hotkey trigger function.
                #
                # `sys_use`, `sys_add`, and `retn_mod` are explained at 2MNIE.
                hotkey_tfunc_mod, hotkey_tfunc = load_obj_local_or_remote(
                    hotkey_tfunc_uri,
                    mod_name=_HOTKEY_TFUNC_DYN_MOD_NAME,
                    sys_use=sys_use_decide(
                        hotkey_tfunc_uri, mod_uri_s_reloaded
                    ),
                    sys_add=False,
                    retn_mod=True,
                )

            # If have error
            except Exception:
                # Get error message
                msg = (
                    '# Error\n'
                    'Failed loading hotkey trigger function.\n'
                    'URI: {func_uri}.\n'
                ).format(func_uri=hotkey_tfunc_uri)

                # Print error message
                sys.stderr.write(msg)

                # If debug is enabled
                if dbg_msg_on:
                    # Get traceback message
                    tb_msg = format_exc()

                    # Print traceback message
                    sys.stderr.write('---\n{}---\n'.format(tb_msg))

                # Set recovery mode be True
                is_recovery_mode = True

                # Continue the loop
                continue

            # Get virtual key code-to-name function URI
            vk_ctn_uri = getattr(args_obj, ARG_VK_CTN_URI_K)

            try:
                # Load virtual key code-to-name function.
                #
                # `sys_use`, `sys_add`, and `retn_mod` are explained at 2MNIE.
                vk_ctn_mod, vk_ctn = load_obj_local_or_remote(
                    vk_ctn_uri,
                    mod_name=_VK_CTN_DYN_MOD_NAME,
                    sys_use=sys_use_decide(
                        vk_ctn_uri, mod_uri_s_reloaded
                    ),
                    sys_add=False,
                    retn_mod=True,
                )

            # If have error
            except Exception:
                # Get error message
                msg = (
                    '# Error\n'
                    'Failed loading virtual key code-to-name function.\n'
                    'URI: {func_uri}.\n'
                ).format(func_uri=vk_ctn_uri)

                # Print error message
                sys.stderr.write(msg)

                # If debug is enabled
                if dbg_msg_on:
                    # Get traceback message
                    tb_msg = format_exc()

                    # Print traceback message
                    sys.stderr.write('---\n{}---\n'.format(tb_msg))

                # Set recovery mode be True
                is_recovery_mode = True

                # Continue the loop
                continue

        # Create hotkey manager
        hotkey_manager = HotkeyManager(
            hotkey_parse=hotkey_parse,
            hotkey_tfunc=hotkey_tfunc,
            vk_ctn=vk_ctn,
        )

        # 2STYZ
        # Set hotkey manager to the runtime module
        hotkey_manager_set(hotkey_manager)

        # If is recovery mode
        if is_recovery_mode:
            # Use default spec parse function
            spec_parse = recovery_mode_spec_parse

            # Use default spec list
            spec = recovery_specs

        # If is not recovery mode
        else:
            # Get hotkey spec parse function URI
            spec_parse_uri = getattr(args_obj, ARG_SPEC_PARSE_URI_K)

            try:
                # Load hotkey spec parse function.
                #
                # `sys_use`, `sys_add`, and `retn_mod` are explained at 2MNIE.
                spec_parse_mod, spec_parse = load_obj_local_or_remote(
                    spec_parse_uri,
                    mod_name=_HOTKEY_SPEC_PARSE_DYN_MOD_NAME,
                    sys_use=sys_use_decide(
                        spec_parse_uri, mod_uri_s_reloaded
                    ),
                    sys_add=False,
                    retn_mod=True,
                )

            # If have error
            except Exception:
                # Get error message
                msg = (
                    '# Error\n'
                    'Failed loading hotkey spec parse function.\n'
                    'URI: {func_uri}.\n'
                ).format(func_uri=spec_parse_uri)

                # Print error message
                sys.stderr.write(msg)

                # If debug is enabled
                if dbg_msg_on:
                    # Get traceback message
                    tb_msg = format_exc()

                    # Print traceback message
                    sys.stderr.write('---\n{}---\n'.format(tb_msg))

                # Set recovery mode be True
                is_recovery_mode = True

                # Continue the loop
                continue

            # Get spec URI
            spec_uri = spec_uri_s[spec_uri_idx]

            try:
                # Get spec ID
                spec_id = spec_id_s[spec_uri_idx]

            # If have error
            except IndexError:
                # Use spec URI index plus 1 as spec ID for display below
                spec_id = str(spec_uri_idx + 1)

            # Get message
            msg = '# Use spec {spec_id}\nURI: {spec_uri}\n\n'\
                .format(spec_id=repr(spec_id), spec_uri=spec_uri)

            # Print message
            sys.stderr.write(msg)

            try:
                # Load hotkey spec list.
                #
                # Hotkey spec list must be loaded only after the hotkey manager
                # is initialized at 2STYZ, because spec items may access the
                # hotkey manager when loaded.
                #
                # `sys_use`, `sys_add`, and `retn_mod` are explained at 2MNIE.
                spec_mod, spec = load_obj_local_or_remote(
                    spec_uri,
                    mod_name=_HOTKEY_SPEC_DYN_MOD_NAME,
                    sys_use=sys_use_decide(
                        spec_uri, mod_uri_s_reloaded
                    ),
                    sys_add=False,
                    retn_mod=True,
                )

            # If have error
            except Exception:
                # Get error message
                msg = (
                    '# Error\n'
                    'Failed loading hotkey spec.\n'
                    'URI: {spec_uri}.\n'
                ).format(spec_uri=spec_uri)

                # Print error message
                sys.stderr.write(msg)

                # If debug is enabled
                if dbg_msg_on:
                    # Get traceback message
                    tb_msg = format_exc()

                    # Print traceback message
                    sys.stderr.write('---\n{}---\n'.format(tb_msg))

                # Set recovery mode be True
                is_recovery_mode = True

                # Continue the loop
                continue

        #
        try:
            # Parse hotkey spec list to hotkey info list
            hotkey_info_s = spec_parse(spec)

            # For the hotkey info list's each hotkey info
            for hotkey_info in hotkey_info_s:
                # Add the hotkey info to the hotkey manager
                hotkey_manager.hotkey_add(hotkey_info)

        # If have error
        except Exception:
            # Get error message
            msg = (
                '# Error\n'
                'Failed parsing hotkey spec.\n'
                'URI: {spec_uri}.\n'
            ).format(spec_uri=spec_uri)

            # Print error message
            sys.stderr.write(msg)

            # If debug is enabled
            if dbg_msg_on:
                # Get traceback message
                tb_msg = format_exc()

                # Print traceback message
                sys.stderr.write('---\n{}---\n'.format(tb_msg))

            # Set recovery mode be True
            is_recovery_mode = True

            # Continue the loop
            continue

        # If is recovery mode
        if is_recovery_mode:
            # Get message
            msg = (
                '\n'
                '# Recovery mode\n'
                'Ctrl q: Quit the program.\n'
                'Ctrl r: Reload the current spec.\n'
                'Ctrl [: Switch to previous spec.\n'
                'Ctrl ]: Switch to next spec.\n'
                '\n'
            )

            # Print message
            sys.stderr.write(msg)

            # Set recovery mode be False
            is_recovery_mode = False

        #
        try:
            # Run the hotkey manager's event loop.
            # This method will not return until the event loop is stopped, or
            # an exception is raised.
            hotkey_manager.eloop_start()

            # Return exit code
            return MAIN_RET_V_OK

        # If have `SpecReloadExc`,
        # this means to reload hotkey spec.
        except SpecReloadExc:
            # Continue the loop
            continue

        # If have `SpecSwitchExc`,
        # this means to switch hotkey spec.
        except SpecSwitchExc as e:
            # Get hotkey spec ID
            spec_id = e.spec_id

            # Get error message
            error_msg = '# Invalid hotkey spec ID: {0}\n\n'\
                .format(repr(spec_id))

            # If the spec ID is special value `first`
            if spec_id == SPEC_SWITCH_V_FIRST:
                # Set spec URI index be 0
                spec_uri_idx = 0

                # Ensure the spec URI index is valid
                assert 0 <= spec_uri_idx <= spec_uri_idx_max

                # Continue the loop
                continue

            # If the spec ID is special value `last`
            elif spec_id == SPEC_SWITCH_V_LAST:
                # Set spec URI index be max index
                spec_uri_idx = spec_uri_idx_max

                # Ensure the spec URI index is valid
                assert 0 <= spec_uri_idx <= spec_uri_idx_max

                # Continue the loop
                continue

            # If the spec ID is special value `previous`
            elif spec_id == SPEC_SWITCH_V_PREV:
                # Decrement the spec URI index
                spec_uri_idx -= 1

                # If the spec URI index is LT 0
                if spec_uri_idx < 0:
                    # Set spec URI index be max index
                    spec_uri_idx = spec_uri_idx_max

                # Ensure the spec URI index is valid
                assert 0 <= spec_uri_idx <= spec_uri_idx_max

                # Continue the loop
                continue

            # If the spec ID is special value `next`
            elif spec_id == SPEC_SWITCH_V_NEXT:
                # Increment the spec URI index
                spec_uri_idx += 1

                # If the spec URI index is GT 0
                if spec_uri_idx > spec_uri_idx_max:
                    # Set spec URI index be 0
                    spec_uri_idx = 0

                # Ensure the spec URI index is valid
                assert 0 <= spec_uri_idx <= spec_uri_idx_max

                # Continue the loop
                continue

            # If the spec ID is integer,
            # it means it is spec index.
            elif isinstance(spec_id, int):
                # If the spec index is not valid
                if not (0 <= spec_id <= spec_uri_idx_max):
                    # Print error message
                    sys.stderr.write(error_msg)

                    # Use the current spec URI index
                    spec_uri_idx = spec_uri_idx

                # If the spec index is valid
                else:
                    # Use the new spec index
                    spec_uri_idx = spec_id

                # Ensure the spec URI index is valid
                assert 0 <= spec_uri_idx <= spec_uri_idx_max

                # Continue the loop
                continue

            # If the spec ID is string,
            # it means it is spec ID.
            elif isinstance(spec_id, str):
                # Map the spec ID to spec index
                idx_new = map_spec_id_to_spec_idx.get(spec_id, None)

                # If the spec index is not found
                if idx_new is None:
                    # Print error message
                    sys.stderr.write(error_msg)

                    # Use the current spec URI index
                    spec_uri_idx = spec_uri_idx

                # If the spec index is found
                else:
                    # Use the new spec index
                    spec_uri_idx = idx_new

                # Ensure the spec URI index is valid
                assert 0 <= spec_uri_idx <= spec_uri_idx_max

                # Continue the loop
                continue

            # If the spec ID is none of above
            else:
                # Print error message
                sys.stderr.write(error_msg)

                # Use the current spec URI index
                spec_uri_idx = spec_uri_idx

                # Ensure the spec URI index is valid
                assert 0 <= spec_uri_idx <= spec_uri_idx_max

                # Continue the loop
                continue

        # If have error
        except Exception:
            # Get traceback message
            tb_msg = format_exc()

            # Print traceback message
            sys.stderr.write('# Error\n---\n{}---\n'.format(tb_msg))

            # Set recovery mode be True
            is_recovery_mode = True

            # Continue the loop
            continue

        # Finally
        finally:
            # Set the hotkey manager be None
            hotkey_manager = None

    # Return exit code
    return MAIN_RET_V_OK


def main_wrap(args=None):
    """
    Main function's wrapper function.

    :param args: Argument list. Default is use `sys.argv[1:]`.

    :return: Exit code.
    """
    try:
        # Delegate call to `main_inner`
        return main_inner(args)

    # If have `SystemExit`
    except SystemExit:
        # Raise as-is
        raise

    # If have `KeyboardInterrupt`
    except KeyboardInterrupt:
        # Return exit code
        return MAIN_RET_V_OK

    # If have other exceptions
    except BaseException:
        # Get traceback message
        tb_msg = format_exc()

        # Print traceback message
        sys.stderr.write('# Caught exception\n---\n{0}---\n'.format(tb_msg))

        # Return exit code
        return MAIN_RET_V_EXC_LEAK_ERR
