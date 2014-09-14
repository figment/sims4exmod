import sys

import os
import os.path
import sims4
import reloader


MOD_PATH = None
SOURCE_PATH = None
MOD_NAME = __name__.replace(' ', '_')


def reload_module_from_file(module, filename):
    if module in sys.modules:
        reloader.reload(sys.modules[module])


def load_files(path, callback=None, reload=False):
    import importlib.machinery
    global MOD_NAME, MOD_PATH

    try:
        pkg_fname = os.path.join(path, '__init__.py')
        if os.path.exists(pkg_fname):
            
            modulename = "{}.{}".format(MOD_NAME, 'source').lower()
            if callback:
                callback("import {} from {}".format(modulename, path))
            if reload:
                reload_module_from_file(modulename, pkg_fname)
            else:
                def sourceimporter(modulename):
                    loader = importlib.machinery.SourceFileLoader(modulename, pkg_fname)
                    module = loader.load_module(modulename)
                    if modulename not in sys.modules:
                        sys.modules[modulename] = module

                reloader.load(modulename, importer=sourceimporter)
            pass
    except Exception as ex:
        with open(os.path.join(MOD_PATH, 'err.log'), "wt") as f:
            f.write(str(ex) + "\n")
            import traceback;

            traceback.print_exc(file=f)
        pass

def initialize():
    global MOD_PATH, SOURCE_PATH, MOD_NAME
    try:
        idx = 0
        (filepath, filename) = os.path.split(__file__)
        MOD_PATH = filepath
        SOURCE_PATH = os.path.join(filepath, 'Source')
        if os.path.exists(SOURCE_PATH):
            sys.path.insert(idx, SOURCE_PATH)
            load_files(SOURCE_PATH, callback=print)

    except Exception as ex:
        with open(os.path.join(SOURCE_PATH, 'err.log'), "wt") as f:
            import traceback
            f.write(str(ex) + "\n")
            traceback.print_exc(file=f)
        pass


@sims4.commands.Command(MOD_NAME + '.reload', command_type=sims4.commands.CommandType.Live)
def reload(core_only:bool=True, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output("Reloading Modules")
    try:
        global SOURCE_PATH
        load_files(SOURCE_PATH, callback=output, reload=True)
        output("Reloading Completed")
    except:
        pass
    return False

# have to call initialize() before leaving the module to bootstrap the whole process
initialize()