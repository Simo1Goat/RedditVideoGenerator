import pyttsx3


class TextToSpeech:
    engine: pyttsx3.Engine = None
    voiceover_dir = "../tmp"

    def __init__(self, voice, rate: int, volume: float):
        self.engine = pyttsx3.init()

        if voice:
            self.engine.setProperty("voice", voice)

        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volumee", volume)

    def list_available_voices(self):
        voices: list = [self.engine.getProperty("voices")]

        for index, voice in enumerate(voices[0], start=1):
            language_voice = voice.languages[0] if voice.languages else "empty"
            print(f"{index} {voice.name} {voice.age}: {language_voice} {voice.gender} {voice.id}")

    def text_to_speech(self, text: str, save: bool = False, file_name="output.mp3"):
        self.engine.say(text)
        print("I am speaking")

        if save:
            self.engine.save_to_file(text, f"{self.voiceover_dir}/{file_name}")

        self.engine.runAndWait()


if __name__ == '__main__':
    tts = TextToSpeech("HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0", 200, 1.0)
    tts.list_available_voices()

    tts.text_to_speech("Hello I am a Python BOT!")
# HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0
