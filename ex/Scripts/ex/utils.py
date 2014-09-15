def print(*args, **kwargs):
    try:
        from builtins import print as _sys_print
        import importlib
        if 'file' not in kwargs or 'flush' not in kwargs:
            newargs = kwargs.copy()
            if 'file' not in newargs:
                import sys
                _MOD_NAME = __name__.split('.', 1)[0]
                _mod = importlib.import_module(_MOD_NAME)
                newargs['file'] = getattr(_mod, 'LOGFILE', sys.stdout)
            if 'flush' not in newargs:
                newargs['flush'] = True
        else:
            newargs = kwargs
        _sys_print(*args, **newargs)
    except Exception as e:
        import traceback
        import sys
        sys.stderr.write(str(e) + "\n")
        traceback.print_exc(file=sys.stderr)