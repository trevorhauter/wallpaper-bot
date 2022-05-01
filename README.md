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
