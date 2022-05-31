from PIL import ImageFile
from pathlib import Path

import requests
import json
import urllib


class redditCollector:
    def __init__(self, form, file_path):
        """
        Parameters:
            form (dict): Dictionary containing all the data we need to collect wallpapers for the user
            file_path (str): the file_path string
        """
        self.RETRIES = 0
        self.downloaded = 0
        self.success = False
        self.last_post_id = None

        self.file_path = file_path
        self.wallpapers_requested = form["wallpapers_requested"]
        self.MAX_RETRIES = int((self.wallpapers_requested * (10**3)) / 100)
        self.resolutions = [
            self.parse_resolution(resolution) for resolution in form["resolutions"]
        ]
        self.subreddit = form["subreddit"].lower()
        self.sort_by = form["sort-by"].lower()
        self.check_for_duplicates = form["check_for_duplicates"]

        # If we already have a record of the retrieved wallpapers, load it, otherwise create a new one so if the user wants to avoid
        # duplicates we can
        if Path("retrieved_wallpapers.json").is_file():
            with open("retrieved_wallpapers.json") as retrieved_wallpapers:
                self.retrieved_wallpapers = json.load(retrieved_wallpapers)
        else:
            self.retrieved_wallpapers = []

    def updated_retrieved_wallpapers(self):
        """
        Updates our local json object so we can keep track of what wallpapers the user has already downloaded
        """
        with open("retrieved_wallpapers.json", "w+") as retrieved_wallpapers:
            retrieved_wallpapers.write(json.dumps(self.retrieved_wallpapers))

    def parse_resolution(self, res):
        """
        Converts the resolution from a string to a list of ints
        1920x1080 --> [1920, 1080]

        Parameters:
            res (str): The resolution in the form of a string

        Returns:
            list
        """

        return [int(res[: res.find("x")]), int(res[res.find("x") + 1 :])]

    def login(self):
        """
        Logs in and returns our headers with our user agent and access token

        Returns:
            headers (dict): A dictionary containing out user agent and access token
        """
        # Get the credentials from base.json (if you don't have the file, you won't be able to use this)
        with open("based.json") as json_file:
            credentials = json.load(json_file)

        # Information that we get from reddit. IMPORTANT TO KEEP PRIVATE
        CLIENT_ID = credentials["CLIENT_ID"]
        SECRET = credentials["SECRET"]

        # Get authorization token
        auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET)

        data = {
            "grant_type": "password",
            "username": credentials["USERNAME"],
            "password": credentials["PASSWORD"],
        }

        # let api know what version we're using
        headers = {"User-Agent": "MyAPI/0.0.1"}

        # Gets access_token
        res = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=auth,
            data=data,
            headers=headers,
        )

        TOKEN = res.json()["access_token"]

        # returns updated headers dict with access token
        return {**headers, **{"Authorization": f"bearer {TOKEN}"}}

    def is_valid_resolution(self, url):
        """
        Checks the resolution of the image before downloading it, then determines whether or not it matches what the user
        wanted

        Parameters:
            url (str): url to the source of the image

        Returns:
            (boolean): Whether or not the image had a valid resolution,
            (str|NoneType): The resolution of the image we found (to be used for better logging)
        """

        # get file size *and* image size (None if not known)
        with urllib.request.urlopen(url) as file:
            size = file.headers.get("content-length")
            if size:
                size = int(size)
            p = ImageFile.Parser()
            data = file.read(1024)
            if not data:
                print("Image size can't be verified... skipping...")
                return False, None
            p.feed(data)
            if p.image:
                image_data = p.image.size
            else:
                return False, None

        width, height = image_data

        if any(width == res[0] or height == res[1] for res in self.resolutions):
            return True, f"{width}x{height}"
        else:
            return False, f"{width}x{height}"

    def download_posts(self, last_post_id=None):
        """
        Requests 100 posts at a time. If a post contains an image, we check the resolution. If the image has the requested resolution, we download it.
        For each image that does match our requirements, we add that to the success count.

        Parameters:
            last_post_id (str|None): The ID of the post we left off on (exists)

        Returns:
            None
        """

        # Make a request to get the posts from the subreddit
        if last_post_id:
            res = requests.get(
                f"https://oauth.reddit.com/r/{self.subreddit}/{self.sort_by}",
                headers=self.headers,
                params={"after": last_post_id, "limit": 100},
            )
        else:
            res = requests.get(
                f"https://oauth.reddit.com/r/{self.subreddit}/{self.sort_by}",
                headers=self.headers,
                params={"limit": 100},
            )

        # Read the json response
        posts = res.json()

        """
        Iterate through the posts, the data structure kind of looks like this. Each dictionary in the "children" list is a post, essentially.
        Also, there are many many more fields, I just included the relevant ones.
        posts = {
            data: {
                children: [
                    {
                        'data': {
                            'url': 'example.com',
                            'id': 'some_id',
                        },
                        'kind': 'some_str',
                    }
                ]
            }
        } 
        """
        for idx in range(len(posts["data"]["children"])):
            # "kind" is just a variable used to make the post id. In order to make a proper post id, you need this attribute and the ID, and then
            # you can reference that in future queries so you know where you left off on.
            kind = posts["data"]["children"][idx]["kind"]
            post = posts["data"]["children"][idx]["data"]
            id = post["id"]
            image_url = post["url"]

            extensions = [".png", ".jpg", ".jpeg"]

            # If the url doesn't contain an image extension
            if all(ex not in image_url for ex in extensions):
                continue

            # Gets the image name
            image_name = image_url[image_url.rfind("/") + 1 :]

            self.last_post_id = kind + id

            valid_resolution, resolution = self.is_valid_resolution(image_url)

            if valid_resolution and self.downloaded < self.wallpapers_requested:
                if self.check_for_duplicates:
                    # If we are checking for duplicates, and this image is already in our retrieved wallpapers record, skip
                    if image_name in self.retrieved_wallpapers:
                        print("Duplicate image found, skipping...")
                        continue
                print(f"Valid image size {resolution}! Downloading...")
                # download and name image
                if self.file_path:
                    if "/" in self.file_path:
                        urllib.request.urlretrieve(
                            image_url, self.file_path + "/" + image_name
                        )
                    else:
                        urllib.request.urlretrieve(
                            image_url, self.file_path + "\\" + image_name
                        )
                else:
                    urllib.request.urlretrieve(image_url, image_name)
                # Now that we've downloaded the image, update the record
                self.retrieved_wallpapers.append(image_name)
                # we yield the download count so that way we can update the progress bar
                self.downloaded += 1
                yield self.downloaded
                if self.downloaded == self.wallpapers_requested:
                    self.success = True
                    return
            elif (
                not valid_resolution
                and self.downloaded < self.wallpapers_requested
                and resolution is not None
            ):
                # This elif statement is so we can just properly log if a resolution is invalid while we're still trying to download
                # wallpapers
                print(f"Invalid image size {resolution}... skipping...")

    def collect_wallpapers(self):
        """
        Gets our credentials, and downloads the desired amount of posts we want at a specific resolution from a given subreddit

        Parameters:
            form (dict): Dictionary containing all the data we need to collect wallpapers for the user
        """
        self.headers = self.login()

        while not self.success and self.RETRIES < self.MAX_RETRIES:
            print(f"Downloading {self.wallpapers_requested} images to {self.file_path}")
            yield self.download_posts()
            self.RETRIES += 1

        self.updated_retrieved_wallpapers()

        if self.success:
            print(f"FINISHED! Successfully downloaded {self.wallpapers_requested}")
        else:
            print(
                f"FINISHED! Failed to download desired amount of wallpapers. {self.downloaded} wallpapers were retrieved"
            )
