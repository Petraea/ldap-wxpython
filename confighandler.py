import logging, traceback
import ConfigParser

class Config:
    def __init__(self,path='default.conf'):
        self.ldapuri='ldap://'
        self.binddn=''
        self.password=''
        self.sasl='false'
        self.proto='auto'
        self.path=path
        self.load()

    def load(self):
        config = ConfigParser.ConfigParser()
        try:
            config.read(self.path)
            for f in self.__dict__.keys():
                try:
                    setattr(self,f,config.get('config',f))
                except:
                    logging.debug('No field %s defined in config.' % f)
        except:
            logging.debug('No config %s defined.' % path)

    def save(self):
        config = ConfigParser.ConfigParser()
        config.add_section('config')
        for f in self.__dict__.keys():
            if f.lower() != 'password':
                config.set('config',f,getattr(self,f))
        try:
            with open(self.path,'w') as f:
                config.write(f)
                logging.debug('Config saved to %s' % self.path)
        except:
            logging.error('Cannot save config to %s' % self.path)
            logging.debug(traceback.format_exc())

    def __str__(self):
        ret='CONFIG: '
        fields = ['%s:%s' % (f, getattr(self,f)) for f in self.__dict__.keys()]
        ret = ret + ' '.join(fields)
        return ret
