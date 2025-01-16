import webbrowser
import wikipedia
from datetime import datetime

class CommandHandler:
    def __init__(self, tts):
        self.tts = tts

    def handle_command(self, comando):
        """Executa comandos com base na entrada de voz."""
        if "wikipedia" in comando:
            self.tts.text_to_speech("O que você gostaria de pesquisar no Wikipedia?")
            termo = input("Digite o termo para pesquisa: ")  # Pode ser substituído por outro método de entrada
            if termo:
                self.search_wikipedia(termo)
        elif "youtube" in comando:
            self.open_youtube()
        elif "farmácia" in comando:
            self.find_pharmacy()
        elif "horas" in comando:
            hora_atual = datetime.now().strftime("%H:%M")
            self.tts.text_to_speech(f"Agora são {hora_atual}.")
        elif "sair" in comando or "encerrar" in comando:
            self.tts.text_to_speech("Até mais! Foi um prazer ajudar você.")
            return False
        else:
            self.tts.text_to_speech("Comando não reconhecido. Tente novamente.")
        return True

    def search_wikipedia(self, termo):
        """Realiza pesquisa no Wikipedia."""
        try:
            resumo = wikipedia.summary(termo, sentences=2, lang="pt")
            self.tts.text_to_speech(f"Aqui está o que eu encontrei sobre {termo}: {resumo}")
        except wikipedia.exceptions.DisambiguationError:
            self.tts.text_to_speech("O termo é ambíguo. Tente ser mais específico.")
        except wikipedia.exceptions.PageError:
            self.tts.text_to_speech("Não encontrei resultados para sua pesquisa.")

    def open_youtube(self):
        """Abre o site do YouTube."""
        self.tts.text_to_speech("Abrindo o YouTube...")
        webbrowser.open("https://www.youtube.com")

    def find_pharmacy(self):
        """Abre o Google Maps para encontrar farmácias próximas."""
        self.tts.text_to_speech("Procurando farmácias próximas...")
        webbrowser.open("https://www.google.com/maps/search/farm%C3%A1cia+pr%C3%B3xima")
