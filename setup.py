# coding: utf-8
from __future__ import absolute_import

import os

from setuptools import find_packages
from setuptools import setup


#/
setup(
    name='AoikHotkey',

    version='0.1.2',

    description="""AutoHotkey remake in Python. Hotkey calls Python function.""",

    long_description="""`Documentation on Github
<https://github.com/AoiKuiyuyou/AoikHotkey>`_""",

    url='https://github.com/AoiKuiyuyou/AoikHotkey',

    author='Aoi.Kuiyuyou',

    author_email='aoi.kuiyuyou@google.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='hotkey autohotkey',

    package_dir={'':'src'},

    packages=find_packages('src'),

    entry_points={
        'console_scripts': [
            'aoikhotkey=aoikhotkey.main.aoikhotkey:main',
        ],
    },
)
