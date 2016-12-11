import logging, sys
import ldap
import ConfigParser

#Temporary testing code
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

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

class LDAP:
    def __init__(self,config=None):
        if config is None:
            config=Config()
        self.config=config
        self.ldap = ldap.initialize(config.ldapuri)
        self.ldap.simple_bind_s(config.binddn,config.password)
        # Trick from https://www.ibm.com/developerworks/aix/library/au-ldap_crud/
        #to find basedn via the root DSE
        rootdse = self.ldap.search_s('',ldap.SCOPE_BASE,'(objectclass=*)',['namingContexts'])
        self.basedn = rootdse[0][1]['namingContexts'][0]

#Attempt to find base dc with nothing
l = LDAP()
print (l.ldap.search_s(l.basedn,ldap.SCOPE_SUBTREE,'(objectClass=*)'))
