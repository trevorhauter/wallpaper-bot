# wallpaper-bot
A neat reddit wallpaper bot

All the depencies are really easy to install, except wx python. In order to properly download wxPython for ubuntu 20.04, use this command below
```
python3 -m pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04 wxPython
```

If you want to use this program with your own reddit bot, just follow this stuff here
https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c

Once you have all of the stuff set up from the article, take the credentials created for the bot and place them in a file called based.json in this data structure
```
{
  "SECRET": SECRET,
  "CLIENT_ID": CLIENT_ID,
  "USERNAME": USERNAME,
  "PASSWORD": PASSWORD
}
```

### Creating an executable for windows

In order to create an executable on windows, you'll want to have python3.8+ installed as well as pip. These commands might be sort of wrong because I'm doing this from memory. If there is anything that needs to be updated let me know and I'll update them.

Install virtualenv
```
pip install virtualenv
```

Create a virtualenv named "venv" in the same directory as the project
```
virtualenv venv
```

Activate the virtualenv
```
.venv\Scripts\activate.bat
```

Install the libraries
```
pip freeze > requirements.txt.
```

Install pyinstaller 
```
pip install pyinstaller
```

Create an executable of the gui.py
```
pyinstaller gui.py --onefile
```

Now you have an executable! You just need to include the based.json file with your credentials and you're good to go
