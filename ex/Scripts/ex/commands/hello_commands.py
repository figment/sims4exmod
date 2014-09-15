import sims4
import sims4.commands
import sims4.log

from ex import MOD_NAME
from ex.utils import *


@sims4.commands.Command(MOD_NAME + '.hello', command_type=sims4.commands.CommandType.Live)
def hello(_connection=None):
    """
    First example:  Outputs text to cheat console

    core_only: fill only the core (initial) commodities.
    """
    output = sims4.commands.CheatOutput(_connection)
    output("World")
    print("Hello World")
    return False