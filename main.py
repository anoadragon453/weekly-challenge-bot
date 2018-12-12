from matrix_client.api import MatrixHttpApi
import praw
import re
import json

with open("settings.json") as s:
    settings = json.loads(s.read())

# Setup matrix auth
matrix = MatrixClient("http://amorgan.xyz", token=settings["matrix_token"])

token = client.login(username=settings["matrix_username"],
                     password=settings["matrix_password"])

# Setup reddit auth
reddit = praw.Reddit(client_id=settings["reddit_client_id"],
                     client_secret=settings["reddit_client_secret"],
                     user_agent=settings["reddit_user_agent"])

for submission in reddit.subreddit('mlpdrawingschool').stream.submissions():
    if re.match("\[Weekly Challenge\] .*", submission.title):
        post_text = ("# Hey bois n girls, it's time for a new weekly challenge!\n\n" +
                    submission.selftext + "\n\nLink: " + submission.permalink)

        for room_id in settings["rooms"]:
            print(matrix.send_message(room_id, post_text))
