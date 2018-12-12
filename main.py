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
    for submission in reddit.subreddit('mlpdrawingschool').stream.submissions():
        if re.match("\[Weekly Challenge\] .*", submission.title):
            post_text = ("# Hey bois n girls, it's time for a new weekly challenge!\n\n" +
                        submission.selftext + "\n\nLink: " + 
                        "https://reddit.com" + submission.permalink)

            for channel in settings["channels"]:
                await client.send_message(client.get_channel(channel), post_text)

client.run(settings["discord_client_token"])
