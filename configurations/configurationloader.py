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

    def configure(self):
        """
        Inizializza l'oggetto ConfigParser.
        """
        self.configreader = configparser.ConfigParser()

    def readconfig(self, configfile):
        """
        Legge il file di configurazione specificato.

        Args:
            configfile (str): Percorso del file di configurazione da leggere.
        """
        self.configreader.read(str(configfile))