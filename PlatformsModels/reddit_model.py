from praw import Reddit
from praw.models import Submission, MoreComments
from config import CLIENT_ID, SECRET_ID, APP_NAME
import json


class RedditModel:
    client = None

    def __init__(self, client_id, client_secret, app_name):
        client = Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=app_name,
        )

        self.client = client

    def get_submissions(self, **kwargs):
        channel = kwargs['channel']
        time_filter = kwargs['time_filter']
        limit = kwargs['limit']

        submissions = self.client.subreddit(channel) \
            .top(time_filter=time_filter, limit=limit)

        return [self.get_submissions_content(submission)
                for submission in submissions
                if submission is not submission.over_18]

    def get_submissions_content(self, submission: Submission) -> dict:
        return {
            "id": submission.id,
            "title": submission.title,
            "permalink": submission.permalink,
            "created_date": submission.created_utc,
            "comments": self.get_submission_comments(submission)
        }

    @staticmethod
    def get_submission_comments(submission: Submission) -> list[dict]:
        wanted_comments = []

        for comment in submission.comments:
            if isinstance(comment, MoreComments) or len(comment.body.split()) > 100:
                continue
            else:
                wanted_comments.append({
                    "id": comment.id,
                    "body": comment.body,
                })

        return wanted_comments


if __name__ == '__main__':
    reddit_client = RedditModel(CLIENT_ID, SECRET_ID, APP_NAME)

    reddit = {
        "channel": "askreddit",
        "time_filter": "day",
        "limit": 3
    }

    submission_list = reddit_client.get_submissions(**reddit)

    with open("../tmp/submissions.json", "w") as json_file:
        json.dump(submission_list, json_file, indent=4)

    print("Saving is done.")
