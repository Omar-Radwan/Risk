import os

from components.logic_gui_controller import LogicGuiController

if __name__ == '__main__':
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(curr_dir)

    logicGuiController = LogicGuiController()
    logicGuiController.start()
