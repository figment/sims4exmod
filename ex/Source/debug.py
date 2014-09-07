import sims4
import sims4.commands
import sims4.log

from ex import MOD_NAME


@sims4.commands.Command(MOD_NAME + '.debug', command_type=sims4.commands.CommandType.Live)
def debug(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output("Connecting to Debugger")
    print("Connecting to Debugger")
    failed = True
    if failed:
        try:
            # Try connecting to Python Tools for Visual Studio 
            #   Note that you need ptvsd.zip in the Mods folder
            #   You also need ctypes from python33\lib in the ptvsd.zip 
            #   as well as _ctypes.pyd copied to Origin\Game\bin\Python\DLLs
            #   You would connect to this machine after this command
            import ptvsd
            ptvsd.enable_attach(secret='ts4')
            # ptvsd.wait_for_attach(timeout=20.0) # wait for 20 seconds?
            failed = False
        except Exception as e:
            import sys, traceback
            print(str(e), file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            pass
            
    if failed:
        try:
            # Try connecting to PyCharm or IntelliJ IDEA Professional
            #   Note that you need pycharm-debug-py3k.egg in the Mods folder
            #   and .egg renamed to .zip for this to work.
            #  Startup the Python Remote Debug Configuration before running this command.
            import pydevd
            pydevd.settrace('localhost', port=5678, stdoutToServer=True, stderrToServer=True)
            failed = False
        except Exception as e:
            import sys, traceback
            print(str(e), file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            pass
        

    if failed:
        output("Exception while connecting to Debugger")
        print("Exception while connecting to Debugger")    
    else:
        output("Continuing Debugger")
        print("Continuing Debugger")
    return False