"""
This module starts the main loop.

Create a control object,
load the state dict for game flow.
Run the control object main loop.
"""

from lib.states import main_menu, world
from tools import Control
import setup
import constants as c

MAIN_MENU = 'main menu'
WORLD = 'world'


def main():
    """Add states to control here and run control."""
    run_it = Control(setup.ORIGINAL_CAPTION)
    state_dict = {MAIN_MENU: main_menu.Menu(),  # Start/draw menu.
                  WORLD: world.World()}
    run_it.setup_states(state_dict, c.MAIN_MENU)  # Load dict into control.
    run_it.main()
