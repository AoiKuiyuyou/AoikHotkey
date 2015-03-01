# coding: utf-8
from __future__ import absolute_import

import os.path
import sys


#/
def pythonpath_init():
    #/
    my_dir = os.path.dirname(os.path.abspath(__file__))

    #/
    for path in ['', '.', my_dir]:
        if path in sys.path:
            sys.path.remove(path)

    #/
    my_dep_dir = os.path.join(os.path.dirname(my_dir), 'dep')

    if my_dep_dir not in sys.path:
        sys.path.insert(0, my_dep_dir)

    #/
    my_src_dir = os.path.dirname(os.path.dirname(my_dir))

    if my_src_dir not in sys.path:
        sys.path.insert(0, my_src_dir)

#/
def main():
    #/
    pythonpath_init()

    #/
    from aoikhotkey.main.main_imp import main as main_

    #/
    return main_()

#/
if __name__ == '__main__':
    #/
    sys.exit(main())
