import sys
import os
import os.path
import sims4.commands


MOD_PATH = None
MOD_NAME = __name__
MOD_ROOT = None
LOGFILE = sys.stdout
LOGPATH = '.'
reloader = None


def reload_module():
    global reloader, LOGFILE, MOD_NAME

    modules = [y for x, y in sys.modules.items() if x.startswith(MOD_NAME + '.')]
    print("To Reload:", modules, file=LOGFILE, flush=True)
    visited = reloader.reloadlist(modules)
    print("Visited:", visited, file=LOGFILE, flush=True)


def initialize():
    global MOD_PATH, MOD_NAME, LOGFILE, LOGPATH, MOD_ROOT
    try:
        (filepath, filename) = os.path.split(__file__)
        MOD_PATH = filepath
        LOGPATH = os.path.join(filepath, 'logs')
        if not os.path.exists(LOGPATH):
            os.mkdir(LOGPATH)
        LOGFILE = open(os.path.join(LOGPATH, MOD_NAME + '.log'), "wt")

        # extract root folder for loading files
        (MOD_ROOT, _) = os.path.split(filepath)

        def sourceimporter(modulename, pkg_root=MOD_ROOT):
            import importlib.machinery
            import os.path
            mod_path = os.path.join(pkg_root, modulename.replace('.', os.path.sep))
            mod_fname = mod_path + '.py' if not os.path.isdir(mod_path) else os.path.join(mod_path, '__init__.py')
            print("Loading '{}' from '{}'".format(modulename, mod_fname))
            loader = importlib.machinery.SourceFileLoader(modulename, mod_fname)
            module = loader.load_module(modulename)
            if modulename not in sys.modules:
                sys.modules[modulename] = module
            return module

        # load the modules
        global reloader
        reloader = sourceimporter(MOD_NAME + '.' + 'reloader')
        if reloader:
            for name in ['hooks', 'debug', 'commands']:
                reloader.load(MOD_NAME + '.' + name, importer=sourceimporter)

    except Exception as e:
        with open(os.path.join(LOGPATH, 'err.log'), "wt") as f:
            import traceback
            f.write(str(e) + "\n")
            traceback.print_exc(file=f)


@sims4.commands.Command(MOD_NAME + '.reload', command_type=sims4.commands.CommandType.Live)
def reload_command(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output("Reloading Modules")

    global LOGPATH
    try:
        reload_module()
        output("Reloading Completed")
    except Exception as e:
        with open(os.path.join(LOGPATH, 'err.log'), "wt") as f:
            import traceback
            f.write(str(e) + "\n")
            traceback.print_exc(file=f)
        pass
    return False

# have to call initialize() before leaving the module to bootstrap the whole process
initialize()
