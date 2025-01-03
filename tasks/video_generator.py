from moviepy import ImageClip, AudioFileClip
import os

def create_clip(screenShotFile, voiceOverFile):
    audio_clip = AudioFileClip(voiceOverFile)
    video_clip = ImageClip(screenShotFile)
    video_clip.duration = audio_clip.duration
    video_clip.audio = audio_clip

    return video_clip

def get_matched_pairs(submission_dir: str) -> list[tuple]:
    """
    this function is going to be used to create a tuple between the comment
    screenshot and its voiceover
    :param: submission directory
    :return: tuple(comment_screenshot, voice_over_screenshot)
    """
    files = os.listdir(submission_dir)
    screenshots = {f.split(".")[0]: f for f in files if f.endswith(".png")}
    voice_overs = {f.split(".")[0]: f for f in files if f.endswith(".mp3")}

    matched_pairs = []
    for file_id, screen in screenshots.items():
        if file_id in voice_overs:
            matched_pairs.append((screen, voice_overs[file_id]))

    return matched_pairs

