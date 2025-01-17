import webbrowser
import wikipedia
from datetime import datetime


class CommandHandler:
    def __init__(self, tts):
        self.tts = tts

    def handle_command(self, comando):
        """Executa comandos com base na entrada de voz."""
        comando = comando.lower()  # Normaliza o comando para evitar problemas de maiúsculas/minúsculas

        if "wikipedia" in comando:
            termo = self.extract_term(comando, "wikipedia")
            if not termo:
                self.tts.text_to_speech("O que você gostaria de pesquisar no Wikipedia?")
                termo = input("Digite o termo para pesquisa: ")  # Substituir por entrada de voz se possível
            if termo:
                self.search_wikipedia(termo)
            else:
                self.tts.text_to_speech("Nenhum termo fornecido para a pesquisa.")
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

    def extract_term(self, comando, keyword):
        """Extrai o termo do comando, se especificado."""
        try:
            index = comando.index(keyword) + len(keyword)
            termo = comando[index:].strip()
            return termo if termo else None
        except ValueError:
            return None

    def search_wikipedia(self, termo):
        """Realiza pesquisa no Wikipedia."""
        try:
            self.tts.text_to_speech(f"Procurando informações sobre {termo} no Wikipedia.")
            resumo = wikipedia.summary(termo, sentences=2, lang="pt")
            self.tts.text_to_speech(f"Aqui está o que eu encontrei sobre {termo}: {resumo}")
        except wikipedia.exceptions.DisambiguationError:
            self.tts.text_to_speech("O termo é ambíguo. Tente ser mais específico.")
        except wikipedia.exceptions.PageError:
            self.tts.text_to_speech("Não encontrei resultados para sua pesquisa.")
        except Exception as e:
            self.tts.text_to_speech("Ocorreu um erro ao acessar o Wikipedia. Tente novamente mais tarde.")
            print(f"Erro ao acessar Wikipedia: {e}")

    def open_youtube(self):
        """Abre o site do YouTube."""
        try:
            self.tts.text_to_speech("Abrindo o YouTube...")
            webbrowser.open("https://www.youtube.com")
        except Exception as e:
            self.tts.text_to_speech("Ocorreu um erro ao tentar abrir o YouTube.")
            print(f"Erro ao abrir YouTube: {e}")

    def find_pharmacy(self):
        """Abre o Google Maps para encontrar farmácias próximas."""
        try:
            self.tts.text_to_speech("Procurando farmácias próximas...")
            webbrowser.open("https://www.google.com/maps/search/farm%C3%A1cia+pr%C3%B3xima")
        except Exception as e:
            self.tts.text_to_speech("Ocorreu um erro ao tentar encontrar farmácias.")
            print(f"Erro ao abrir Google Maps: {e}")
