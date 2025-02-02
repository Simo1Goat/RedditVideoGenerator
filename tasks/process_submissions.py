from PlatformsModels.ElevenLabsModel import ElevenLabs
from PlatformsModels.selenium_scrapper import SeleniumScrapper
from config import REDDIT_WEBSITE


def process_submissions(submissions_object: list[dict]):
    elevenlabs = ElevenLabs()
    scrapper = SeleniumScrapper()

    for submission in submissions_object:
        scrapper.set_screenshot_dir(f"submission_{submission.get('id')}")
        elevenlabs.set_voiceover_dir(f"submission_{submission.get('id')}")

        scrapper.get_website(f"{REDDIT_WEBSITE}{submission['permalink']}")
        scrapper.screen_shoot_submission(submission)

        elevenlabs.list_all_voices()
        elevenlabs.text_to_speech(submission)
        for comment in submission.get("comments")[:3]:
            elevenlabs.text_to_speech(comment, is_comment=True)
