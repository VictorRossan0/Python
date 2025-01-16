import speech_recognition as sr

class SpeechRecognitionModule:
    def __init__(self, language="pt-BR"):
        self.recognizer = sr.Recognizer()
        self.language = language

    def recognize_speech(self):
        """Converte fala em texto."""
        try:
            with sr.Microphone() as source:
                print("Ouvindo...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)  # Timeout configurável
                comando = self.recognizer.recognize_google(audio, language=self.language)
                print(f"Você disse: {comando}")
                return comando.lower()
        except sr.UnknownValueError:
            print("Desculpe, não entendi o que você disse.")
        except sr.WaitTimeoutError:
            print("Nenhuma fala detectada no tempo limite.")
        except OSError as e:
            print("Problema com o microfone:", e)
        except sr.RequestError as e:
            print("Erro no serviço de reconhecimento:", e)
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
        return None
