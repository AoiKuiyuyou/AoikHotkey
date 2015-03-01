# coding: utf-8
"""
File ID: 3ngd7IH
"""
from __future__ import absolute_import

import imp
import os.path
import sys


try:
    from urllib.request import urlopen ## Py3
except ImportError:
    from urllib2 import urlopen ## Py2

#/
__version__ = '0.2.3'

#/ define |exec_| and |raise_| that are 2*3 compatible.
##
## Modified from |six|:
##  https://bitbucket.org/gutworth/six/src/cc9fce6016db076497454f9352e55b4758ccc07c/six.py?at=default#cl-632
##
## ---BEG
if sys.version_info[0] == 2:
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
def add_to_sys_modules(mod_name, mod_obj=None):
    """Add a module object to |sys.modules|.

    @param mod_name: module name, used as key to |sys.modules|.
    If |mod_name| is |a.b.c| while modules |a| and |a.b| are not existing,
     empty modules will be created for |a| and |a.b| as well.

    @param mod_obj: a module object.
    If None, an empty module object will be created.
    """
    #/
    mod_sname_s = mod_name.split('.')

    #/
    parent_mod_name = ''

    parent_mod_obj = None

    for mod_sname in mod_sname_s:
        #/
        if parent_mod_name == '':
            cur_mod_name = mod_sname
        else:
            cur_mod_name = parent_mod_name + '.' + mod_sname

        #/
        if cur_mod_name == mod_name:
            #/
            cur_mod_obj = mod_obj
        else:
            #/
            cur_mod_obj = sys.modules.get(cur_mod_name, None)

        #/
        if cur_mod_obj is None:
            #/ create an empty module
            cur_mod_obj = imp.new_module(cur_mod_name)

        #/
        sys.modules[cur_mod_name] = cur_mod_obj

        #/
        if parent_mod_obj is not None:
            setattr(parent_mod_obj, mod_sname, cur_mod_obj)

        #/
        parent_mod_name = cur_mod_name

        parent_mod_obj = cur_mod_obj

#/
def import_module_by_code(mod_code, mod_name, sys_add=True, sys_use=True):
    """Create a module object by code.
    @param mod_code: the code that the module contains.

    @param mod_name: module name.

    @param sys_use: whether use an existing module with the same name in |sys.modules|,
     instead of creating a new one.

    @param sys_add: whether add the module object to |sys.modules|.
    If |sys_add| is on, |mod_name| is used as key to |sys.modules|.

    If |sys_add| is on, and if |mod_name| is |a.b.c| while modules
     |a| and |a.b| are not existing, empty modules will be created
     for |a| and |a.b| as well.
    """
    #/
    mod_obj_old = sys.modules.get(mod_name, None)

    #/
    if mod_obj_old is not None and sys_use:
        return mod_obj_old

    #/
    mod_obj = imp.new_module(mod_name)

    #/ 3plQeic
    exec_(mod_code, mod_obj.__dict__, mod_obj.__dict__)

    #/
    if sys_add:
        #/
        add_to_sys_modules(mod_name=mod_name, mod_obj=mod_obj)

    #/
    return mod_obj

#/
def import_module_by_name(mod_name,
    ns_dir=None,
    sys_use=True,
    sys_add=True,
    ):
    """Import a module by module name.

    @param mod_name: module name in Python namespace.

    @param ns_dir: load from which namespace dir.
    Namespace dir means the dir is considered as if it's in |sys.path|.
    If |ns_dir| is specified, only load from that dir.
    Otherwise load from any namespace dirs in |sys.path|.
    """
    #/
    if ns_dir is None:
        #/
        try:
            mod_obj_old = sys.modules[mod_name]
        except KeyError:
            mod_obj_old = None

        #/
        if sys_use:
            #/
            if mod_obj_old is not None:
                return mod_obj_old
        #/
        #/ 3pRKQd1
        #/ if not want to use existing module in "sys.modules", need re-import
        ##  by calling "__import__" at 2eys2rL. But "__import__" will return
        ##  existing module in "sys.modules", so we must delete existing module
        ##  before calling "__import__".
        else:
            #/
            try:
                del sys.modules[mod_name]
            except KeyError:
                pass

        #/
        try:
            #/ 2eys2rL
            __import__(mod_name)
            ## raise ImportError if the module not exists.
            ## raise any error from the imported module.
        except Exception:
            #/
            if mod_obj_old is not None:
                #/ restore to "sys.modules" the old module deleted at 3pRKQd1
                sys.modules[mod_name] = mod_obj_old

            #/
            raise

        #/
        mod_obj = sys.modules[mod_name]

        #/
        if not sys_add:
            #/
            par_mod = None

            rdot_idx = mod_name.rfind('.')

            if rdot_idx != -1:
                #/
                par_mod_name = mod_name[0:rdot_idx]

                mod_sname = mod_name[rdot_idx+1:]

                #/ can None
                par_mod = sys.modules.get(par_mod_name, None)

            #/
            if mod_obj_old is not None:
                #/ restore to "sys.modules" the old module deleted at 3pRKQd1
                sys.modules[mod_name] = mod_obj_old

                #/ restore to parent module's attribute the old module deleted
                ##  at 3pRKQd1
                if par_mod is not None \
                and getattr(par_mod, mod_sname, None) is mod_obj:
                    try:
                        setattr(par_mod, mod_sname, mod_obj_old)
                    except AttributeError:
                        pass
            #/
            else:
                #/ delete from "sys.modules" the module newly loaded at 2eys2rL.
                try:
                    del sys.modules[mod_name]
                except KeyError:
                    pass

                #/
                if par_mod is not None \
                and getattr(par_mod, mod_sname, None) is mod_obj:
                    #/ delete from parent module's attribute the module
                    ##  newly loaded at 2eys2rL.
                    try:
                        delattr(par_mod, mod_sname)
                    except AttributeError:
                        pass

        #/
        return mod_obj

    #/
    #assert ns_dir is not None

    #/
    mod_file_name_s = mod_name.split('.')
    ## |file_name| means the bare name, without extension.
    ##
    ## E.g. 'a.b.c' to ['a', 'b', 'c']

    #/
    parent_mod_name = '' ## change in each iteration below

    mod_file_dir = ns_dir ## change in each iteration below

    for mod_file_name in mod_file_name_s:
        #/
        if parent_mod_name == '':
            parent_mod_obj = None

            mod_name = mod_file_name
        else:
            parent_mod_obj = sys.modules[parent_mod_name]

            mod_name = parent_mod_name + '.' + mod_file_name

        #/
        if parent_mod_obj:
            __import__(mod_name)

            mod_obj = sys.modules[mod_name]
        else:
            file_handle = None

            try:
                #/
                tup = imp.find_module(mod_file_name, [mod_file_dir])
                ## raise ImportError

                #/
                mod_obj = imp.load_module(mod_name, *tup)
                ## raise any error from the imported module.

                #/
                file_handle = tup[0]
            finally:
                if file_handle is not None:
                    file_handle.close()

        #/
        parent_mod_name = mod_name

        mod_file_dir = os.path.join(mod_file_dir, mod_file_name)

    #/
    return mod_obj

#/
def import_module_by_path(mod_path, mod_name, sys_add=True, sys_use=True):
    """Import a module by module file path.

    @param mod_path: module file path.

    @param mod_name: module name to be imported as.

    @param sys_use: see func |import_module_by_code|'s same name arg.

    @param sys_add: see func |import_module_by_code|'s same name arg.
    """
    #/
    mod_code = open(mod_path).read()
    ## raise error

    #/
    mod_obj = import_module_by_code(
        mod_code=mod_code,
        mod_name=mod_name,
        sys_use=sys_use,
        sys_add=sys_add,
    )
    ## raise error

    #/
    mod_obj.__file__ = mod_path

    #/
    return mod_obj

#/
def import_module_by_http(uri, mod_name, sys_use=True, sys_add=True):
    """Download module code via HTTP and create the module object from the code.

    @param uri: HTTP URI of the module file.

    @param mod_name: module name to be imported as.

    @param sys_use: see func |import_module_by_code|'s same name arg.

    @param sys_add: see func |import_module_by_code|'s same name arg.
    """
    #/
    resp = urlopen(uri)
    ## raise error

    #/
    mod_code = resp.read()
    ## raise error

    #/
    mod_obj = import_module_by_code(
        mod_code=mod_code,
        mod_name=mod_name,
        sys_use=sys_use,
        sys_add=sys_add,
    )
    ## raise error

    #/
    return mod_obj

#/
def uri_split(uri, mod_attr_sep='::'):
    #/
    uri_part_s = uri.split(mod_attr_sep, 2)
    ## use |split| instead of |partition| to be compatible with Python 2.4-

    if len(uri_part_s) == 2:
        mod_uri, attr_chain = uri_part_s
    else:
        mod_uri = uri_part_s[0]

        attr_chain = None

    #/
    if uri.startswith('http://'):
        #/
        prot = 'http'

        #/ mod_uri is file url
        #mod_uri = mod_uri
    #/
    elif uri.startswith('https://'):
        prot = 'https'

        #/ mod_uri is file url
        #mod_uri = mod_uri
    #/
    elif mod_uri.startswith('py://'):
        #/
        prot = 'py'

        #/ mod_uri is module name
        mod_uri = mod_uri[5:]
    #/
    elif mod_uri.startswith('file://'):
        #/
        prot = 'file'

        #/ mod_uri is file path
        mod_uri = mod_uri[7:]
    #/
    elif mod_uri.endswith('.py'):
    ## This means if no protocol prefix is present, and the uri ends with |.py|,
    ##  then consider the uri as module file path instead of module name.
        #/
        prot = 'file'

        #/ mod_uri is file path
        #mod_uri = mod_uri
    else:
        #/
        prot = 'py'

        #/ mod_uri is module name
        #mod_uri = mod_uri

    #/
    res = (prot, mod_uri, attr_chain)

    return res

#/
def getattr_chain(obj, attr_chain, sep='.'):
    """Get the last attribute of a specified chain of attributes from a specified object.
    E.g. |getattr_chain(x, 'a.b.c')| is equivalent to |x.a.b.c|.

    @param obj: an object

    @param attr_chain: a chain of attribute names

    @param sep: separator for the chain of attribute names
    """
    #/
    if sep is None:
        sep = '.'

    #/
    attr_name_s = attr_chain.split(sep)

    #/
    new_obj = obj

    for attr_name in attr_name_s:
        new_obj = getattr(new_obj, attr_name)

    #/
    return new_obj

#/
def load_obj(
    uri,
    mod_name=None,
    sys_use=True,
    sys_add=True,
    mod_attr_sep='::',
    attr_chain_sep='.',
    retn_mod=False,
    uri_parts=None,
    ):
    """Load an object from a module (specified by module name in Python namespace)
     or from a module file (specified by module file path).

    @param uri: an uri specifying which object to load.
    An |uri| consists of two parts: |module uri| and |attr chain|,
     e.g. |a/b/c.py::x.y.z| or |a.b.c::x.y.z|

    #/ module uri
    |a/b/c.py| or |a.b.c| is the |module uri| part.
    Can be either a file path or a module name in Python namespace.
    Whether it is a file path is determined by whether it ends with |.py|.

    #/ attr chain
    |x.y.z| is attribute chain on the module object specified by module uri.

    @param mod_name: module name to be imported as.
    Only applies when |uri| specifies a module file path, not a module name.
    If None, the module file's name is used.
     E.g. |path/to/hello.py| gets module name |hello|.

    @param sys_use: see func |import_module_by_code|'s same name arg.

    @param sys_add: see func |import_module_by_code|'s same name arg.

    @param mod_attr_sep: see func |load_obj|'s same name arg.

    @param attr_chain_sep: see func |load_obj|'s same name arg.

    @retn_mod: see func |load_obj|'s same name arg.
    """
    #/
    if uri_parts is None:
        uri_parts = uri_split(uri=uri, mod_attr_sep=mod_attr_sep)

    prot, mod_uri, attr_chain = uri_parts

    #/
    if prot == 'py':
    ## This means the uri specifies a module name, e.g. |a.b.c|
        #/
        mod_name_to_load = mod_uri
        ## avoid naming collision with func arg |mod_name|.
        ##
        ## arg |mod_name| is not used when importing by module name.
        ## the name of the module to import is specified in arg |uri|.

        #/
        mod_obj = import_module_by_name(mod_name_to_load,
            sys_use=sys_use,
            sys_add=sys_add,
        )
        ## raise error

    else:
    ## This means the uri specifies a module file path, e.g. |/a/b/c.py|
        #/
        mod_file_path = mod_uri

        #/
        if not mod_name:
            _, mod_file_name = os.path.split(mod_file_path)

            mod_name, _ = os.path.splitext(mod_file_name)

        #/
        mod_obj = import_module_by_path(mod_file_path,
            mod_name=mod_name,
            sys_use=sys_use,
            sys_add=sys_add,
        )
        ## raise error

    #/
    if not attr_chain:
        if retn_mod:
            return mod_obj, None
        else:
            return mod_obj

    #/
    #assert attr_chain

    attr_obj = getattr_chain(
        obj=mod_obj,
        attr_chain=attr_chain,
        sep=attr_chain_sep,
    )
    ## raise error

    #/
    if retn_mod:
        return mod_obj, attr_obj
    else:
        return attr_obj

#/
def load_obj_http(
    uri,
    mod_name=None,
    sys_use=True,
    sys_add=True,
    mod_attr_sep='::',
    attr_chain_sep='.',
    retn_mod=False,
    uri_parts=None,
    ):
    """Load an object from a remote module file downloaded via HTTP.

    @param uri: specify the remote module file's location and which attribute object to load.
    #/ load the module object
    https://localhost/aoikimportutil/aoikimportutil.py

    #/ load the module object, get its attribute object |load_obj_http|.
    https://localhost/aoikimportutil/aoikimportutil.py::load_obj_http

    @param mod_name: module name to be imported as.

    @param sys_use: see func |import_module_by_code|'s same name arg.

    @param sys_add: see func |import_module_by_code|'s same name arg.

    @param mod_attr_sep: see func |load_obj|'s same name arg.

    @param attr_chain_sep: see func |load_obj|'s same name arg.

    @retn_mod: see func |load_obj|'s same name arg.
    """
    #/
    if uri_parts is None:
        uri_parts = uri_split(uri=uri, mod_attr_sep=mod_attr_sep)

    _, file_url, attr_chain = uri_parts

    #/
    if not mod_name:
    ## |None| or |''|
        #/ use file name as module name
        _, file_name = os.path.split(file_url)

        mod_name, _ = os.path.splitext(file_name)

        #/ should not happen, but just in case
        if not mod_name:
            raise ValueError('Module name can not be inferred from the URI.\n URI is |%s|' % uri)

    #/
    #assert mod_name

    mod_obj = import_module_by_http(
        uri=file_url,
        mod_name=mod_name,
        sys_use=sys_use,
        sys_add=sys_add,
    )

    #/
    if not attr_chain:
        if retn_mod:
            return mod_obj, None
        else:
            return mod_obj

    #/
    #assert attr_chain

    attr_obj = getattr_chain(
        obj=mod_obj,
        attr_chain=attr_chain,
        sep=attr_chain_sep,
    )
    ## raise error

    #/
    if retn_mod:
        return mod_obj, attr_obj
    else:
        return attr_obj

#/
def load_obj_local_or_remote(
    uri,
    mod_name=None,
    sys_use=True,
    sys_add=True,
    mod_attr_sep='::',
    attr_chain_sep='.',
    retn_mod=False,
    ):
    """Load an object from local or remote (using HTTP).

    Whether it's local or remote depends on
     whether the |uri| starts with |http://| or |https://|.

    Local loading is done via func |load_obj|.

    Remote loading is done via func |load_obj_http|.

    @param uri: see func |load_obj| or |load_obj_http|'s same name arg.

    @param mod_name: see func |load_obj| or |load_obj_http|'s same name arg.

    @param sys_use: see func |import_module_by_code|'s same name arg.

    @param sys_add: see func |import_module_by_code|'s same name arg.

    @param mod_attr_sep: see func |load_obj| or |load_obj_http|'s same name arg.

    @param attr_chain_sep: see func |load_obj| or |load_obj_http|'s same name arg.

    @retn_mod: see func |load_obj| or |load_obj_http|'s same name arg.
    """
    #/
    uri_parts = uri_split(uri=uri, mod_attr_sep=mod_attr_sep)

    prot = uri_parts[0]

    #/
    if prot in ('py', 'file'):
        #/
        return load_obj(
            uri,
            mod_name=mod_name,
            sys_use=sys_use,
            sys_add=sys_add,
            mod_attr_sep=mod_attr_sep,
            attr_chain_sep=attr_chain_sep,
            retn_mod=retn_mod,
            uri_parts=uri_parts,
        )
    #/
    elif prot in ('http', 'https'):
        #/
        return load_obj_http(
            uri,
            mod_name=mod_name,
            sys_use=sys_use,
            sys_add=sys_add,
            mod_attr_sep=mod_attr_sep,
            attr_chain_sep=attr_chain_sep,
            retn_mod=retn_mod,
            uri_parts=uri_parts,
        )
    #/
    else:
        #/
        assert 0, uri
