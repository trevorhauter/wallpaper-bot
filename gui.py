
# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-39-g978478d5)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame
###########################################################################

import time

from main import redditCollector

class MyFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,350 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        gSizer1 = wx.GridSizer( 0, 2, 0, 0 )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.sub_selector = wx.StaticText( self, wx.ID_ANY, u"Subreddit", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.sub_selector.Wrap( -1 )

        bSizer1.Add( self.sub_selector, 0, wx.ALL, 5 )

        sub_selectorChoices = ["Wallpapers", "Art"]
        self.sub_selector = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, sub_selectorChoices, 0 )
        bSizer1.Add( self.sub_selector, 0, wx.ALL, 5 )

        self.amount_label = wx.StaticText( self, wx.ID_ANY, u"# Of Wallpapers", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.amount_label.Wrap( -1 )

        bSizer1.Add( self.amount_label, 0, wx.ALL, 5 )

        self.wallpapers_requested = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.wallpapers_requested, 0, wx.ALL, 5 )


        gSizer1.Add( bSizer1, 1, wx.EXPAND, 5 )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.sort_label = wx.StaticText( self, wx.ID_ANY, u"Sort By", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.sort_label.Wrap( -1 )

        bSizer2.Add( self.sort_label, 0, wx.ALL, 5 )

        sort_selectorChoices = ["New", "Hot"]
        self.sort_selector = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, sort_selectorChoices, 0 )
        bSizer2.Add( self.sort_selector, 0, wx.ALL, 5 )

        self.resolution_label = wx.StaticText( self, wx.ID_ANY, u"Resolution", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.resolution_label.Wrap( -1 )

        bSizer2.Add( self.resolution_label, 0, wx.ALL, 5 )

        resolution_selectorChoices = ["1920x1080"]
        self.resolution_selector = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, resolution_selectorChoices, 0 )
        bSizer2.Add( self.resolution_selector, 0, wx.ALL, 5 )


        gSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )


        bSizer3.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.dir_selector_label = wx.StaticText( self, wx.ID_ANY, u"Wallpaper Directory", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.dir_selector_label.Wrap( -1 )

        bSizer3.Add( self.dir_selector_label, 0, wx.ALL, 5 )

        self.directory_selector = wx.ToggleButton( self, wx.ID_ANY, u"Select Directory", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.directory_selector, 0, wx.ALL, 5 )

        self.duplicate_label = wx.StaticText( self, wx.ID_ANY, u"Check For Duplicates", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.duplicate_label.Wrap( -1 )

        bSizer3.Add( self.duplicate_label, 0, wx.ALL, 5 )

        self.duplicate_checkbox = wx.CheckBox( self, wx.ID_ANY, u"Check Me!", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.duplicate_checkbox, 0, wx.ALL, 5 )


        bSizer3.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        gSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )

        bSizer4 = wx.BoxSizer( wx.VERTICAL )


        bSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        self.run_button = wx.Button( self, wx.ID_ANY, u"Get Wallpapers", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.run_button.Bind(wx.EVT_BUTTON, self.run)
        bSizer4.Add( self.run_button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        bSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        gSizer1.Add( bSizer4, 1, wx.EXPAND, 5 )


        self.SetSizer( gSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

    """
    ---------------------------
    END OF WX PYTHON FORM BUILDING - BEGINNING OF FUNCTIONS USED TO INTERACT WITH COLLECTION
    ---------------------------
    """

    def run(self, event):
        """
        This function is called when "Get Wallpapers" is clicked. We validate the form, and it valid, we pass it to the collector to do it's job.
        """
        required_form_values = [
            self.sub_selector.GetValue(),
            self.sort_selector.GetValue(),
            self.resolution_selector.GetValue(),
            self.wallpapers_requested.GetValue()
        ]

        req = int(self.wallpapers_requested.GetValue())

        # If a required field is left incomplete, don't collect anything
        if any(val == '' for val in required_form_values):
            return False

        form = {
            'subreddit': required_form_values[0],
            'sort-by': required_form_values[1],
            'resolution': required_form_values[2],
            'wallpapers_requested': int(required_form_values[3]),
            'check_for_duplicates': self.duplicate_checkbox.GetValue()
        }
        
        print("Starting")
        progress_bar = wx.ProgressDialog(" Running...", "Logging into the cabinet...", maximum=req, parent=None, style= wx.PD_AUTO_HIDE | wx.PD_APP_MODAL | wx.PD_SMOOTH)
        progress_bar.Update(1, "Downloading wallpaper #" + str(1))

        print(form)
        col = redditCollector(form)
        progress = col.collect_wallpapers()

        for group in progress:
            for count in group:
                progress_bar.Update(count, "Downloading wallpaper #" + str(count))

        progress_bar.Destroy()

    def __del__( self ):
        pass


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show(True)
    app.MainLoop()