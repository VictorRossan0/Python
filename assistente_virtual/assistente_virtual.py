from modules.speech_recognition_module import SpeechRecognitionModule
from modules.text_to_speech_module import TextToSpeechModule
from modules.command_handler import CommandHandler

def main():
    """Função principal para executar o assistente virtual."""
    tts = TextToSpeechModule(language="pt-BR")
    sr_module = SpeechRecognitionModule(language="pt-BR")
    command_handler = CommandHandler(tts)

    tts.text_to_speech("Olá! Como posso ajudar você hoje?")
    ativo = True

    while ativo:
        try:
            comando = sr_module.recognize_speech()
            if comando:
                ativo = command_handler.handle_command(comando)
            else:
                tts.text_to_speech("Desculpe, não consegui ouvir nada. Pode repetir?")
        except KeyboardInterrupt:
            # Permite encerrar com Ctrl+C
            tts.text_to_speech("Até mais! Encerrando o programa.")
            ativo = False
        except Exception as e:
            # Lida com erros inesperados
            print(f"Erro inesperado: {e}")
            tts.text_to_speech("Ocorreu um erro inesperado. Por favor, tente novamente.")

if __name__ == "__main__":
    main()
