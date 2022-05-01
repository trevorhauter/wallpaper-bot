# wallpaper-bot
A neat reddit wallpaper bot

All the depencies are really easy to install, except wx python. In order to properly download wxPython for ubuntu 20.04, use this command below
```
python3 -m pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04 wxPython
```

If you want to use this program with your own reddit bot, just follow this stuff here
https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c

You just need a json file called based.json containing the keys CLIENT_ID, and SECRET (which you can find using the article above) and the program will use your API credentials!
