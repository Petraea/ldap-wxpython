import wx

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

class ConnectWindow(wx.Dialog):
    def __init__(self, parent, id):
        wx.Dialog.__init__(self, parent, -1, 'Connect to a Server')

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(pnl, label='Connection Settings')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)

        ldapuri = wx.BoxSizer(wx.HORIZONTAL)
        ldapuri.Add(wx.StaticText(pnl, label='LDAP URI'))
        ldapuri.Add(wx.TextCtrl(pnl), flag=wx.LEFT, border=5)
        sbs.Add(ldapuri)

        binddn = wx.BoxSizer(wx.HORIZONTAL)
        binddn.Add(wx.StaticText(pnl, label='Bind DN'))
        binddn.Add(wx.TextCtrl(pnl), flag=wx.LEFT, border=5)
        sbs.Add(binddn)

        passwd = wx.BoxSizer(wx.HORIZONTAL)
        passwd.Add(wx.StaticText(pnl, label='Password'))
        passwd.Add(wx.TextCtrl(pnl,style=wx.TE_PASSWORD), flag=wx.LEFT, border=5)
        sbs.Add(passwd)

        sasl = wx.CheckBox(pnl,label='Use SASL')
        sasl.SetValue(False)
        sasl.Disable()
        sbs.Add(sasl)

        sbs.Add(wx.RadioBox(pnl,label='Protocol',choices=['Automatic','Force 2','Force 3'],
                majorDimension = 1,style = wx.RA_SPECIFY_COLS))
        pnl.SetSizer(sbs)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)
        self.Fit()
        okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

        self.ShowModal()

    def OnClose(self, e):
        self.Destroy()

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
        chgdep = ConnectWindow(self,-1)

app = wx.App(0)
LdapBrowser(None, -1)
app.MainLoop()

