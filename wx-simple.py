import wx
from collections import OrderedDict

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
        wx.Dialog.__init__(self, parent, -1, 'Connect')
        self.parent = parent

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(pnl, label='Connection Settings')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)

        ldapurib = wx.BoxSizer(wx.HORIZONTAL)
        ldapurib.Add(wx.StaticText(pnl, label='LDAP URI'))
        self.ldapuri = wx.TextCtrl(pnl)
        ldapurib.Add(self.ldapuri, flag=wx.LEFT, border=5)
        sbs.Add(ldapurib)

        binddnb = wx.BoxSizer(wx.HORIZONTAL)
        binddnb.Add(wx.StaticText(pnl, label='Bind DN'))
        self.binddn = wx.TextCtrl(pnl)
        binddnb.Add(self.binddn, flag=wx.LEFT, border=5)
        sbs.Add(binddnb)

        passwdb = wx.BoxSizer(wx.HORIZONTAL)
        passwdb.Add(wx.StaticText(pnl, label='Password'))
        self.passwd = wx.TextCtrl(pnl,style=wx.TE_PASSWORD)
        passwdb.Add(self.passwd, flag=wx.LEFT, border=5)
        sbs.Add(passwdb)

        self.sasl = wx.CheckBox(pnl,label='Use SASL')
        self.sasl.SetValue(False)
        self.sasl.Disable()
        sbs.Add(self.sasl)

        self.protochoices=OrderedDict([('Automatic',None),('Force 2',2),('Force 3',3)])
        self.proto = wx.RadioBox(pnl,label='Protocol',
            choices=self.protochoices.keys(),
            majorDimension = 1,style = wx.RA_SPECIFY_COLS)
        sbs.Add(self.proto)
        pnl.SetSizer(sbs)

        buttonbox = wx.BoxSizer(wx.HORIZONTAL)
        connectButton = wx.Button(self, label='Connect')
        closeButton = wx.Button(self, label='Close')
        buttonbox.Add(connectButton)
        buttonbox.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(buttonbox,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)
        self.Fit()
        connectButton.Bind(wx.EVT_BUTTON, self.OnConnect)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

        self.ShowModal()

    def OnConnect(self, e):
        print(self.passwd.GetValue())
        print(self.ldapuri.GetValue())
        print(self.binddn.GetValue())
        print(self.sasl.GetValue())
        print(self.proto.GetSelection())
        print(self.protochoices.values())
        print(self.protochoices.values()[self.proto.GetSelection()])
        self.Destroy()

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

