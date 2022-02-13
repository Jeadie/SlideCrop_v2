import sys
import os
pkgs = os.path.abspath(".venw/lib/python2.7/site-packages/")
sys.path.append(pkgs)

import wx
from autoanalysis import App

if __name__ == "__main__":
    app = wx.App()
    frame = App.AppFrame()
    app.MainLoop()

