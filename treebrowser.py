import wx
import logging
from ldaphandler import LDAP

class TreeBrowser(wx.TreeCtrl):
    def __init__(self, parent, ldap=None, infopane=None):
        wx.TreeCtrl.__init__(self, parent, -1, style=wx.TR_HAS_BUTTONS)
        self.tree = {}
        if not ldap:
            ldap = LDAP()
        self.ldap = ldap
        self.infopane = infopane
        if not self.ldap.connected:
            self.Disable()
        else:
            self.root = self.AddRoot(self.ldap.basedn)
            self.AppendItem(self.root,'')
            self.Bind(wx.EVT_TREE_ITEM_EXPANDING,self.OnExpand)

    def getPath(self, id):
        if id == self.root:
            return [self.GetItemText(id)]
        else:
            return [self.GetItemText(id)] + self.getPath(self.getItemParent(id))

#    def Expand(self,item):
#        logging.debug('EXPAND: %s' % repr(item))
#        wx.TreeCtrl.Expand(self,item)

    def OnExpand(self, event):
        path = self.getPath(event.GetItem())
        dn = ','.join(path)
        #Get the path to this node
        #Look up int the LDAP these children
        #Add them as my children but don't replace any already existing
        #Unless they no longer exist
        logging.debug('Expanding spotted: %s' % path)
        logging.debug(self.ldap.getChildren(dn))
#        logging.debug(self.ldap.getChildren(','.join(path)))
