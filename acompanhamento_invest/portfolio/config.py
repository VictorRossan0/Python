import json

def carregar_configuracoes(nome_arquivo='config.json'):
    with open(nome_arquivo, 'r') as f:
        return json.load(f)

def salvar_configuracoes(configuracoes, nome_arquivo='config.json'):
    with open(nome_arquivo, 'w') as f:
        json.dump(configuracoes, f, indent=4)
