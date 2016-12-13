import wx
import logging
import os, sys
from connectdialog import ConnectDialog
from treebrowser import TreeBrowser
from infopane import InfoPane
from confighandler import Config
from ldaphandler import LDAP

#Temporary testing code
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

ID_CONNECT=10
ID_DISCONNECT=20
ID_SPLITTER=100

class LdapBrowser(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, -1, 'LDAP Browser')
        self.config = Config()
        self.ldap=LDAP(self.config)

        self.splitter = wx.SplitterWindow(self, ID_SPLITTER, style=wx.SP_BORDER)
        self.splitter.SetMinimumPaneSize(50)

        p1 = TreeBrowser(self.splitter, self.ldap)
        p2 = InfoPane(self.splitter, self.ldap,p1)
        p1.infopane=p2
        self.splitter.SplitVertically(p1, p2)

        servermenu= wx.Menu()
        servermenu.Append(ID_CONNECT,"C&onnect"," Connect to a server")
        servermenu.Append(ID_DISCONNECT,"D&isconnect"," Disconnect from a server")

        menuBar = wx.MenuBar()
        menuBar.Append(servermenu,"&Server")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnConnect, id=ID_CONNECT)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_DISCONNECT)

        self.Show(True)

    def OnExit(self,e):
        self.Close(True)

    def OnConnect(self,e):
        self.vals={}
        condia = ConnectDialog(self,self.config)
        res = condia.ShowModal()
        if res == wx.ID_OK:
            condia.UpdateConfig()
            self.ldap.connect()
        condia.Destroy()

app = wx.App(0)
LdapBrowser(None, -1)
app.MainLoop()

