import logging, sys
import ldap
from confighandler import Config

#Temporary testing code
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

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

    def getChildren(self,dn):
        '''Wrapper function for treebrowsing. Just get me the DNs that are under this one.'''
        res = [x[0] for x in self.ldap.search_s(dn,ldap.SCOPE_ONELEVEL,attrlist=['dn'])]
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
        return None

    def modifyAttrs(self,dn,attrs):
        '''Wrapper function for modifications. Will add or modify existing attrs, but not delete.'''
        curattrs=self.getAttrs(dn).keys()
        newattrs={x:attrs[x] for x in attrs if x not in curattrs}
        modattrs={x:attrs[x] for x in attrs if x in curattrs}
        #do modify_s functions
        return None

    def deleteAttrs(self,dn,attrs):
        '''Wrapper function for modifications. Will only delete attributes.'''
        curattrs=self.getAttrs(dn).keys()
        delattrs={x:attrs[x] for x in curattrs if x not in attrs}
        #do modify_s functions
        return None

    def deleteObject(self,dn):
        '''Wrapper function for modifications. Delete entire object.'''
        #do delete_s functions
        return None

    def createObject(self,dn,attrs={}):
        '''Wrapper function for modifications. Adds entire object, with optional attributes set.'''
        #do add_s functions
        return None

    def copyObject(self,olddn,newdn):
        '''Wrapper function for modifications. Copies entire object.'''
        self.createObject(newdn,self.getAttrs(olddn))
        return None

    def moveObject(self,olddn,newdn):
        '''Wrapper function for modifications. Moved an object.'''
        #do rename_s functions
        return None


l = LDAP()
print(l.getChildren(l.basedn))
a = l.getChildren(l.basedn)[1]
print(l.getChildren(a))
b = l.getChildren(a)[2]
print(l.getAttrs(b))

