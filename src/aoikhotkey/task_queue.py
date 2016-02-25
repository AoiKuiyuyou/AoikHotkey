# coding: utf-8
from __future__ import absolute_import

import sys
from threading import Thread

from aoikexcutil import get_traceback_stxt
from aoikhotkey.spec.util import need_event_info_tag_get


try:
    from queue import Queue # Py3
except ImportError:
    from Queue import Queue # Py2

#
TASK_QUEUE = Queue()

#
def task_queue_thread_func():
    while True:
        task_info = TASK_QUEUE.get()

        if task_info is None:
            break

        func, event = task_info

        try:
            if need_event_info_tag_get(func):
                func(event)
            else:
                func()
        except Exception:
            #
            tb_msg = get_traceback_stxt()

            sys.stderr.write('#/ Error when calling function in task thread\n---\n{}---\n'\
                .format(tb_msg))

def task_queue_thread_start():
    th_obj = Thread(target=task_queue_thread_func)
    th_obj.daemon = True
    th_obj.start()

def task_queue_thread_stop():
    TASK_QUEUE.put(None)
