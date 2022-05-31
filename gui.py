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
            self.sub_selector_value = settings["subreddit"]
            sort_selector_value = settings["sort-by"]
            wallpapers_requested_value = str(settings["wallpapers_requested"])
            resolutions = settings["resolutions"]
            check_duplicates_value = settings["check_for_duplicates"]
        else:
            self.sub_selector_value = ""
            sort_selector_value = ""
            wallpapers_requested_value = ""
            resolutions = ""
            check_duplicates_value = False

        if settings and "file_path" in settings:
            self.file_path = settings["file_path"]
        else:
            self.file_path = ""

        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.sub_selector_label = wx.StaticText(
            self.m_panel1, wx.ID_ANY, "Subreddit", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.sub_selector_label.Wrap(-1)

        bSizer1.Add(self.sub_selector_label, 0, wx.ALL, 5)

        # Get all the subreddits from the local json file
        self.subreddit_choices = profile.read_subreddits()
        sub_selectorChoices = self.subreddit_choices
        # Sets the subreddit selector to the users last value if any
        self.sub_selector = wx.ComboBox(
            self.m_panel1,
            wx.ID_ANY,
            self.sub_selector_value,
            wx.DefaultPosition,
            wx.DefaultSize,
            sub_selectorChoices,
            0,
        )
        bSizer1.Add(self.sub_selector, 0, wx.ALL, 5)

        self.amount_label = wx.StaticText(
            self.m_panel1, wx.ID_ANY, "# Of Wallpapers", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.amount_label.Wrap(-1)

        bSizer1.Add(self.amount_label, 0, wx.ALL, 5)
        # Sets the wallpaper requested textctrl to the users last value if any
        self.wallpapers_requested = wx.TextCtrl(
            self.m_panel1,
            wx.ID_ANY,
            wallpapers_requested_value,
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        bSizer1.Add(self.wallpapers_requested, 0, wx.ALL, 5)

        self.edit_subreddits_button = wx.Button(
            self.m_panel1, wx.ID_ANY, "Edit Subreddits", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.edit_subreddits_button.Bind(wx.EVT_BUTTON, self.switch_to_edit_subreddits)
        bSizer1.Add(self.edit_subreddits_button, 0, wx.ALL, 5)

        gSizer1.Add(bSizer1, 1, wx.EXPAND, 5)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.sort_label = wx.StaticText(
            self.m_panel1, wx.ID_ANY, "Sort By", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.sort_label.Wrap(-1)

        bSizer2.Add(self.sort_label, 0, wx.ALL, 5)

        sort_selectorChoices = ["New", "Hot", "Random", "Rising"]
        # Sets the sort selector to the users last value if any
        self.sort_selector = wx.ComboBox(
            self.m_panel1,
            wx.ID_ANY,
            sort_selector_value,
            wx.DefaultPosition,
            wx.DefaultSize,
            sort_selectorChoices,
            0,
        )
        bSizer2.Add(self.sort_selector, 0, wx.ALL, 5)

        self.resolution_label = wx.StaticText(
            self.m_panel1, wx.ID_ANY, "Resolution", wx.DefaultPosition, wx.DefaultSize, 0
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
            check_box = wx.CheckBox(self.m_panel1, wx.ID_ANY, choice, wx.DefaultPosition, wx.DefaultSize, 0)
            if choice in resolutions:
                check_box.SetValue(1)
            self.resolution_checkbox_container.Add(check_box, 0, wx.ALL, 5)
            self.resolution_choices.append(check_box)
        
        self.resolution_checkbox_container.AddSpacer(wx.EXPAND)


        self.select_all = wx.Button(
            self.m_panel1, wx.ID_ANY, "Select All", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.select_all.Bind(wx.EVT_BUTTON, self.select_all_resolutions)
        self.resolution_checkbox_container.Add(self.select_all, 0, wx.ALL, 5)

        self.deselect_all = wx.Button(
            self.m_panel1, wx.ID_ANY, "Deselect All", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.deselect_all.Bind(wx.EVT_BUTTON, self.deselect_all_resolutions)
        self.resolution_checkbox_container.Add(self.deselect_all, 0, wx.ALL, 5)

        bSizer2.Add(self.resolution_checkbox_container, 1, wx.EXPAND, 5)
        gSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        bSizer3.Add((0, 0), 1, wx.EXPAND, 5)

        self.dir_selector_label = wx.StaticText(
            self.m_panel1,
            wx.ID_ANY,
            "Wallpaper Directory",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.dir_selector_label.Wrap(-1)

        bSizer3.Add(self.dir_selector_label, 0, wx.ALL, 5)

        self.directory_selector = wx.Button(
            self.m_panel1, wx.ID_ANY, "Select Directory", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.directory_selector.Bind(wx.EVT_BUTTON, self.dirBrowser)
        bSizer3.Add(self.directory_selector, 0, wx.ALL, 5)

        self.duplicate_label = wx.StaticText(
            self.m_panel1,
            wx.ID_ANY,
            "Check For Duplicates",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.duplicate_label.Wrap(-1)

        bSizer3.Add(self.duplicate_label, 0, wx.ALL, 5)

        self.duplicate_checkbox = wx.CheckBox(
            self.m_panel1, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, 0
        )
        # Sets the duplicate checkbox to the users last value if any
        self.duplicate_checkbox.SetValue(check_duplicates_value)
        bSizer3.Add(self.duplicate_checkbox, 0, wx.ALL, 5)

        bSizer3.Add((0, 0), 1, wx.EXPAND, 5)

        gSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        bSizer4.Add((0, 0), 1, wx.EXPAND, 5)

        self.run_button = wx.Button(
            self.m_panel1, wx.ID_ANY, "Get Wallpapers", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.run_button.Bind(wx.EVT_BUTTON, self.run)
        bSizer4.Add(self.run_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer4.Add((0, 0), 1, wx.EXPAND, 5)

        gSizer1.Add(bSizer4, 1, wx.EXPAND, 5)

        self.m_panel1.SetSizer(gSizer1)
        self.m_panel1.Layout()
        gSizer1.Fit(self.m_panel1)

        """
        ----- END OF MAIN PANEL -----
        ----- START OF EDIT SUBREDDITS PANEL -----
        """

        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer5 = wx.BoxSizer(wx.VERTICAL)
        gSizer2 = wx.GridSizer(0, 2, 0, 0)

        self.subreddit_listctrl = wx.ListCtrl(self.m_panel2, style = wx.LC_REPORT)
        self.subreddit_listctrl.InsertColumn(0, "-- SUBREDDITS --")
        self.subreddit_listctrl.SetColumnWidth(0, 150)

        for idx, sub in enumerate(self.subreddit_choices):
            self.subreddit_listctrl.InsertItem(idx, sub)

        gSizer2.Add(self.subreddit_listctrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        self.add_subreddit_button = wx.Button(
            self.m_panel2, wx.ID_ANY, "Add a subreddit", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.add_subreddit_button.Bind(wx.EVT_BUTTON, self.add_subreddit)
        bSizer6.Add(self.add_subreddit_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.remove_subreddit_button = wx.Button(
            self.m_panel2, wx.ID_ANY, "Remove subreddits", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.remove_subreddit_button.Bind(wx.EVT_BUTTON, self.remove_subreddit)
        bSizer6.Add(self.remove_subreddit_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.back_to_home_button = wx.Button(
            self.m_panel2, wx.ID_ANY, "Back", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.back_to_home_button.Bind(wx.EVT_BUTTON, self.back_to_home)
        bSizer6.Add(self.back_to_home_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        # bSizer5.Add(gSizer2, 1, 5)
        gSizer2.Add(bSizer6, 1, wx.EXPAND, 5)
        bSizer5.Add(gSizer2, 0, wx.EXPAND, 5)

        self.m_panel2.SetSizer(bSizer5)
        self.m_panel2.Layout()
        gSizer2.Fit(self.m_panel2)
        self.m_panel2.Hide()

        """
        ----- END OF EDIT SUBREDDITS PANEL -----
        """

        self.SetSizer(gSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

    """
    ---------------------------
    END OF WX PYTHON FORM BUILDING - BEGINNING OF FUNCTIONS USED TO INTERACT WITH COLLECTION
    ---------------------------
    """

    def back_to_home(self, event):
        """
        Switches the panel back to the main panel
        """
        self.m_panel2.Hide()
        self.m_panel1.Show()

        self.SetSize(600, 501)
        self.SetSize(600, 500)
        
    def switch_to_edit_subreddits(self, event):
        """
        Switches the panel to a panel used to add/remove subreddits from the dropdown
        """
        self.m_panel1.Hide()
        self.m_panel2.Show()

        self.SetSize(400, 251)
        self.SetSize(400, 250)


    def dirBrowser(self, event):
        """
        Opens up a file explorer that the user can use to select the folder they would like wallpapers to be saved in
        """
        dialog = wx.DirDialog(None, message="Pick a directory.")
        if dialog.ShowModal() == wx.ID_OK:
            print(f"Default directory has been changed to {dialog.GetPath()}")
            self.file_path = dialog.GetPath()
            profile.save_settings(file_path=dialog.GetPath())
        else:
            pass
        dialog.Destroy()


    def select_all_resolutions(self, event):
        """
        Selects all of the resolution checkboxes
        """
        for choice in self.resolution_choices:
            choice.SetValue(1)

    def deselect_all_resolutions(self, event):
        """
        Unchecks all of the resolution checkboxes
        """
        for choice in self.resolution_choices:
            choice.SetValue(0)

    def add_subreddit(self, event):
        """
        Adds a subreddit using a text filed
        """
        dlg = wx.TextEntryDialog(frame, 'Enter a subreddit name','Subreddit')

        if dlg.ShowModal() == wx.ID_OK:
            existing_subs = profile.read_subreddits()

            new_sub = str(dlg.GetValue())
            if new_sub:
                existing_subs.append(new_sub)
                new_subreddits_list = set(existing_subs)
                self.update_subreddit_selectors(new_subreddits_list)
                profile.write_subreddits(list(new_subreddits_list))

        dlg.Destroy()

    def remove_subreddit(self, event):
        item = self.subreddit_listctrl.GetFirstSelected()

        subreddits_to_remove = []

        while item != -1:
            data = self.subreddit_listctrl.GetItem(item)
            subreddits_to_remove.append(data.Text)
            item = self.subreddit_listctrl.GetNextSelected(item)

        if subreddits_to_remove:
            existing_subs = profile.read_subreddits()

            new_subreddit_list = [sub for sub in existing_subs if sub not in subreddits_to_remove]
            self.update_subreddit_selectors(new_subreddit_list)
            profile.write_subreddits(new_subreddit_list)
        else:
            box = wx.MessageDialog(None,'In order to remove subreddits, please select 1 or more subreddits from the list', 'Invalid selection', wx.OK)
            answer=box.ShowModal()
            box.Destroy()

    def update_subreddit_selectors(self, subreddits):
        """
        Ubdates the subreddit dropdown and list control with the current list of subreddits
        """
        self.subreddit_choices = subreddits

        self.subreddit_listctrl.DeleteAllItems()
        for idx, sub in enumerate(subreddits):
            self.subreddit_listctrl.InsertItem(idx, sub)

        self.sub_selector.Clear()
        for sub in subreddits:
            self.sub_selector.Append(sub)

        if self.sub_selector_value and self.sub_selector_value in subreddits:
            self.sub_selector.SetValue(self.sub_selector_value)


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

        try:
            for group in progress:
                for count in group:
                    progress_bar.Update(count, "Downloading wallpaper #" + str(count))
        except json.decoder.JSONDecodeError:
            box = wx.MessageDialog(None,f'An error occurred during collection. Are you sure "{form["subreddit"]}" is a valid subreddit?', 'ERROR', wx.OK)
            answer=box.ShowModal()
            box.Destroy()


        progress_bar.Destroy()

    def __del__(self):
        pass


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show(True)
    app.MainLoop()
