from matrix_client.api import MatrixHttpApi

import discord
import asyncio
import praw
import re
import json

# Open settings file
with open("settings.json") as s:
    settings = json.loads(s.read())

# Setup discord auth
client = discord.Client()

# Setup reddit auth
reddit = praw.Reddit(client_id=settings["reddit_client_id"],
                     client_secret=settings["reddit_client_secret"],
                     user_agent=settings["reddit_user_agent"])

# Wait for discord client to be ready
@client.event
async def on_ready():
    channels = []
    for channel_id in settings["channels"]:
        channels.append(client.get_channel(channel_id))

    for submission in reddit.subreddit('mlpdrawingschool').stream.submissions(skip_existing=True):
        if re.match("\[Weekly Challenge\] .*", submission.title):
            print("Posting:", submission.title)
            post_text = ("# Hey bois n girls, it's time for a new weekly challenge!\n\n" +
                        submission.selftext + "\n\nLink: " + 
                        "https://reddit.com" + submission.permalink)

            # Split post into 2000 char increments
            n = 2000
            posts = [post_text[i:i+n] for i in range(0, len(post_text), n)]

            for post in posts:
                for channel in channels:
                    await client.send_message(channel, post_text)

client.run(settings["discord_client_token"])
