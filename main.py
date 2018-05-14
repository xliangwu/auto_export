import wx
from auto import DataExport
from datetime import datetime


class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(*args, **kw)

        # create a panel in the frame
        pnl = wx.Panel(self)
        self.button = wx.Button(pnl, label="导出", pos=(25, 25))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("欢迎使用工具")

    def makeMenuBar(self):
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT, '关于')

        menuBar = wx.MenuBar()
        menuBar.Append(helpMenu, "&帮助")

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.onAbout, aboutItem)

    def OnClick(self, event):
        self.SetStatusText("Click button %d\n" % event.GetId())
        DataExport()
        now = datetime.now()
        self.SetStatusText("导出数据成功 {}".format(now.strftime("%Y/%m/%d %H:%M:%S")))

    def onAbout(self, event):
        wx.MessageBox("自动导出数据工具",
                      "关于我们",
                      wx.OK | wx.ICON_INFORMATION)


if __name__ == '__main__':
    app = wx.App()
    frm = MainFrame(None, title='数据导出', size=(600, 400))
    frm.Show()
    app.MainLoop()
