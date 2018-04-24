# coding: utf-8
"""
Setup module.
"""
from __future__ import absolute_import

# Standard imports
import sys

# External imports
from setuptools import find_packages
from setuptools import setup


# Whether the platform is Linux
IS_LINUX = sys.platform.startswith('linux')

# Whether the platform is MacOS
IS_MACOS = sys.platform.startswith('darwin')


# If the platform is Linux
if IS_LINUX:
    # Set dependency package list
    dependency_package_list = [
        'python-xlib>=0.17',
    ]

# If the platform is MacOS
elif IS_MACOS:
    # Set dependency package list
    dependency_package_list = [
        'pyobjc>=3.1.1',
    ]

# If the platform is not Linux or MacOS
else:
    # Set dependency package list
    dependency_package_list = []


setup(
    name='AoikHotkey',

    version='0.5.0',

    description=(
        'Python hotkey manager that works on Linux, MacOS, and Windows.'
    ),

    long_description="""`Documentation on Github
<https://github.com/AoiKuiyuyou/AoikHotkey>`_""",

    url='https://github.com/AoiKuiyuyou/AoikHotkey',

    author='Aoi.Kuiyuyou',

    author_email='aoi.kuiyuyou@google.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='hotkey',

    package_dir={
        '': 'src'
    },

    packages=find_packages('src'),

    package_data={
        'aoikhotkeydep': [
            'pyHook_versions/*/*/*',
        ],
    },

    include_package_data=True,

    install_requires=dependency_package_list,

    entry_points={
        'console_scripts': [
            'aoikhotkey=aoikhotkey.__main__:main',
        ],
    },
)
