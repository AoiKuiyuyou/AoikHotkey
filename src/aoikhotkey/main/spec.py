# coding: utf-8
from __future__ import absolute_import

from aoikhotkey.const import SPEC_SWITCH_V_NEXT
from aoikhotkey.const import SPEC_SWITCH_V_PREV
from aoikhotkey.spec.efunc import efunc_no_mouse_move
from aoikhotkey.spec.util import Cmd
from aoikhotkey.spec.util import Quit
from aoikhotkey.spec.util import SpecReload
from aoikhotkey.spec.util import SpecSwitch


#/ 3qMmsJ5
SPEC = [
    #/ 8fsGDgc
    ('$', efunc_no_mouse_move),

    ('<^q', Quit),

    ('<!q', SpecReload),

    ('<^[', SpecSwitch(SPEC_SWITCH_V_PREV)),

    ('<^]', SpecSwitch(SPEC_SWITCH_V_NEXT)),

    ('<^n', Cmd('notepad.exe')),
]
