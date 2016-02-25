# coding: utf-8
#
from functools import partial
import os.path
import sys

from aoikdyndocdsl.ext.all import nto as nto_dft
from aoikdyndocdsl.ext.markdown.heading import hd_to_key
from aoikdyndocdsl.ext.markdown.heading import hd_url
from aoikdyndocdsl.ext.var import var
from aoikdyndocdsl.ext.var import var_set
from aoikdyndocdsl.ext.var import var_set_v2


# A list of "prefix spec" items.
# Each prefix spec's format is: (_VALUE_PREFIX_, _PATH_PREFIX_).
# "_VALUE_PREFIX_" is the prefix to match with a value.
# "_PATH_PREFIX_" is the path to use if a value has matched the value prefix.
# "_PATH_PREFIX_" can be None, which will be ignored at 7JHF9.
_PREFIX_SPEC_S = [
    ('src/', './src/'),
    ('/', './'),
]


# A dictionary to cache file data read in by "_file_reader" function below.
# Item format: (_FILE_PATH_, _FILE_DATA_).
_FILE_DATA_CACHE = {}


#
def _file_reader(key, value, file_path=None, line_num=None):
    """
    @param key: key of "aoikdyndocdsl.ext.var.var_set".

    @param value: value of "aoikdyndocdsl.ext.var.var_set".

    @param file_path: the path of the file that the value is "mentioned".
    This argument is optional. If the file path is not given, methods at 2UKIL
    and 5S8D3 are used to find the file path.

    @param line_num: the number of the line in the file that the value is
    "mentioned".
    This argument is optional. If the line number is not given, method at 6SFEI
    is used to find the line number.

    @param return: a tuple of (file data, line number).
    """

    # If the file path is given
    if file_path is not None:
        # Use it
        file_path_2 = file_path
    # If the file path is not given,
    # and the value starts with "aoikhotkey." or '"aoikhotkey.'
    elif value.startswith('aoikhotkey.') \
            or value.startswith('"aoikhotkey.'):
        # 2UKIL
        # Assume the value contains a module name.
        # Convert it to a file path.

        # Strip '"'
        file_path_2 = value.strip('"')

        # Replace '.' with '/'
        file_path_2 = file_path_2.replace('.', '/')

        # Remove "function name" part
        file_path_2, _, _ = file_path_2.partition('::')

        # Add path prefix and file extension
        file_path_2 = 'src/{}.py'.format(file_path_2)
    # If the file path is not given,
    # and the value not starts with "aoikhotkey." or '"aoikhotkey.'
    else:
        # 5S8D3
        # Use "_PREFIX_SPEC_S" to convert the value to a file path

        # Whether found a file path
        found = False

        # Start to find file path
        for prefix_spec in _PREFIX_SPEC_S:
            # Unpack the prefix spec
            value_prefix, path_prefix = prefix_spec

            # If the value starts with the prefix
            if value.startswith(value_prefix):
                # 7JHF9
                # If the path prefix means to ignore
                if path_prefix is None:
                    # Set "found" to False
                    found = False

                    # Stop finding
                    break

                # Remove
                file_path_2 = value[len(value_prefix):]

                if path_prefix:
                    file_path_2 = path_prefix + file_path_2

                # Set "found" to true
                found = True

                # Stop finding
                break
            # If the value not starts with the prefix
            else:
                # Try next prefix spec
                continue

        # If a file path is not found
        if not found:
            # Message
            msg = 'File checking ignores: {} {}\n'.format(key, value)

            sys.stderr.write(msg)

            # Return a tuple of (file data, line number) as (None, None)
            return None, None

        # Ensure the file path is found at this point
        assert file_path_2

    # Ensure the file path is found at this point
    assert file_path_2

    # If line number is not given
    if line_num is None:
        # 6SFEI
        # Find the line number

        # If "#L" is in the file path
        if '#L' in file_path_2:
            #
            file_path_2, sep, line_num = file_path_2.rpartition('#L')

            # If the partition separator "#L" is not found
            if not sep:
                # Keep it None.
                # Let the caller handle the "no line number" case.
                line_num = None
            else:
                # Convert the line number text to int
                line_num = int(line_num)

    # Convert the file path to absolute path
    file_path_2 = os.path.abspath(file_path_2)

    # Normalize the file path
    file_path_2 = os.path.normpath(file_path_2)

    # Get the file data from cache
    file_data = _FILE_DATA_CACHE.get(file_path_2, None)

    # If the file data is not available in cache
    if file_data is None:
        # Open the file
        file_obj = open(file_path_2)

        # Read the file data
        file_data = file_obj.read()

        # Cache the file data
        _FILE_DATA_CACHE[file_path_2] = file_data

    # Ensure file data is read
    assert file_data is not None

    # Return a tuple of (file data, line number)
    return file_data, line_num

# 6KCP2
# Create short names
v = var

vs = var_set

vs2 = partial(var_set_v2, file_reader=_file_reader)

hk = hd_to_key

h = hd_url


#
def nto(name):
    """
    Name-to-object function to be used by AoikDynDocDSL's parser.

    @param name: name to be mapped to object.

    @param return: the object for the name.
    """
    # Map the name using one of the short names at 6KCP2
    obj = globals().get(name, None)

    # If found an object
    if obj is not None:
        # Use it
        obj = obj
    else:
        # Delegate to the default name-to-object function
        obj = nto_dft(name)

    # Return the object for the name
    return obj
