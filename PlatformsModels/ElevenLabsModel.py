import requests
from random import choice
from config import ELEVENLABS_URL, XI_API_KEY
import logging
import os

logging.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s', level=logging.INFO)


class ElevenLabs:
    voices_url = f"{ELEVENLABS_URL}/voices"
    basic_tts_url = f"{ELEVENLABS_URL}/text-to-speech"
    voiceover_dir = None
    tts_url = None
    current_voice = None
    current_voices = []

    def set_tts_url(self):
        random_voice = choice(self.current_voices)
        while random_voice == self.current_voice:
            random_voice = choice(self.current_voices)

        self.tts_url = f"{self.basic_tts_url}/{random_voice.get('voice_id')}/stream"
        self.current_voice = random_voice

    def list_all_voices(self):
        headers = {
            "Accept": "application/json",
            "xi-api-key": XI_API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.get(self.voices_url, headers=headers)

        if response.ok:
            data_voices = response.json()

            self.current_voices = data_voices["voices"]
            return 200

        return None

    def set_voiceover_dir(self, voiceover_dir):
        self.voiceover_dir = f"../tmp/{voiceover_dir}"
        if not os.path.exists(self.voiceover_dir):
            os.mkdir(self.voiceover_dir)
            logging.info(f"Created new directory {self.voiceover_dir}")
            return True
        logging.info(f"Directory {self.voiceover_dir} already exists")

    def text_to_speech(self, text_to_speak: dict, is_comment: bool = False):
        self.set_tts_url()
        headers = {
            "Accept": "application/json",
            "xi-api-key": XI_API_KEY
        }

        payload = {
            "text": text_to_speak.get("body") if is_comment else text_to_speak.get("title"),
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8,
                "style": 0.0
            }
        }

        response = requests.post(self.tts_url,
                                 headers=headers,
                                 json=payload,
                                 stream=True)
        while not response.ok:
            self.set_tts_url()
            response = requests.post(self.tts_url,
                                     headers=headers,
                                     json=payload,
                                     stream=True)

        output_file = f"{self.voiceover_dir}/{'comment' if is_comment else 'title'}-{text_to_speak.get('id')}.mp3"
        with open(output_file, mode="wb") as audio_file:
            for chunk in response.iter_content(chunk_size=1024):
                audio_file.write(chunk)
            print("The audio file is saved successfully :)")


if __name__ == '__main__':
    eleven = ElevenLabs()

    eleven.list_all_voices()

    text = {
        "id": "m05vlxr",
        "body": "All unscented soap, laundry soap, face soap and body soap. My skin feels better and when I wear perfume it's not clashing with any other cheaper fragrances."
    }

    eleven.text_to_speech(text)
