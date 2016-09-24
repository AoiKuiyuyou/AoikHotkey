# coding: utf-8
"""
This module contains task manager.
"""
from __future__ import absolute_import

# Standard imports
from multiprocessing.pool import ThreadPool
import sys
from traceback import format_exc


class TaskManager(object):
    """
    Task manager that manages a thread pool. It is used to run hotkey \
    functions in the thread pool.
    """

    def __init__(self):
        """
        Constructor.

        :return: None.
        """
        # Create thread pool
        self._thread_pool = ThreadPool(3)

    def add_task(self, func):
        """
        Add task function to be run in the task manager's thread pool.

        :param func: Task function.

        :return: None.
        """
        # Create wrapper function
        def func_wrapper():
            try:
                # Call given function
                func()

            # If have error
            except BaseException:
                # Get traceback message
                tb_msg = format_exc()

                # Get error message
                msg = (
                    '# Error calling function in task thread:\n'
                    '---\n{0}---\n'
                ).format(tb_msg)

                # Print error message
                sys.stderr.write(msg)

        # Run the wrapper function in the thread pool
        self._thread_pool.apply_async(func_wrapper)


# Create task manager
_TASK_MANAGER = TaskManager()


def add_task(func):
    """
    Add task function to be run in the task manager's thread pool.

    :param func: Task function.

    :return: None.
    """
    # Add task function to be run in the task manager's thread pool
    _TASK_MANAGER.add_task(func)
