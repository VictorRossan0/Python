from modules.speech_recognition_module import SpeechRecognitionModule
from modules.text_to_speech_module import TextToSpeechModule
from modules.command_handler import CommandHandler

if __name__ == "__main__":
    tts = TextToSpeechModule(language="pt-BR")
    sr_module = SpeechRecognitionModule(language="pt-BR")
    command_handler = CommandHandler(tts)

    tts.text_to_speech("Olá! Como posso ajudar você hoje?")
    ativo = True

    while ativo:
        comando = sr_module.recognize_speech()  # Corrigido para chamar o método correto
        if comando:
            ativo = command_handler.handle_command(comando)
