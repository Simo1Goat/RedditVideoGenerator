from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, VideoFileClip
import os
from random import choice

def generate_video(submission_id: str):
    background_vid_dir = f"../tmp/backgrounds/"
    submission_dir = f"../tmp/submission_{submission_id}"
    clips = []

    if os.path.exists(submission_dir):
        matched_pairs = get_matched_pairs(submission_dir)
        title_files = [item for item in matched_pairs if item[0].startswith("title")][0]
        comment_files = [item for item in matched_pairs if item[0].startswith("comment")]
        # the beginning of the clip
        title_clip = create_clip(os.path.join(submission_dir, title_files[0]),
                                 os.path.join(submission_dir, title_files[1]))
        clips.append(title_clip)

        for comment in comment_files:
            comment_screen = os.path.join(submission_dir, comment[0])
            comment_voice = os.path.join(submission_dir, comment[1])
            comment_clip = create_clip(comment_screen, comment_voice)
            clips.append(comment_clip)

    title_and_comment_clips = concatenate_videoclips(clips)

    # we need to add the background video
    background_vids = os.listdir(background_vid_dir)
    background_vid = choice(background_vids)
    background_vid_path = os.path.join(background_vid_dir, background_vid)
    background_clip = VideoFileClip(filename=background_vid_path).without_audio()
    background_clip = background_clip.subclip(0, title_and_comment_clips.duration)

    # create a composite clip
    clips = [background_clip, title_and_comment_clips]
    final_clip = CompositeVideoClip(clips)
    output_file = os.path.join(submission_dir, f"final-{submission_id}.mp4")
    final_clip.write_videofile(output_file,
                               codec="mpeg4",
                               threads=12,
                               bitrate="8000k",
                               logger="bar")


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


if __name__ == '__main__':
    generate_video("1hq286d")
