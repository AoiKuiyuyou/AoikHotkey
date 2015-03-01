# coding: utf-8
from __future__ import absolute_import


#/ initialized at 2styZ2U
_MANAGER = None

#/
def manager_set(manager):
    #/
    global _MANAGER

    _MANAGER = manager

#/
def manager_get():
    #/
    return _MANAGER
