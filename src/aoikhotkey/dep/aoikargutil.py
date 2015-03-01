# coding: utf-8
from __future__ import absolute_import
from argparse import ArgumentTypeError
import itertools
import re
import sys

#/
__version__ = '0.2'

#/
def str_nonempty(txt):
    if txt != '':
        return txt
    else:
        raise ArgumentTypeError('Empty value is not allowed.')

#/
def str_strip_nonempty(txt):
    #/
    txt = txt.strip()

    #/
    if txt != '':
        return txt
    else:
        raise ArgumentTypeError('Empty value is not allowed.')

#/
def bool_0or1(txt):
    if txt == '0':
        return False
    elif txt == '1':
        return True
    else:
        raise ArgumentTypeError('|%s| is not 0 or 1.' % txt)

#/
def float_lt0(txt):
    try:
        val = float(txt)
        assert val < 0
    except Exception:
        raise ArgumentTypeError('|%s| is not a negative number.' % txt)
    return val

#/
def float_le0(txt):
    try:
        val = float(txt)
        assert val <= 0
    except Exception:
        raise ArgumentTypeError('|%s| is not zero or a negative number.' % txt)
    return val

#/
def float_gt0(txt):
    try:
        val = float(txt)
        assert val > 0
    except Exception:
        raise ArgumentTypeError('|%s| is not a positive number.' % txt)
    return val

#/
def float_ge0(txt):
    try:
        val = float(txt)
        assert val >= 0
    except Exception:
        raise ArgumentTypeError('|%s| is not zero or a positive number.' % txt)
    return val

#/
def int_lt0(txt):
    try:
        val = int(txt)
        assert val < 0
    except Exception:
        raise ArgumentTypeError('|%s| is not a negative integer.' % txt)
    return val

#/
def int_le0(txt):
    try:
        val = int(txt)
        assert val <= 0
    except Exception:
        raise ArgumentTypeError('|%s| is not zero or a negative integer.' % txt)
    return val

#/
def int_gt0(txt):
    try:
        val = int(txt)
        assert val > 0
    except Exception:
        raise ArgumentTypeError('|%s| is not a positive integer.' % txt)
    return val

#/
def int_ge0(txt):
    try:
        val = int(txt)
        assert val >= 0
    except Exception:
        raise ArgumentTypeError('|%s| is not zero or a positive integer.' % txt)
    return val

#/
def ensure_exc(parser, spec, args=None):
    #/
    if args is None:
        args = sys.argv[1:]

    #/
    if isinstance(spec, list):
        spec_s = spec
    elif isinstance(spec, tuple):
        spec_s = [spec]
    else:
        assert False, spec

    #/
    for spec in spec_s:
        #/
        spec_len = len(spec)

        #/
        if spec_len < 2:
            continue

        #/
        #assert spec_len >= 2
        if spec_len == 2:
            #/
            s0, s1 = spec

            #/ if is special syntax e.g. ['-a', ['-b', '-c']]
            if isinstance(s1, (list, tuple)):
                #/ transform to pairs [('-a', '-b'), ('-a', '-c')]
                pair_s = [(s0, x) for x in s1]

            #/ if is regular syntax e.g. ['-a', '-b']
            else:
                #/ transform to pairs [('-a', '-b')]
                pair_s = [spec]

        #/ if is regular syntax e.g. ['-a', '-b', '-c']
        else:
            #/ transform to pairs [('-a', '-b'), ('-a', '-c'), ('-b', '-c')]
            pair_s = list(itertools.combinations(spec, 2))

        #/
        for pair in pair_s:
            #/
            arg_a, arg_b = pair

            arg_a_rec = re.compile('^%s($|=|[0-9])' % arg_a)

            arg_b_rec = re.compile('^%s($|=|[0-9])' % arg_b)

            #/
            if any(map(lambda x: bool(arg_a_rec.search(x)), args))\
            and any(map(lambda x: bool(arg_b_rec.search(x)), args)):
                #/
                msg = 'argument %s: not allowed with argument %s' % (arg_a, arg_b)

                parser.error(msg)
                ## raise error

#/
def ensure_one_arg_specs_to_arg_names(specs):
    #/
    arg_name_s = []

    for arg_spec_x in specs:
        if isinstance(arg_spec_x, str):
            #/
            arg_name_s.append(arg_spec_x)
        #/
        elif isinstance(arg_spec_x, (list, tuple)):
            #/
            arg_name_s.append(arg_spec_x[0])
        #/
        else:
            assert False, arg_spec_x

    #/
    return arg_name_s

#/
def ensure_one(parser, spec, args=None):
    #/
    if args is None:
        args = sys.argv[1:]

    #/
    if isinstance(spec, list):
        spec_s = spec
    elif isinstance(spec, tuple):
        spec_s = [spec]
    else:
        assert False, spec

    #/
    for spec in spec_s:
        #/
        spec_pass = False

        #/
        arg_spec_s = spec

        for arg_spec in arg_spec_s:
            #/
            sub_spec = None

            #/
            if isinstance(arg_spec, str):
                #/
                arg_name = arg_spec

                sub_spec = None
            #/
            elif isinstance(arg_spec, (list, tuple)):
                #/
                arg_name = arg_spec[0]

                sub_spec = arg_spec[1]
            #/
            else:
                assert False, arg_spec

            #/
            arg_name_rec = re.compile('^%s($|=|[0-9])' % arg_name)

            #/
            arg_name_exists = any(map(lambda x: bool(arg_name_rec.search(x)), args))

            if arg_name_exists:
                #/
                if isinstance(arg_spec_s, tuple):
                    #/
                    exc_arg_name_s = ensure_one_arg_specs_to_arg_names(arg_spec_s)

                    #/
                    exc_spec = tuple(exc_arg_name_s)

                    #/
                    ensure_exc(parser=parser, spec=exc_spec, args=args)

                #/
                if sub_spec is not None:
                    ensure_spec(parser=parser, spec=sub_spec, args=args)

                #/
                spec_pass = True

                break

        #/
        if not spec_pass:
            arg_name_s = ensure_one_arg_specs_to_arg_names(arg_spec_s)

            msg = """one of the arguments %s is required""" % (', '.join(arg_name_s))

            parser.error(msg)
            ## raise error

#/
def ensure_two(parser, spec, args=None):
    #/
    if args is None:
        args = sys.argv[1:]

    #/
    if isinstance(spec, list):
        spec_s = spec
    elif isinstance(spec, tuple):
        spec_s = [spec]
    else:
        assert False, spec

    #/
    for spec in spec_s:
        #/
        arg_a_spec, arg_b_spec = spec

        #/
        if isinstance(arg_a_spec, (list, tuple)):
            arg_a_s = arg_a_spec
        else:
            arg_a_s = [arg_a_spec]

        #/
        for arg_a in arg_a_s:
            #/
            arg_a_rec = re.compile('^%s($|=|[0-9])' % arg_a)

            #/
            arg_a_exists = any(bool(arg_a_rec.search(arg)) for arg in args)

            #/
            if arg_a_exists:
                #/
                if isinstance(arg_b_spec, (list, tuple)):
                    #/
                    arg_b_s = arg_b_spec
                else:
                    #/
                    arg_b_s = [arg_b_spec]

                #/
                arg_b_rec_s = [re.compile('^%s($|=|[0-9])' % arg_b) for arg_b in arg_b_s]

                #/
                if isinstance(arg_b_spec, tuple):
                    req_all_arg_bs = True
                else:
                    req_all_arg_bs = False

                #/
                arg_b_exists = False

                for arg_b_rec in arg_b_rec_s:
                    #/
                    arg_b_exists = any(bool(arg_b_rec.search(arg)) for arg in args)

                    #/
                    if arg_b_exists:
                        if not req_all_arg_bs:
                            break
                    else:
                        if req_all_arg_bs:
                            break

                #/
                if not arg_b_exists:
                    #/
                    if isinstance(arg_b_spec, tuple):
                        #/
                        msg = 'argument %s: requires all of the arguments %s' % (arg_a, ', '.join(arg_b_spec))

                        parser.error(msg)
                        ## raise error
                    #/
                    elif isinstance(arg_b_spec, list):
                        #/
                        msg = 'argument %s: requires one of the arguments %s' % (arg_a, ', '.join(arg_b_spec))

                        parser.error(msg)
                        ## raise error
                    else:
                        #/
                        msg = 'argument %s: requires argument %s' % (arg_a, arg_b_spec)

                        parser.error(msg)
                        ## raise error

#/
SPEC_DI_K_EXC = 'exc'
SPEC_DI_K_ONE = 'one'
SPEC_DI_K_TWO = 'two'
def ensure_spec(parser, spec, args=None):
    #/
    if args is None:
        args = sys.argv[1:]

    #/
    one_spec = spec.get(SPEC_DI_K_ONE, None)

    if one_spec is not None:
        ensure_one(parser=parser, spec=one_spec, args=args)

    #/
    two_spec = spec.get(SPEC_DI_K_TWO, None)

    if two_spec is not None:
        ensure_two(parser=parser, spec=two_spec, args=args)

    #/
    exc_spec = spec.get(SPEC_DI_K_EXC, None)

    if exc_spec is not None:
        ensure_exc(parser=parser, spec=exc_spec, args=args)
