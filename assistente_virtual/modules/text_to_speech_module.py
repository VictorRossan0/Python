import os
from gtts import gTTS
import playsound

class TextToSpeechModule:
    def __init__(self, language="pt-BR"):
        self.language = language
        self.audio_file = "audio.mp3"

    def text_to_speech(self, text):
        """Converte texto em fala."""
        try:
            tts = gTTS(text=text, lang=self.language)
            tts.save(self.audio_file)
            playsound.playsound(self.audio_file)
            if os.path.exists(self.audio_file):
                os.remove(self.audio_file)
            else:
                print("Arquivo de áudio não encontrado para exclusão.")
        except PermissionError:
            print("Erro ao acessar o arquivo de áudio: Permissão negada.")
        except Exception as e:
            print(f"Erro inesperado ao converter texto para fala: {e}")
