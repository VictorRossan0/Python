import speech_recognition as sr

class SpeechRecognitionModule:
    def __init__(self, language="pt-BR", timeout=5, phrase_time_limit=10):
        self.recognizer = sr.Recognizer()
        self.language = language
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit

    def recognize_speech(self):
        """Converte fala em texto."""
        try:
            with sr.Microphone() as source:
                print("Ajustando para ruído ambiente, aguarde...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)  # Ajuste de ruído ambiente
                print("Ouvindo... Fale algo!")
                audio = self.recognizer.listen(
                    source, timeout=self.timeout, phrase_time_limit=self.phrase_time_limit
                )
                comando = self.recognizer.recognize_google(audio, language=self.language)
                print(f"Você disse: {comando}")
                return comando.lower()
        except sr.UnknownValueError:
            print("Desculpe, não consegui entender o que você disse. Tente novamente.")
        except sr.WaitTimeoutError:
            print("Nenhuma fala detectada no tempo limite. Por favor, tente novamente.")
        except OSError as e:
            print(f"Problema com o microfone: {e}")
        except sr.RequestError as e:
            print(f"Erro ao conectar com o serviço de reconhecimento: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
        return None
