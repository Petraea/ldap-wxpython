import wx
from connectdialog import ConnectDialog

ID_CONNECT=10
ID_DISCONNECT=20
ID_SPLITTER=100

class TreeBrowser(wx.TreeCtrl):
    def __init__(self, parent, id):
        wx.TreeCtrl.__init__(self, parent, id, style=wx.TR_HAS_BUTTONS)

        r = self.AddRoot('test')
        self.AppendItem(r,'test2')

class InfoPane(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.InsertColumn(0,'Field')
        self.InsertColumn(1,'Value')

        self.SetColumnWidth(0, 220)
        self.SetColumnWidth(1, 70)

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

