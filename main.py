import sys
from managers import ContainerManager, GUIManager

## FIXME/TODO: use `configparser` for configuring stuffs
## and also, ANTANI

def main(argv):
    """main

    Args:
        argv (list of strings): wrapper for sys.argv
    """
    container_manager = ContainerManager(6000)
    gui_manager = GUIManager(container_manager)
    container_manager.set_gui_manager(gui_manager)

    gui_manager.configure()
    gui_manager.window.mainloop()

if __name__ == "__main__":
    main(sys.argv)