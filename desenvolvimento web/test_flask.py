from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Olá, mundo!'

@app.route('/pagina')
def pagina():
    return render_template('pagina.html')

@app.route('/processar-formulario', methods=['POST'])
def processar_formulario():
    nome = request.form['nome']
    mensagem = 'Olá, ' + nome + '! Seu formulário foi enviado com sucesso.'
    return render_template('resultado.html', mensagem=mensagem)

if __name__ == '__main__':
    app.run()