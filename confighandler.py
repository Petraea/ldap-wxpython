import logging
import ConfigParser

class Config:
    def __init__(self,path='default.conf'):
        self.ldapuri='ldap://'
        self.binddn=''
        self.password=None
        self.sasl=False
        self.force2=False
        self.force3=False
        self.path=path
        config = ConfigParser.ConfigParser()
        config.read(path)
        for f in self.__dict__.keys():
            try:
                setattr(self,f,config.get('config',f))
            except:
                logging.debug('No field %s defined in config.' % f)
