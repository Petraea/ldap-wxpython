import wx

class InfoPane(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.InsertColumn(0,'Field')
        self.InsertColumn(1,'Value')

        self.SetColumnWidth(0, 220)
        self.SetColumnWidth(1, 70)
