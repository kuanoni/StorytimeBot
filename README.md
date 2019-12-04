# StorytimeBot
A Discord bot for moderating one-word-at-a-time stories.

<a href="http://fvcproductions.com"><img src="https://cdn.iconscout.com/icon/free/png-256/discord-283279.png" title="FVCproductions" alt="FVCproductions"></a>

Requires **discord.py** from https://github.com/Rapptz/discord.py
```
pip install discord
```

## Usage

```
usage: StorytimeBot.py [-h] [-t TOKEN] [-s STORY CHANNEL ID] 
                       [-c COMMAND CHANNEL ID] [-p PEOPLE TO POST]
                       [-l LOG TO FILE]

a bot for moderating one-word-at-a-time stories

arguments:
  -h, --help              show this help message and exit
  -t TOKEN,               discord bot token
  -s STORY CHANNEL ID     channel id where story will take place
  -c COMMAND CHANNEL ID   channel id where commands will take place
  -p PEOPLE TO POST       people must wait for N people to post
  -l LOG TO FILE          include logging to 'discord.log'
```

## Example
```
python StorytimeBot.py -t f87asd6f7876asd87f68sa7df6896vgk.fasdf7 -s 123412341212 -c 123412341234 -p 4 -l
```
