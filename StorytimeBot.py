import discord
import string
from collections import Counter

token = ""
client = discord.Client()

story_channel_id = 0
command_channel_id = 0

banned_words = []
banned_users = []
people_to_post = 3
command_prefix = '!'


@client.event
async def on_ready():
    print(f"Bot has logged on as {client.user} and is ready to use.")


@client.event
async def on_message(msg):
    if msg.channel.id == story_channel_id:
        channel = msg.channel
        msg_text = msg.clean_content

        if check_banned(msg):
            await msg.delete()

        temp_users = []
        async for message in channel.history(limit=(people_to_post + 1)):
            temp_users.append(message.author.name)

        if check_people_to_post(msg, temp_users):
            await msg.delete()

        if check_multiple_words(msg_text):
            await msg.delete()

    # COMMANDS
    if msg.channel.id == command_channel_id:
        channel = msg.channel
        msg_text = msg.clean_content

        if msg_text == "!storytime":
            story = await get_story()
            for elem in [story[i:i + 2000] for i in range(0, len(story), 2000)]:  # discord messages can only be 2000 chars
                await msg.channel.send(elem)

        if msg_text == "!storystats":
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
