# Pyenv setup
```
# Set project top directory variable
PROJECT_DIR=~/aoikprojectstarter

# Set up dependency packages required for compiling Python
sudo bash "$PROJECT_DIR/tools/pyenv/setup_deps.sh"

# Use PYENV_ROOT to specify where is `pyenv`'s root directory
export PYENV_ROOT=~/pyenv

# Set up `pyenv` in the directory specified in PYENV_ROOT
bash "$PROJECT_DIR/tools/pyenv/setup.sh"

# Add `pyenv` bin directory to PATH.
# This makes command `pyenv` available in the shell.
export PATH="$PYENV_ROOT/bin:$PATH"

# Initialize `pyenv`.
# This makes `pyenv`'s `python` shim command available in the shell.
#
# Notice `PYENV_ROOT` must be properly set otherwise `pyenv` plugins will not
# be loaded correctly, leading to errors like "no such command `install'" when
# running `pyenv install` below.
eval "$(pyenv init -)"

# Install Python version
pyenv install 3.5.1

# Use PYENV_VERSION to specify the Python version to use
export PYENV_VERSION=3.5.1

# Switch to the Python version specified in PYENV_VERSION
pyenv shell

# Show current Python version
pyenv version

# Show available Python versions
pyenv versions

# Add these lines to `~/.bashrc` to be run at every login
export PYENV_ROOT=~/pyenv
export PATH="$PYENV_ROOT/bin:$PATH"
export PYENV_VERSION=3.5.1
eval "$(pyenv init -)"
```
