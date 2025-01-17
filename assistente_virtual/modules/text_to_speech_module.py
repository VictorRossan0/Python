import os
from gtts import gTTS
import playsound

class TextToSpeechModule:
    def __init__(self, language="pt-BR"):
        self.language = language
        self.audio_file = "audio.mp3"

    def text_to_speech(self, text):
        """Converte texto em fala."""
        if not text.strip():
            print("Texto vazio. Por favor, forneça um texto válido.")
            return

        try:
            # Gerar o áudio
            tts = gTTS(text=text, lang=self.language)
            tts.save(self.audio_file)

            # Reproduzir o áudio
            print("Reproduzindo áudio...")
            playsound.playsound(self.audio_file)

        except PermissionError:
            print("Erro ao acessar o arquivo de áudio: Permissão negada.")
        except Exception as e:
            print(f"Erro inesperado ao converter texto para fala: {e}")
        finally:
            # Certificar-se de excluir o arquivo, se existir
            if os.path.exists(self.audio_file):
                try:
                    os.remove(self.audio_file)
                    print("Arquivo de áudio removido com sucesso.")
                except Exception as e:
                    print(f"Erro ao remover o arquivo de áudio: {e}")
            else:
                print("Arquivo de áudio não encontrado para exclusão.")
