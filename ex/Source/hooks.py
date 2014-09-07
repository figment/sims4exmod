import sys

from singletons import DEFAULT
import os.path
import _trace

import sims4
import sims4.log
from sims4.console_colors import ConsoleColor
import sims4.console_colors
from ex import MOD_PATH

# first override the stdout and stderr log files
#  this is global so only do this for debugging

stderr_log = os.path.join(MOD_PATH, 'stderr.log')
stdout_log = os.path.join(MOD_PATH, 'stdout.log')

class FileLogHandler:
    def __init__(self, name, flags="wt", *args, **kwargs):
        self.file = open(name, flags, *args, **kwargs)

    def write(self, string):
        self.file.write(string)
        self.flush()  # maybe overused but ensures file is updated regularly

    def close(self):
        self.file.close()

    def flush(self):
        self.file.flush()

sys.stdout = FileLogHandler(stdout_log)
sys.stderr = FileLogHandler(stderr_log)

# next override the basic log functions in sims4
def write(message):
    try:
        sys.stdout.write(message)
        sys.stdout.write("\n")
        # sys.stdout.flush()
    except Exception as ex:
        sys.stderr.write(str(ex))
        sys.stderr.write("\n")
        # sys.stderr.flush()


def log(group, message, *args, level, frame=DEFAULT, owner=None):
    result = False
    try:
        if owner:
            message = ('[{owner}] ' + message).format(owner=owner, *args)
        elif args:
            message = message.format(*args)
        if frame is DEFAULT:
            frame = sys._getframe(1)
        ConsoleColor.change_color(sims4.log.get_console_color(level, group))
        result = _trace.trace(sims4.log.TYPE_LOG, message, group, level, sims4.log.get_log_zone(), frame)
    except:
        pass
    write(message)
    return result


def message(message, *args, owner=None):
    result = False
    try:
        if owner:
            message = ('[{owner}] ' + message).format(owner=owner, *args)
        elif args:
            message = message.format(*args)
        frame = sys._getframe(1)
        result = _trace.trace(sims4.log.TYPE_TRACE, message, frame=frame)
    except:
        pass
    write(message)
    return result


sims4.log.log = log
sims4.log.message = message

# now do some more sophisticated patching of logger functions

def monkeypatch(target):
    def patcher(func):
        setattr(target, func.__name__, func)
        return func

    return patcher


@monkeypatch(sims4.log.Logger)
def log(self, message, *args, level, owner=None, trigger_breakpoint=False):
    write(message)


@monkeypatch(sims4.log.LoggerClass)
def log(self, message, *args, level, frame=DEFAULT, owner=None, trigger_breakpoint=False, **kwargs):
    result = False
    try:
        owner = owner or self.default_owner
        if owner:
            message = ('[{owner}] ' + message).format(owner=owner, *args)
        elif args:
            message = message.format(*args)
        if frame is DEFAULT:
            frame = sys._getframe(2)
        result = _trace.trace(sims4.log.TYPE_LOG, message, self.group, level, sims4.log.get_log_zone(), frame)
    except:
        pass
    write(message)
    return result
