#!/usr/bin/env bash

# Set quit on error
set -e

# If this file path is absolute path
if [[ "$BASH_SOURCE" == /* ]]; then
    # Use the absolute path as file path
    file_path="$BASH_SOURCE"

# If this file path is not absolute path
else
    # Combine working directory path with the relative path as file path
    file_path="$(pwd)/$BASH_SOURCE"
fi

# Get project top directory path from the file path
# E.g. ``{top_path}/tools/pyenv/setup.sh`` -> ``{top_path}``
top_path="$(dirname "$(dirname "$(dirname "$file_path")")")"

# Get build directory path
build_dir="$top_path/build_pyenv"

# If environment variable PYENV_ROOT is not empty
if [ -n "${PYENV_ROOT}" ]; then
    # Use environment variable PYENV_ROOT's value as pyenv root directory
    pyenv_root="${PYENV_ROOT}"

# If environment variable PYENV_ROOT is empty
else
    # Put pyenv root directory inside the build directory
    pyenv_root="$build_dir/root"
fi

# Print title
echo -e "\n# ----- Create build directory: $build_dir -----"

# Create build directory
mkdir -p -v "$build_dir"

# Print end title
echo "# ===== Create build directory: $build_dir ====="

# Print title
echo -e "\n# ----- Change directory to: $build_dir -----"

# Change directory to build directory
cd "$build_dir"

# Print end title
echo "# ===== Change directory to: $build_dir ====="

# Print title
echo -e "\n# ----- Remove existing pyenv root directory: $pyenv_root -----"

# Remove existing pyenv root directory if any
rm -rf "$pyenv_root"

# Print end title
echo "# ===== Remove existing pyenv root directory: $pyenv_root ====="

# Print title
echo -e "\n# ----- Download setup file -----"

# If command `curl` is available
if command -v "curl" >/dev/null 2>&1; then
    # Download setup file using `curl`
    curl -L -o pyenv-master.zip https://github.com/yyuu/pyenv/archive/master.zip

    # Unzip the setup file
    unzip pyenv-master.zip >/dev/null

    # Move the unzipped directory to the pyenv root directory path
    mv pyenv-master "$pyenv_root"

# If command `curl` is not available.

# If command `wget` is available
elif command -v "wget" >/dev/null 2>&1; then
    # Download setup file using `wget`
    wget -O pyenv-master.zip https://github.com/yyuu/pyenv/archive/master.zip

    # Unzip the setup file
    unzip pyenv-master.zip >/dev/null

    # Move the unzipped directory to the pyenv root directory path
    mv pyenv-master "$pyenv_root"

# If command `wget` is not available.

# If command `git` is available
elif command -v "git" >/dev/null 2>&1; then
    # Clone pyenv's repository to the pyenv root directory path
    git clone git://github.com/yyuu/pyenv.git "$pyenv_root"

# If command `git` is not available.

# If commands `curl`, `wget`, and `git` are not available.
else
    # Print info
    echo 'Error: Please set up `curl`, `wget`, or `git` for downloading setup file.'

    # Print end title
    echo "# ===== Download setup file ====="

    # Exit with error code
    exit 1
fi

# Print end title
echo "# ===== Download setup file ====="

# Print title
echo -e "\n# ----- Done -----"

# Print info
echo "Pyenv root directory: $pyenv_root"

# Print end title
echo "# ===== Done ====="
