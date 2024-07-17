# portfolio/historico.py
import json
import os

# Diretório para armazenar arquivos JSON
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

def registrar_movimentacao(tipo, valor, data, nome_arquivo='historico.json'):
    caminho_arquivo = os.path.join(DATA_DIR, nome_arquivo)
    try:
        with open(caminho_arquivo, 'r') as f:
            historico = json.load(f)
    except FileNotFoundError:
        historico = []

    historico.append({
        'tipo': tipo,
        'valor': valor,
        'data': data
    })

    with open(caminho_arquivo, 'w') as f:
        json.dump(historico, f, indent=4)

def carregar_historico(nome_arquivo='historico.json'):
    caminho_arquivo = os.path.join(DATA_DIR, nome_arquivo)
    try:
        with open(caminho_arquivo, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
