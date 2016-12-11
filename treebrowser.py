import wx

class TreeBrowser(wx.TreeCtrl):
    def __init__(self, parent, id):
        wx.TreeCtrl.__init__(self, parent, id, style=wx.TR_HAS_BUTTONS)

        r = self.AddRoot('test')
        self.AppendItem(r,'test2')
