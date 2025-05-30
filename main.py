import sys
from configurations import ConfigurationReader
from managers import ContainerManager, GUIManager

def main(argv):
    """
    Funzione principale dell'applicazione.
    Inizializza la configurazione, il gestore dei container e la GUI, poi avvia il mainloop di Tkinter.

    Args:
        argv (list of str): wrapper per sys.argv
    """
    config = ConfigurationReader()
    config.configure()
    config.readconfig('config.ini')

    container_manager = ContainerManager(int(config.configreader['configuration']['base_external_port']), config)
    gui_manager = GUIManager(container_manager)
    container_manager.set_gui_manager(gui_manager)

    gui_manager.configure()
    gui_manager.window.mainloop()

if __name__ == "__main__":
    main(sys.argv)