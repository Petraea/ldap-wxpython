import wx
from connectdialog import ConnectDialog
from treebrowser import TreeBrowser
from infopane import InfoPane

ID_CONNECT=10
ID_DISCONNECT=20
ID_SPLITTER=100

class LdapBrowser(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, -1, 'LDAP Browser')

        self.splitter = wx.SplitterWindow(self, ID_SPLITTER, style=wx.SP_BORDER)
        self.splitter.SetMinimumPaneSize(50)

        p1 = TreeBrowser(self.splitter, -1)
        p2 = InfoPane(self.splitter, -1)
        self.splitter.SplitVertically(p1, p2)

        servermenu= wx.Menu()
        servermenu.Append(ID_CONNECT,"C&onnect"," Connect to a server")
        servermenu.Append(ID_DISCONNECT,"D&isconnect"," Disconnect from a server")

        menuBar = wx.MenuBar()
        menuBar.Append(servermenu,"&Server")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.ConnectMenu, id=ID_CONNECT)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_DISCONNECT)

        self.Show(True)

    def OnExit(self,e):
        self.Close(True)

    def ConnectMenu(self,e):
        self.vals={}
        condia = ConnectDialog(self,-1)
        res = condia.ShowModal()
        if res == wx.ID_OK:
            self.vals=condia.GetValue()
        condia.Destroy()
        print(self.vals)

app = wx.App(0)
LdapBrowser(None, -1)
app.MainLoop()

