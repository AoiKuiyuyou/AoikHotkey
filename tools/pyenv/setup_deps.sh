#!/usr/bin/env bash

# Set quit on error
set -e

# If command `apt-get` is available
if command -v "apt-get" >/dev/null 2>&1; then
    # Use `apt-get` to set up dependency packages.

    # Print title
    echo -e "\n# ----- Set up \`libssl-dev\` -----"

    # Set up the package
    apt-get install -y libssl-dev

    # Print end title
    echo "# ===== Set up \`libssl-dev\` ====="

    # Print title
    echo -e "\n# ----- Set up \`libbz2-dev\` -----"

    # Set up the package
    apt-get install -y libbz2-dev

    # Print end title
    echo "# ===== Set up \`libbz2-dev\` ====="

    # Print title
    echo -e "\n# ----- Set up \`zlib1g-dev\` -----"

    # Set up the package
    apt-get install -y zlib1g-dev

    # Print end title
    echo "# ===== Set up \`zlib1g-dev\` ====="

    # Print title
    echo -e "\n# ----- Set up \`libncurses5-dev\` -----"

    # Set up the package
    apt-get install -y libncurses5-dev

    # Print end title
    echo "# ===== Set up \`libncurses5-dev\` ====="

    # Print title
    echo -e "\n# ----- Set up \`libreadline6-dev\` -----"

    # Set up the package
    apt-get install -y libreadline6-dev

    # Print end title
    echo "# ===== Set up \`libreadline6-dev\` ====="

    # Print title
    echo -e "\n# ----- Set up \`libsqlite3-dev\` -----"

    # Set up the package
    apt-get install -y libsqlite3-dev

    # Print end title
    echo "# ===== Set up \`libsqlite3-dev\` ====="

# If command `apt-get` is not available.

# If command `yum` is available
elif command -v "yum" >/dev/null 2>&1; then
    # Use `yum` to set up dependency packages.

    # Print title
    echo -e "\n# ----- Set up \`openssl-devel\` -----"

    # Set up the package
    yum install -y openssl-devel

    # Print end title
    echo "# ===== Set up \`openssl-devel\` ====="

    # Print title
    echo -e "\n# ----- Set up \`bzip2-devel\` -----"

    # Set up the package
    yum install -y bzip2-devel

    # Print end title
    echo "# ===== Set up \`bzip2-devel\` ====="

    # Print title
    echo -e "\n# ----- Set up \`zlib-devel\` -----"

    # Set up the package
    yum install -y zlib-devel

    # Print end title
    echo "# ===== Set up \`zlib-devel\` ====="

    # Print title
    echo -e "\n# ----- Set up \`readline-devel\` -----"

    # Set up the package
    yum install -y readline-devel

    # Print end title
    echo "# ===== Set up \`readline-devel\` ====="

    # Print title
    echo -e "\n# ----- Set up \`sqlite-devel\` -----"

    # Set up the package
    yum install -y sqlite-devel

    # Print end title
    echo "# ===== Set up \`sqlite-devel\` ====="

# If command `yum` is not available.

# If commands `apt-get` and `yum` are not available.
else
    # Print info
    echo 'Error: `apt-get` and `yum` are not found.'

    # Exit with error code
    exit 1
fi
