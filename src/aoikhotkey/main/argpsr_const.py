# coding: utf-8
from __future__ import absolute_import

from aoikargutil import SPEC_DI_K_ONE
from aoikargutil import SPEC_DI_K_TWO


#/
ARG_HELP_ON_F = '-h'
ARG_HELP_ON_F2 = '--help'

#/
ARG_SPEC_URI_F = '-s'
ARG_SPEC_URI_K = '4cHsWb4'
ARG_SPEC_URI_A = 'append'
ARG_SPEC_URI_D = []
ARG_SPEC_URI_V = 'SPEC_URI'
ARG_SPEC_URI_H = 'Spec URI. Can be used multiple times.'

#/
ARG_SPEC_ID_F = '-i'
ARG_SPEC_ID_K = '4mvr4Rt'
ARG_SPEC_ID_A = 'append'
ARG_SPEC_ID_D = []
ARG_SPEC_ID_V = 'SPEC_ID'
ARG_SPEC_ID_H = (
    'Spec ID given to a spec.'
    ' Can be used multiple times,'
    ' each time matching with one {spec_option} in order.'
    ' Spec ID is used by "aoikhotkey.spec.util::SpecSwitch"'
    ' to identify the spec to swicth to.'
).format(spec_option=ARG_SPEC_URI_F)

#/
ARG_SPEC_PARSE_URI_F = '-S'
ARG_SPEC_PARSE_URI_K = '4nLIB4P'
ARG_SPEC_PARSE_URI_D = 'aoikhotkey.spec.parser::spec_parse'
ARG_SPEC_PARSE_URI_V = 'SPEC_PARSE'
ARG_SPEC_PARSE_URI_H = (
    'Spec parse function URI.'
    ' Default is "{default}".'
).format(default=ARG_SPEC_PARSE_URI_D)

#/
ARG_HOTKEY_PARSE_URI_F = '-p'
ARG_HOTKEY_PARSE_URI_K = '4gQtGkg'
ARG_HOTKEY_PARSE_URI_D = 'aoikhotkey.spec.parser::hotkey_parse'
ARG_HOTKEY_PARSE_URI_V = 'HOTKEY_PARSE'
ARG_HOTKEY_PARSE_URI_H = (
    'Hotkey parse function URI.'
    ' Default is "{default}".'
).format(default=ARG_HOTKEY_PARSE_URI_D)

#/
ARG_HOTKEY_TFUNC_URI_F = '-T'
ARG_HOTKEY_TFUNC_URI_K = '5thyp3L'
ARG_HOTKEY_TFUNC_URI_D = 'aoikhotkey.spec.tfunc::hotkey_tfunc'
ARG_HOTKEY_TFUNC_URI_V = 'HOTKEY_TFUNC'
ARG_HOTKEY_TFUNC_URI_H = (
    'Hotkey trigger function URI.'
    ' Default is "{default}".'
).format(default=ARG_HOTKEY_TFUNC_URI_D)

#/
ARG_VK_NTC_URI_F = '-n'
ARG_VK_NTC_URI_K = '4mtINLv'
ARG_VK_NTC_URI_D = 'aoikhotkey.virkey::vk_ntc'
ARG_VK_NTC_URI_V = 'VK_NTC'
ARG_VK_NTC_URI_H = (
    'Virtual key name-to-code function URI. '
    ' Used by hotkey parse function.'
    ' E.g. convert name "VK_LCONTROL" to code 162.'
    ' Default is "{default}".'
).format(default=ARG_VK_NTC_URI_D)

#/
ARG_VK_TRAN_URI_F = '-t'
ARG_VK_TRAN_URI_K = '2z9qPwK'
ARG_VK_TRAN_URI_D = 'aoikhotkey.virkey::vk_tran'
ARG_VK_TRAN_URI_V = 'VK_TRAN'
ARG_VK_TRAN_URI_H = (
    'Virtual key translate function URI.'
    ' Used by hotkey parse function.'
    ' E.g. Translate VK_CONTROL with a preceding "<" to VK_LCONTROL.'
    ' Default is "{default}".'
).format(default=ARG_VK_TRAN_URI_D)

#/
ARG_VK_EXPAND_URI_F = '-e'
ARG_VK_EXPAND_URI_K = '4kmv6KW'
ARG_VK_EXPAND_URI_D = 'aoikhotkey.virkey::vk_expand'
ARG_VK_EXPAND_URI_V = 'VK_EXPAND'
ARG_VK_EXPAND_URI_H = (
    'Virtual key expand function URI.'
    ' Used by hotkey parse function.'
    ' E.g. Expand VK_CONTROL to VK_LCONTROL and VK_RCONTROL.'
    ' Default is "{default}".'
).format(default=ARG_VK_EXPAND_URI_D)

#/
ARG_VK_CTN_URI_F = '-c'
ARG_VK_CTN_URI_K = '3rpR99f'
ARG_VK_CTN_URI_D = 'aoikhotkey.virkey::vk_ctn'
ARG_VK_CTN_URI_V = 'VK_CTN'
ARG_VK_CTN_URI_H = (
    'Virtual key code-to-name function URI.'
    ' Used by hotkey manager to print message when a hotkey is triggered.'
    ' E.g. convert code 162 to name "VK_LCONTROL".'
    ' Default is "{default}".'
).format(default=ARG_VK_CTN_URI_D)

#/
ARG_REPEAT_ON_F = '-r'
ARG_REPEAT_ON_K = '3hLmkQc'
ARG_REPEAT_ON_D = True
ARG_REPEAT_ON_V = '1|0'
ARG_REPEAT_ON_H = (
   'Repeat mode on/off.'
   ' If set off, a repeated key-down event will be ignored.'
   ' Default is {}.'
).format('on' if ARG_REPEAT_ON_D else 'off')

#/
ARG_DBG_MSG_F = '-V'
ARG_DBG_MSG_K = '2s3sNzD'
ARG_DBG_MSG_D = True
ARG_DBG_MSG_V = '1|0'
ARG_DBG_MSG_H = """Debug messages on/off. Default is {}."""\
    .format('on' if ARG_DBG_MSG_D else 'off')

#/
ARG_VER_ON_F = '--ver'
ARG_VER_ON_K = '4yc2oxu'
ARG_VER_ON_A = 'store_true'
ARG_VER_ON_H = 'Show version.'

#/
ARG_SPEC = {
    SPEC_DI_K_ONE: (
        ARG_HELP_ON_F,
        ARG_HELP_ON_F2,
        ARG_VER_ON_F,
        #/
        ARG_SPEC_URI_F,
    ),
}
