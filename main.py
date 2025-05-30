import sys
from configurations import ConfigurationReader
from managers import ContainerManager, GUIManager

def main(argv):
    """main

    Args:
        argv (list of strings): wrapper for sys.argv
    """
    config = ConfigurationReader()
    config.configure()
    config.readconfig('config.ini')

    container_manager = ContainerManager(int(config.configreader['configuration']['base_port']))
    gui_manager = GUIManager(container_manager)
    container_manager.set_gui_manager(gui_manager)

    gui_manager.configure()
    gui_manager.window.mainloop()

if __name__ == "__main__":
    main(sys.argv)