import wx
import logging
from ldaphandler import LDAP

class InfoPane(wx.ListCtrl):
    def __init__(self, parent, ldap=None, treebrowser=None):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        if ldap is None:
            ldap = LDAP() 
        self.ldap = ldap
        self.treebrowser = treebrowser
        self.index=0
        self.InsertColumn(0,'Field')
        self.InsertColumn(1,'Value')

        self.SetColumnWidth(0, 220)
        self.SetColumnWidth(1, 700)

    def addLine(self, data=[]):
        columns = self.GetColumnCount()-1
        line = "Line %s" % self.index
        if len(data)> 0:
            self.InsertStringItem(self.index, data[0])
            data.pop(0)
        for c in range(min(columns,len(data))):
            self.SetStringItem(self.index, c+1, repr(data[0]))
            data.pop(0)
        self.index += 1

    def Clear(self, event=None):
        self.DeleteAllItems()
        self.index=0

    def Update(self,dn):
        attrs = self.ldap.getAttrs(dn)
        self.Clear()
        for a in attrs:
            for val in attrs[a]:
                self.addLine([a,val])
