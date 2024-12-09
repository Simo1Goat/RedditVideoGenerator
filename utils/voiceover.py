import pyttsx3
from config import VOICEOVER_DIR
import json

def make_voice_over():
    # initialize the engine
    engine = pyttsx3.init()
    # get the comment
    with open("../tmp/submissions.json", 'rb') as submission_file:
        submissions = json.load(submission_file)

        for submission in submissions:
            print(f"converting submission {submission['title']} comments to audios ...")
            for comment in submission['comments'][:3]:
                comment_id = comment['id']
                comment_body = comment['body']
                voice_over_path = f"{VOICEOVER_DIR}/comment-{comment_id}.mp3"
                engine.save_to_file(comment_body, voice_over_path)
                engine.runAndWait()

    print("converting text to audios done.")

if __name__ == '__main__':
    make_voice_over()
