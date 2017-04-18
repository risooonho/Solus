"""Docstring for main."""
from lib.states import main_menu
from tools import Control
import setup
import constants as c

MAIN_MENU = 'main menu'


def main():
    run_it = Control(setup.ORIGINAL_CAPTION)
    state_dict = {MAIN_MENU: main_menu.Menu()}
    run_it.setup_states(state_dict, c.MAIN_MENU)
    run_it.main()
