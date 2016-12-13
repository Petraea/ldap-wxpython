import wx
import logging
import os
from collections import OrderedDict
from confighandler import Config

class ConnectDialog(wx.Dialog):
    def __init__(self, parent, config=None):
        wx.Dialog.__init__(self, parent, -1, 'Connect')
        self.parent = parent
        if config is None:
            config=Config()
        self.config=config
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
        binddnb.Add(wx.StaticText(pnl, label='Bind DN/login'))
        self.binddn = wx.TextCtrl(pnl)
        binddnb.Add(self.binddn, flag=wx.LEFT, border=5)
        sbs.Add(binddnb)

        passwdb = wx.BoxSizer(wx.HORIZONTAL)
        passwdb.Add(wx.StaticText(pnl, label='Password'))
        self.passwd = wx.TextCtrl(pnl,style=wx.TE_PASSWORD)
        passwdb.Add(self.passwd, flag=wx.LEFT, border=5)
        sbs.Add(passwdb)

        self.sasl = wx.CheckBox(pnl,label='Use SASL')
        self.sasl.Disable()
        sbs.Add(self.sasl)

        self.protochoices=OrderedDict([('Automatic','auto'),('Force 2','2'),('Force 3','3')])
        self.proto = wx.RadioBox(pnl,label='Protocol',
            choices=self.protochoices.keys(),
            majorDimension = 1,style = wx.RA_SPECIFY_COLS)
        sbs.Add(self.proto)
        pnl.SetSizer(sbs)

        buttonbox = wx.BoxSizer(wx.HORIZONTAL)
        connectButton = wx.Button(self, wx.ID_OK, label='Connect')
        loadButton = wx.Button(self, wx.ID_SAVE, label='Load')
        saveButton = wx.Button(self, wx.ID_SAVE, label='Save')
        saveAsButton = wx.Button(self, wx.ID_SAVEAS, label='Save As')
        closeButton = wx.Button(self, wx.ID_CANCEL, label='Cancel')
        buttonbox.Add(connectButton)
        buttonbox.Add(loadButton, flag=wx.LEFT, border=5)
        buttonbox.Add(saveButton, flag=wx.LEFT, border=5)
        buttonbox.Add(saveAsButton, flag=wx.LEFT, border=5)
        buttonbox.Add(closeButton, flag=wx.LEFT, border=5)
        loadButton.Bind(wx.EVT_BUTTON, self.OnLoad)
        saveButton.Bind(wx.EVT_BUTTON, self.OnSave)
        saveAsButton.Bind(wx.EVT_BUTTON, self.OnSaveAs)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(buttonbox,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.LoadValues()
        self.SetSizer(vbox)
        self.Fit()

    def LoadValues(self):
        self.binddn.SetValue(self.config.binddn)
        self.ldapuri.SetValue(self.config.ldapuri)
        self.passwd.SetValue(self.config.password)
        if self.config.sasl.lower() == 'false':
            self.sasl.SetValue(False)
        else:
            self.sasl.SetValue(False)
        if self.config.proto in self.protochoices.values():
            self.proto.SetSelection(self.protochoices.values().index(self.config.proto))

    def OnLoad(self, event):
        self.dirname = "";

        loadFileDialog = wx.FileDialog(self, "Save Connection File As", self.dirname, "",
            "Connection Config Files (*.conf)|*.conf|All Files (*.*)|*.*", 
            wx.FD_OPEN)

        if loadFileDialog.ShowModal() == wx.ID_OK:
            self.filename = loadFileDialog.GetFilename()
            self.dirname = loadFileDialog.GetDirectory()
            self.config.path = os.path.join(self.dirname, self.filename)
            self.config.load()
            self.LoadValues()
        loadFileDialog.Destroy()

    def OnSave(self, event):
        self.config.save()

    def OnSaveAs(self, event):
        self.UpdateConfig()
        saveAsFileDialog = wx.FileDialog(self, "Save Connection File As", self.dirname, "",
            "Connection Config Files (*.conf)|*.conf|All Files (*.*)|*.*", 
            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if saveAsFileDialog.ShowModal() == wx.ID_OK:
            self.filename = saveAsFileDialog.GetFilename()
            self.dirname = saveAsFileDialog.GetDirectory()
            self.config.path = os.path.join(self.dirname, self.filename)
            self.config.save()
        saveAsFileDialog.Destroy()

    def UpdateConfig(self, e=''):
        self.config.password = self.passwd.GetValue()
        self.config.ldapuri = self.ldapuri.GetValue()
        self.config.binddn = self.binddn.GetValue()
        self.config.sasl = str(self.sasl.GetValue()).lower()
        self.config.proto = self.protochoices.values()[self.proto.GetSelection()]

    def GetValue(self):
        self.UpdateConfig()
        return self.config
