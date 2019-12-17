# StorytimeBot
A Discord bot for moderating one-word-at-a-time stories.

<a><img src="https://i.imgur.com/r85tVM7.png"></a>

Made with **Python3.7** and **discord.py** version 1.2.5, from https://github.com/Rapptz/discord.py
```
pip install discord
```

## Usage

Edit this config file with your own information. 
To get channel IDs, enable developer mode in the Discord client settings, and right click your desired channel.
```
{
  "token": "0",
  "story_channel_id": "0",
  "command_channel_id": "0",
  "people_to_post": "3",
  "log_to_file": "True",
  "banned_words" : [
    "supercalifragilisticexpialidocious"
  ],
  "banned_users" : [
    "supercalifragilisticexpialidocious"
  ]
}
```
