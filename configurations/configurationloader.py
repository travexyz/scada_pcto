import configparser

class ConfigurationReader:
    def __init__(self):
        self.configreader = None

    def configure(self):
        self.configreader = configparser.ConfigParser()

    def readconfig(self, configfile):
        self.configreader.read(str(configfile))