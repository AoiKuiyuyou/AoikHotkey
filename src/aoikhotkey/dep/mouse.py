# coding: utf-8
#
# Modified from http://schurpf.com/python-mouse-control/
#
from __future__ import absolute_import

import ctypes
import time

import win32api
import win32gui


#/
class Mouse:
    """It simulates the mouse"""
    MOUSEEVENTF_MOVE = 0x0001 # mouse move
    MOUSEEVENTF_LEFTDOWN = 0x0002 # left button down
    MOUSEEVENTF_LEFTUP = 0x0004 # left button up
    MOUSEEVENTF_RIGHTDOWN = 0x0008 # right button down
    MOUSEEVENTF_RIGHTUP = 0x0010 # right button up
    MOUSEEVENTF_MIDDLEDOWN = 0x0020 # middle button down
    MOUSEEVENTF_MIDDLEUP = 0x0040 # middle button up
    MOUSEEVENTF_WHEEL = 0x0800 # wheel button rolled
    MOUSEEVENTF_ABSOLUTE = 0x8000 # absolute move
    SM_CXSCREEN = 0
    SM_CYSCREEN = 1

    def _do_event(self, flags, x_pos, y_pos, data, extra_info):
        """generate a mouse event"""
        x_calc = 65536L * x_pos / ctypes.windll.user32.GetSystemMetrics(self.SM_CXSCREEN) + 1
        y_calc = 65536L * y_pos / ctypes.windll.user32.GetSystemMetrics(self.SM_CYSCREEN) + 1
        return ctypes.windll.user32.mouse_event(flags, x_calc, y_calc, data, extra_info)

    def _get_button_value(self, button_name, button_up=False):
        """convert the name of the button into the corresponding value"""
        buttons = 0
        if button_name.find("right") >= 0:
            buttons = self.MOUSEEVENTF_RIGHTDOWN
        if button_name.find("left") >= 0:
            buttons = buttons + self.MOUSEEVENTF_LEFTDOWN
        if button_name.find("middle") >= 0:
            buttons = buttons + self.MOUSEEVENTF_MIDDLEDOWN
        if button_up:
            buttons = buttons << 1
        return buttons

    def move_mouse(self, pos):
        """move the mouse to the specified coordinates"""
        (x, y) = pos
        old_pos = self.get_position()
        x =  x if (x != -1) else old_pos[0]
        y =  y if (y != -1) else old_pos[1]
        self._do_event(self.MOUSEEVENTF_MOVE + self.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0)

    def press_button(self, pos=(-1, -1), button_name="left", button_up=False):
        """push a button of the mouse"""
        self.move_mouse(pos)
        self._do_event(self.get_button_value(button_name, button_up), 0, 0, 0, 0)

    def click(self, pos=(-1, -1), button_name= "left"):
        """Click at the specified placed"""
##        self.move_mouse(pos)
        self._do_event(self._get_button_value(button_name, False)+self._get_button_value(button_name, True), 0, 0, 0, 0)

    def double_click (self, pos=(-1, -1), button_name="left"):
        """Double click at the specifed placed"""
        for i in xrange(2):
            self.click(pos, button_name)

    def get_position(self):
        """get mouse position"""
        return win32api.GetCursorPos()

    def click_abs(self,
        pos,
        button_name='left',
        move_cursor=False,
        pre_click_wait=None,
        ):
        #/
        pre_click_wait = 0.02 if pre_click_wait is None else pre_click_wait

        #/
        if not move_cursor:
            xcur,ycur = win32gui.GetCursorPos()

        #/
        ctypes.windll.user32.SetCursorPos(pos[0],pos[1])

        #/
        if pre_click_wait:
            time.sleep(pre_click_wait)

        #/
        self.click(pos,button_name)

        #/
        if not move_cursor:
            ctypes.windll.user32.SetCursorPos(xcur,ycur)

    def click_rel(self,
        pos,
        button_name='left',
        move_cursor=False,
        pre_click_wait=None,
        handle=None,
        ):
        #/
        if handle is None:
            handle = win32gui.GetForegroundWindow()

        #/
        xleft, ytop, xright, ybottom = win32gui.GetWindowRect(handle)

        #/
        abs_x = pos[0]+xleft

        abs_y = pos[1]+ytop

        #/
        self.click_abs(pos=(abs_x, abs_y),
            button_name=button_name,
            move_cursor=move_cursor,
            pre_click_wait=pre_click_wait,
        )
