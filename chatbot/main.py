from flask import Flask, request, jsonify
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from peewee import SqliteDatabase, Model, CharField
import spacy
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)
CORS(app)  # Permitir solicitações de qualquer origem

# Configuração do banco de dados
db = SqliteDatabase('mensagens.db')

class Mensagem(Model):
    texto = CharField()

    class Meta:
        database = db

# Conectar ao banco de dados e criar tabelas
db.connect()
db.create_tables([Mensagem], safe=True)

# Carregar modelo spaCy em português
nlp = spacy.load("pt_core_news_sm")

# Inicializar lematizador e stopwords do NLTK
nltk.download('punkt')
nltk.download('stopwords')
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('portuguese'))

# Inicializar ChatBot
chatbot = ChatBot('MeuBot')

# Inicializar treinador fora da função de rota
trainer = ChatterBotCorpusTrainer(chatbot)

def preprocess_text(text):
    # Pré-processamento de texto usando spaCy e NLTK
    doc = nlp(text)
    tokens = [lemmatizer.lemmatize(token.text.lower()) for token in doc if token.text.lower() not in stop_words]
    return ' '.join(tokens)

@app.route('/salvar_mensagem', methods=['POST'])
def salvar_mensagem():
    try:
        data = request.get_json()
        user_input = data['mensagem']

        # Salvar a mensagem do usuário no banco de dados
        Mensagem.create(texto=user_input)

        return jsonify({'status': 'Mensagem salva com sucesso'})
    except Exception as e:
        # Imprimir detalhes da exceção no console
        print(f"Erro ao salvar mensagem: {str(e)}")
        return jsonify({'status': 'Erro ao salvar mensagem'})

@app.route('/treinar_chatbot', methods=['POST'])
def treinar_chatbot():
    try:
        data = request.get_json()
        user_input = data['mensagem']

        # Salvar a mensagem do usuário no banco de dados
        Mensagem.create(texto=user_input)

        return jsonify({'status': 'ChatBot treinado com sucesso'})
    except Exception as e:
        # Tratamento de exceção
        print(f"Erro ao treinar ChatBot: {str(e)}")
        return jsonify({'status': f'Erro ao treinar ChatBot: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
