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

