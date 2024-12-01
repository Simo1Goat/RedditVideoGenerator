from praw import Reddit
from config import CLIENT_ID, SECRET_ID, APP_NAME


class RedditModel:
    client = None

    def __init__(self, client_id, client_secret, app_name):
        client = Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=app_name,
        )

        self.client = client
