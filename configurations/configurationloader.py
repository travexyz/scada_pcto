import os
import configparser

class ConfigurationReader:
    """
    Gestisce la lettura e la configurazione dei file INI tramite configparser.
    """
    def __init__(self):
        """
        Inizializza il ConfigurationReader senza caricare alcun file.
        """
        self.configreader = None

    def initialize_parser(self):
        """
        Inizializza l'oggetto ConfigParser.
        """
        self.configreader = configparser.ConfigParser()

    def read_config(self, configfile):
        """
        Legge il file di configurazione specificato.

        Args:
            configfile (str): Percorso del file di configurazione da leggere.
        """
        if not os.path.isfile(configfile):
            print(f'Selected configuration file ({configfile}) not found')
            return
        try:
            self.configreader.read(str(configfile))
        except configparser.ParsingError as e:
            print(f"Error: {e}")
            return
