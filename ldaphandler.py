import logging, sys
import traceback
import ldap
from confighandler import Config

class LDAP:
    def __init__(self,config=None):
        if config is None:
            config=Config()
        self.config=config
        self.connected=False
        self.connect()

    def connect(self):
        try:
            self.ldap = ldap.initialize(self.config.ldapuri)
            self.ldap.set_option(ldap.OPT_REFERRALS, 0)
            logging.debug('LDAP initialised from URI %s' % self.config.ldapuri)
            try:
                self.ldap.simple_bind_s(self.config.binddn,self.config.password)
                logging.debug('LDAP bound to bindDN %s' % self.config.binddn)
                try:
                    # Trick from https://www.ibm.com/developerworks/aix/library/au-ldap_crud/
                    #to find basedn via the root DSE
                    #This is valid in LDAP, not AD
                    rootdse = self.ldap.search_s("",ldap.SCOPE_BASE,attrlist=['+'])
                    self.basedns = rootdse[0][1]['namingContexts']
                    logging.debug('LDAP baseDNs are %s' % self.basedns)
                    self.connected = True
                except:
                    try:
                        #This is valid in AD, not LDAP
                        rootdse = self.ldap.search_s("",ldap.SCOPE_BASE,'(objectclass=*)')
                        self.basedns = rootdse[0][1]['namingContexts']
                        logging.debug('LDAP baseDNs are %s' % self.basedns)
                        self.connected = True
                    except:
                        logging.error('LDAP baseDNs not found.')
                        logging.debug(traceback.format_exc())
            except:
                logging.error('LDAP not bound to bindDN %s' % self.config.binddn)
                logging.debug(traceback.format_exc())
        except:
            logging.error('LDAP not initialised. URI: %s' % self.config.ldapuri)
            logging.debug(traceback.format_exc())

    def getChildren(self,dn):
        '''Wrapper function for treebrowsing. Just get me the DNs that are under this one.'''
        res = [x[0] for x in self.ldap.search_s(dn,ldap.SCOPE_ONELEVEL,attrlist=['dn'])]
        #This needs paged results.
        res = [x for x in res if x is not None]
        res = [x[:-len(dn)-1] for x in res]
        return res

    def getAttrs(self,dn):
        '''Wrapper function for objectviewing.'''
        res = self.ldap.search_s(dn,ldap.SCOPE_BASE)
        return res[0][1]

    def replaceAttrs(self,dn,attrs):
        '''Wrapper function for modifications. Will entirely replace attributes, removing non-existent ones.'''
        curattrs=self.getAttrs(dn).keys()
        newattrs={x:attrs[x] for x in attrs if x not in curattrs}
        modattrs={x:attrs[x] for x in attrs if x in curattrs}
        delattrs={x:attrs[x] for x in curattrs if x not in attrs}
        #do modify_s functions

    def modifyAttrs(self,dn,attrs):
        '''Wrapper function for modifications. Will add or modify existing attrs, but not delete.'''
        curattrs=self.getAttrs(dn).keys()
        newattrs={x:attrs[x] for x in attrs if x not in curattrs}
        modattrs={x:attrs[x] for x in attrs if x in curattrs}
        #do modify_s functions

    def deleteAttrs(self,dn,attrs):
        '''Wrapper function for modifications. Will only delete attributes.'''
        curattrs=self.getAttrs(dn).keys()
        delattrs={x:attrs[x] for x in curattrs if x not in attrs}
        #do modify_s functions

    def deleteObject(self,dn):
        '''Wrapper function for modifications. Delete entire object.'''
        #do delete_s functions

    def createObject(self,dn,attrs={}):
        '''Wrapper function for modifications. Adds entire object, with optional attributes set.'''
        #do add_s functions

    def copyObject(self,olddn,newdn):
        '''Wrapper function for modifications. Copies entire object.'''
        self.createObject(newdn,self.getAttrs(olddn))

    def moveObject(self,olddn,newdn):
        '''Wrapper function for modifications. Moves an object.'''
        #do rename_s functions


#Test code
if __name__ == '__main__':

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    l = LDAP()
    la = l.getChildren(l.basedns[0])
    print(la)
    a=[x for x in la if x.lower().startswith('ou=')][0]+','+l.basedns[0]
    print(a)
    lb = l.getChildren(a)
    print(lb)
    b=[x for x in la if x.lower().startswith('cn=')][0]+','+a
    print(l.getAttrs(b))

