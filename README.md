# Lost Ark status tracker bot for Discord

This bot is made to check the Lost Ark's servers status.  
I got this idea when I tried to play to [Lost Ark](https://www.playlostark.com/fr-fr/), because their servers are always full atm. So when I was hard-working on discord (kind of), I had to alt-tab, refresh the page to check the servers' status etc: boring. So i thought, let's make a discord bot for that !  

## Quick start

### Install dependencies

- [nextcord](https://pypi.org/project/nextcord/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [requests-cache](https://pypi.org/project/requests-cache/)
```console
$ pip install -r ./requirements.txt
```

### Configure

In order to run the discord bot, you'll need a bot token.  
Please check [this tutorial](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) if you don't know how to get one.  
Once you have it, create a `.env` file and write down your token like this:
```
TOKEN=your token here
```

### Run

```console
$ python src/main.py
```

## Documentation

### Status

Usage: `_status` <br>
Description: Displays the current status of the different servers

![Demo](https://i.imgur.com/uMXTeLb.gif)