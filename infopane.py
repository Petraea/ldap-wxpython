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
        self.InsertColumn(0,'Field')
        self.InsertColumn(1,'Value')

        self.SetColumnWidth(0, 220)
        self.SetColumnWidth(1, 70)
