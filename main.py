import sys
from configurations import ConfigurationReader
from managers import ContainerManager, GUIManager, HelperThreads

CONFIG_FILE = 'config.ini'

def main(argv):
    """
    Funzione principale dell'applicazione.
    Inizializza la configurazione, il gestore dei container e la GUI, poi avvia il mainloop di Tkinter.

    Args:
        argv (list of str): wrapper per sys.argv
    """

    # Inizializzazione della configurazione
    config = ConfigurationReader()
    config.initialize_parser()
    config.read_config(CONFIG_FILE)

    container_manager = ContainerManager(int(config.configreader['configuration']['base_external_port']), config)

    helper_threads = HelperThreads(container_manager)
    gui_manager = GUIManager(container_manager, helper_threads)

    helper_threads.set_gui_manager(gui_manager)
    container_manager.set_gui_manager(gui_manager)

    # Inizializzazione della GUI
    gui_manager.configure()
    gui_manager.window.mainloop()

if __name__ == "__main__":
    main(sys.argv)