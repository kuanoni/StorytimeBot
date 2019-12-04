import discord
import string
from collections import Counter
import logging
import argparse

# Command line argument parser
parser = argparse.ArgumentParser(description='Storytime Bot: a bot for moderating one-word-at-a-time stories')
parser.add_argument("-t", required=True, default=0, help="Discord bot token")
parser.add_argument("-s", required=True, default=0, type=int, help="Story channel id")
parser.add_argument("-c", required=True, default=0, type=int, help="Command channel id")
parser.add_argument("-p", default=3, type=int, help="People to post. (Default is 3)")
parser.add_argument("-l", default=False, action='store_true', help="Log infractions?")
args = parser.parse_args()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

token = args.t
client = discord.Client()

story_channel_id = args.s
command_channel_id = args.c

banned_words = []
banned_users = []
people_to_post = args.p


@client.event
async def on_ready():
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if args.l:
        # create a file handler
        handler = logging.FileHandler('discord.log')
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.info(f"Bot has logged on as {client.user} and is ready to use.")


@client.event
async def on_message(msg):
    if msg.channel.id == story_channel_id:
        channel = msg.channel
        msg_text = msg.clean_content

        if check_banned(msg):
            logger.warning(f"A banned user or message was posted: {msg.author.name} | {msg.clean_content}")
            await msg.delete()

        temp_users = []
        async for message in channel.history(limit=(people_to_post + 1)):
            temp_users.append(message.author.name)

        if check_people_to_post(msg, temp_users):
            logger.warning(f"{msg.author.name} attempted to multi-post: {msg.clean_content}")
            await msg.delete()

        if check_multiple_words(msg_text):
            logger.warning(f"{msg.author.name} posted too many words: {msg.clean_content}")
            await msg.delete()

    # COMMANDS
    if msg.channel.id == command_channel_id:
        channel = msg.channel
        msg_text = msg.clean_content

        if msg_text == "!storytime":
            logger.info(f"{msg.author.name} used !storytime")
            story = await get_story()
            for elem in [story[i:i + 2000] for i in range(0, len(story), 2000)]:  # discord messages can only be 2000 chars
                await msg.channel.send(elem)

        if msg_text == "!storystats":
            logger.info(f"{msg.author.name} used !storystats")
            stats = await get_stats()
            await msg.channel.send(stats)


def check_banned(msg):
    if msg.author.name in banned_users:
        return True

    for word in banned_words:
        if word in msg.clean_content:
            return True


def check_people_to_post(msg, history):
    global people_to_post
    if history.count(msg.author.name) > 1:
        return True


def check_multiple_words(msg):
    return len(msg.split()) > 1


async def get_story():
    story_list = []
    channel = client.get_channel(story_channel_id)
    async for msg in channel.history():
        story_list.append(msg.clean_content)

    story_list.reverse()

    for i in range(len(story_list)):
        story_list[i] = story_list[i].replace(' ', '')

        if story_list[i][0] in string.punctuation:  # moves punctuation from beginning of word to end of previous word
            story_list[i - 1] += (story_list[i][0])
            story_list[i] = story_list[i][1:]

    del story_list[0]  # deletes rules post

    story = ""
    for word in story_list:
        story += word + ' '

    return story


async def get_stats():
    temp_users = []

    channel = client.get_channel(story_channel_id)
    async for message in channel.history(limit=10000):
        temp_users.append(message.author.name)

    user_list = dict(Counter(temp_users))
    user_list = sorted(user_list.items(), key=lambda x: x[1], reverse=True)

    user_stats = "**@ Word Count Leaderboard @**\n"
    for i in range(len(user_list)):
        user_stats = user_stats + user_list[i][0] + ": " + str(user_list[i][1]) + "\n"

    return user_stats


client.run(token)
