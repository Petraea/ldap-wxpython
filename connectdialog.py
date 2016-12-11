import wx
from collections import OrderedDict

class ConnectDialog(wx.Dialog):
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
        connectButton = wx.Button(self, wx.ID_OK, label='Connect')
        closeButton = wx.Button(self, wx.ID_CANCEL, label='Cancel')
        buttonbox.Add(connectButton)
        buttonbox.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(buttonbox,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)
        self.Fit()

    def GetValue(self):
        val={}
        val['password'] = self.passwd.GetValue()
        val['ldapuri'] = self.ldapuri.GetValue()
        val['binddn'] = self.binddn.GetValue()
        val['sasl'] = self.sasl.GetValue()
        val['proto'] = self.protochoices.values()[self.proto.GetSelection()]
        return val
