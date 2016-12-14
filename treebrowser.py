import wx
import logging
from ldaphandler import LDAP

class TreeBrowser(wx.TreeCtrl):
    def __init__(self, parent, ldap=None, infopane=None):
        wx.TreeCtrl.__init__(self, parent, -1, style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT)
        self.tree = {}
        if not ldap:
            ldap = LDAP()
        self.ldap = ldap
        self.infopane = infopane
        if not self.ldap.connected:
            self.Disable()
        else:
            self._root = self.AddRoot('')
            self.roots = [self.AppendItem(self._root,basedn) for basedn in self.ldap.basedns]
            for r in self.roots:
                self.AppendItem(r,'')
            self.Bind(wx.EVT_TREE_ITEM_EXPANDING,self.OnExpand)
            self.Bind(wx.EVT_TREE_SEL_CHANGED,self.OnSelect)

    def getPath(self, id):
        if id in self.roots:
            return [id]
        else:
            return [id] + self.getPath(self.GetItemParent(id))

    def getDirectChildren(self,id):
        children = self.GetChildrenCount(id)
        if children == 0: return []
        cid, cookie = self.GetFirstChild(id)
        ids = []
        while cid.IsOk():
            ids.append(cid)
            cid, cookie = self.GetNextChild(id, cookie)
        return ids

    def OnExpand(self, event):
        id = event.GetItem()
        path = self.getPath(id)
        logging.debug('Expanding spotted: %s' % path)
        dn = ','.join([self.GetItemText(i) for i in path])

        lchildren = self.ldap.getChildren(dn)
        tchildren = {self.GetItemText(x):x for x in self.getDirectChildren(id)}
        addchildren = [x for x in lchildren if x not in tchildren]
        rmchildren = [x for x in tchildren if x not in lchildren]
        remchildren = [tchildren[x] for x in rmchildren]
        for child in addchildren:
            if child is not None:
                logging.debug('Adding child: %s' % child)
                newid = self.AppendItem(path[0],child)
                if not child.lower().startswith('cn='):
                    #Or if objectClass: container - THESE HAVE CONTENTS
                    self.AppendItem(newid,'')
        for child in remchildren:
            if child is not None:
                logging.debug('Removing child: %s' % child)
                self.Delete(child)


    def OnSelect(self, event):
        id = event.GetItem()
        path = [self.GetItemText(x) for x in self.getPath(id)]
        self.infopane.Update(','.join(path))
