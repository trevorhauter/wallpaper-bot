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

from pathlib import Path

import json

from main import redditCollector
from settings import user_profile

profile = user_profile()


class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=wx.EmptyString,
            pos=wx.DefaultPosition,
            size=wx.Size(600, 500),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        # Get the settings
        settings = profile.settings
        # Set the values that will be displayed in our fields

        if settings and "subreddit" in settings:
            sub_selector_value = settings["subreddit"]
            sort_selector_value = settings["sort-by"]
            wallpapers_requested_value = str(settings["wallpapers_requested"])
            resolutions = settings["resolutions"]
            check_duplicates_value = settings["check_for_duplicates"]
        else:
            sub_selector_value = ""
            sort_selector_value = ""
            wallpapers_requested_value = ""
            resolutions = ""
            check_duplicates_value = False

        if settings and "file_path" in settings:
            self.file_path = settings["file_path"]
        else:
            self.file_path = ""


        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.sub_selector = wx.StaticText(
            self, wx.ID_ANY, "Subreddit", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.sub_selector.Wrap(-1)

        bSizer1.Add(self.sub_selector, 0, wx.ALL, 5)

        subreddit_choices = ["Wallpapers", "Art"]
        # Check to see if the user added their own wallpapers with a json file
        if Path("subreddits.json").is_file():
            with open("subreddits.json", "r") as subreddits_file:
                subreddits = json.load(subreddits_file)
            if subreddits:
                subreddit_choices = list(set(subreddits + subreddit_choices))
                print(subreddit_choices)

        sub_selectorChoices = subreddit_choices
        # Sets the subreddit selector to the users last value if any
        self.sub_selector = wx.ComboBox(
            self,
            wx.ID_ANY,
            sub_selector_value,
            wx.DefaultPosition,
            wx.DefaultSize,
            sub_selectorChoices,
            0,
        )
        bSizer1.Add(self.sub_selector, 0, wx.ALL, 5)

        self.amount_label = wx.StaticText(
            self, wx.ID_ANY, "# Of Wallpapers", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.amount_label.Wrap(-1)

        bSizer1.Add(self.amount_label, 0, wx.ALL, 5)
        # Sets the wallpaper requested textctrl to the users last value if any
        self.wallpapers_requested = wx.TextCtrl(
            self,
            wx.ID_ANY,
            wallpapers_requested_value,
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        bSizer1.Add(self.wallpapers_requested, 0, wx.ALL, 5)

        gSizer1.Add(bSizer1, 1, wx.EXPAND, 5)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.sort_label = wx.StaticText(
            self, wx.ID_ANY, "Sort By", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.sort_label.Wrap(-1)

        bSizer2.Add(self.sort_label, 0, wx.ALL, 5)

        sort_selectorChoices = ["New", "Hot", "Random", "Rising"]
        # Sets the sort selector to the users last value if any
        self.sort_selector = wx.ComboBox(
            self,
            wx.ID_ANY,
            sort_selector_value,
            wx.DefaultPosition,
            wx.DefaultSize,
            sort_selectorChoices,
            0,
        )
        bSizer2.Add(self.sort_selector, 0, wx.ALL, 5)

        self.resolution_label = wx.StaticText(
            self, wx.ID_ANY, "Resolution", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.resolution_label.Wrap(-1)

        bSizer2.Add(self.resolution_label, 0, wx.ALL, 5)

        # Create a container to contain all of the resolution choices
        self.resolution_checkbox_container = wx.GridSizer( 0, 2, 0, 0 )
        self.resolution_selectorChoices = [
            "1280x720",
            "1366x768",
            "1440x900",
            "1536x864",
            "1920x1080",
            "2560x1440",
            "3840x2160",
        ]
        # Create a variable to contain all the checkboxes so we can interact with them later
        self.resolution_choices = []
        # Create the checkboxes and store them in the variable
        for choice in self.resolution_selectorChoices:
            check_box = wx.CheckBox(self, wx.ID_ANY, choice, wx.DefaultPosition, wx.DefaultSize, 0)
            if choice in resolutions:
                check_box.SetValue(1)
            self.resolution_checkbox_container.Add(check_box, 0, wx.ALL, 5)
            self.resolution_choices.append(check_box)
        
        self.resolution_checkbox_container.AddSpacer(wx.EXPAND)


        self.select_all = wx.Button(
            self, wx.ID_ANY, "Select All", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.select_all.Bind(wx.EVT_BUTTON, self.select_all_resolutions)
        self.resolution_checkbox_container.Add(self.select_all, 0, wx.ALL, 5)

        self.deselect_all = wx.Button(
            self, wx.ID_ANY, "Deselect All", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.deselect_all.Bind(wx.EVT_BUTTON, self.deselect_all_resolutions)
        self.resolution_checkbox_container.Add(self.deselect_all, 0, wx.ALL, 5)

        bSizer2.Add(self.resolution_checkbox_container, 1, wx.EXPAND, 5)
        gSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        bSizer3.Add((0, 0), 1, wx.EXPAND, 5)

        self.dir_selector_label = wx.StaticText(
            self,
            wx.ID_ANY,
            "Wallpaper Directory",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.dir_selector_label.Wrap(-1)

        bSizer3.Add(self.dir_selector_label, 0, wx.ALL, 5)

        self.directory_selector = wx.Button(
            self, wx.ID_ANY, "Select Directory", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.directory_selector.Bind(wx.EVT_BUTTON, self.dirBrowser)
        bSizer3.Add(self.directory_selector, 0, wx.ALL, 5)

        self.duplicate_label = wx.StaticText(
            self,
            wx.ID_ANY,
            "Check For Duplicates",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.duplicate_label.Wrap(-1)

        bSizer3.Add(self.duplicate_label, 0, wx.ALL, 5)

        self.duplicate_checkbox = wx.CheckBox(
            self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, 0
        )
        # Sets the duplicate checkbox to the users last value if any
        self.duplicate_checkbox.SetValue(check_duplicates_value)
        bSizer3.Add(self.duplicate_checkbox, 0, wx.ALL, 5)

        bSizer3.Add((0, 0), 1, wx.EXPAND, 5)

        gSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        bSizer4.Add((0, 0), 1, wx.EXPAND, 5)

        self.run_button = wx.Button(
            self, wx.ID_ANY, "Get Wallpapers", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.run_button.Bind(wx.EVT_BUTTON, self.run)
        bSizer4.Add(self.run_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer4.Add((0, 0), 1, wx.EXPAND, 5)

        gSizer1.Add(bSizer4, 1, wx.EXPAND, 5)

        self.SetSizer(gSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

    """
    ---------------------------
    END OF WX PYTHON FORM BUILDING - BEGINNING OF FUNCTIONS USED TO INTERACT WITH COLLECTION
    ---------------------------
    """

    def dirBrowser(self, event):
        dialog = wx.DirDialog(None, message="Pick a directory.")
        if dialog.ShowModal() == wx.ID_OK:
            print(f"Default directory has been changed to {dialog.GetPath()}")
            self.file_path = dialog.GetPath()
            profile.save_settings(file_path=dialog.GetPath())
        else:
            pass
        dialog.Destroy()


    def select_all_resolutions(self, event):
        # Selects all of the resolution checkboxes
        for choice in self.resolution_choices:
            choice.SetValue(1)

    def deselect_all_resolutions(self, event):
        # Unchecks all of the resolution checkboxes
        for choice in self.resolution_choices:
            choice.SetValue(0)

    def run(self, event):
        """
        This function is called when "Get Wallpapers" is clicked. We validate the form, and it valid, we pass it to the collector to do it's job.
        """

        def get_requested_resolutions():
            requested_resolutions = []
            for choice in self.resolution_choices:
                if choice.GetValue() == 1:
                    requested_resolutions.append(choice.GetLabel())
            return requested_resolutions

        required_form_values = [
            self.sub_selector.GetValue(),
            self.sort_selector.GetValue(),
            get_requested_resolutions(),
            self.wallpapers_requested.GetValue(),
        ]

        req = int(self.wallpapers_requested.GetValue())

        # If a required field is left incomplete, don't collect anything
        if any(not val for val in required_form_values):
            print("You have to select a resolution or something idk you're just missing something dude")
            return False
        
        form = {
            "subreddit": required_form_values[0],
            "sort-by": required_form_values[1],
            "resolutions": required_form_values[2],
            "wallpapers_requested": int(required_form_values[3]),
            "check_for_duplicates": self.duplicate_checkbox.GetValue(),
        }

        profile.save_settings(form=form)

        print("Starting")
        progress_bar = wx.ProgressDialog(
            " Running...",
            "Retrieving wallpapers from reddit... Whatever that is...",
            maximum=req,
            parent=None,
            style=wx.PD_AUTO_HIDE | wx.PD_APP_MODAL | wx.PD_SMOOTH,
        )
        progress_bar.Update(1, "Downloading wallpaper #" + str(1))

        print(form)
        col = redditCollector(form, self.file_path)
        progress = col.collect_wallpapers()

        for group in progress:
            for count in group:
                progress_bar.Update(count, "Downloading wallpaper #" + str(count))

        progress_bar.Destroy()

    def __del__(self):
        pass


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show(True)
    app.MainLoop()
