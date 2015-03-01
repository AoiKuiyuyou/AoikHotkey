# coding: utf-8
from __future__ import absolute_import
import sys
import traceback

#/
__version__ = '0.1'

#/
IS_PY2 = sys.version_info[0] == 2

#/ define |exec_| and |raise_| that are 2*3 compatible.
##
## Modified from |six|:
##  https://bitbucket.org/gutworth/six/src/cc9fce6016db076497454f9352e55b4758ccc07c/six.py?at=default#cl-632
##
## ---BEG
if IS_PY2:
    #/
    def exec_(_code_, _globs_=None, _locs_=None):
        """Execute code in a namespace."""
        if _globs_ is None:
            frame = sys._getframe(1)
            _globs_ = frame.f_globals
            if _locs_ is None:
                _locs_ = frame.f_locals
            del frame
        elif _locs_ is None:
            _locs_ = _globs_
        exec("""exec _code_ in _globs_, _locs_""")

    #/
    exec_("""def raise_(exc, tb=None):
    raise exc, None, tb
""")
else:
    #/
    exec_ = eval('exec')

    #/
    def raise_(exc, tb=None):
        if tb is not None and exc.__traceback__ is not tb:
            raise exc.with_traceback(tb)
        else:
            raise exc
## ---END

#/
def get_traceback_stxt():
    """
    Result is (bytes) str type on Python 2 and (unicode) str type on Python 3.
    """
    #/
    exc_cls, exc_obj, tb_obj = sys.exc_info()

    #/
    txt_s = traceback.format_exception(exc_cls, exc_obj, tb_obj)

    #/
    res = ''.join(txt_s)

    return res
