from pathlib import Path

import json


class user_profile:
    """
    This class is used to store a users preferences. Basically to just remember what they last entered
    user_profile might be a bit of an overstatement
    """

    def __init__(self):
        # This is the variable we store our settings in
        if Path("settings.json").is_file():
            with open("settings.json") as settings:
                self.settings = json.load(settings)
        else:
            self.settings = None

    def save_settings(self, form=None, file_path=None):
        """
        Saves the users current settings to json file

        Parameters:
            form (dict): Dictionary containing all the data we need to collect wallpapers for the user, this is also passed to the reddit collector
            file_path (str): optional str containing the users default filepath if any
        """

        def read_settings():
            """
            Returns the file contents in dictionary form
            """
            with open("settings.json", "r") as settings:
                return json.load(settings)

        def write_settings(data):
            """
            Writes the file in json with whatever data we git it
            """
            with open("settings.json", "w+") as settings:
                settings.write(json.dumps(data))

        if Path("settings.json").is_file():
            settings = read_settings()
            if file_path:
                # If form data is already in the existing settings, include that when writing the new form, otherwise just save the form
                if "subreddit" in settings:
                    settings["file_path"] = file_path
                    write_settings(settings)
                else:
                    write_settings({"file_path": file_path})
            else:
                # If file_path is already in the existing settings, include that when writing the new form, otherwise just save the form
                if "file_path" in settings:
                    file_path = settings["file_path"]
                    form["file_path"] = file_path
                    write_settings(form)
                else:
                    write_settings(form)
        else:
            # If the json file doesn't exist and we're just saving the file path
            if file_path:
                print(f"Saving {file_path}")
                write_settings({"file_path": file_path})
            else:
                write_settings(form)

    def read_subreddits(self):
        """
        Returns the current list of subreddits
        """
        default_subreddits = ["Wallpapers", "Art"]

        if Path("subreddits.json").is_file():
            with open("subreddits.json", "r") as subs_file:
                return json.load(subs_file)
        else:
            self.write_subreddits(default_subreddits)
            return default_subreddits
        

    def write_subreddits(self, subreddits):
        """
        Rewrites the subreddits list with the list provided
        """
        with open("subreddits.json", "w+") as subs_file:
                subs_file.write(json.dumps(subreddits))
