from TTS.api import TTS
from pydub import AudioSegment
from pydub.playback import play

def textTs():
    # Modelo en español
    model_name = "tts_models/es/css10/vits"
    # Init TTS
    tts = TTS(model_name)
    # Text to speech
    tts.tts_to_file(text="hello, i'm isaac.",
                    file_path="output.wav",
                    emotion = "happy",
                    speed = 1.5)
    # Play audio
    song = AudioSegment.from_wav("output.wav")
    play(song)
