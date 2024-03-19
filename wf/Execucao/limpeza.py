import os

def limpar_diretorio(caminho_diretorio):
    for arquivo in os.listdir(caminho_diretorio):
        caminho_arquivo = os.path.join(caminho_diretorio, arquivo)
        try:
            if os.path.isfile(caminho_arquivo):
                os.unlink(caminho_arquivo)
        except Exception as e:
            print(f"Erro ao excluir {caminho_arquivo}: {e}")

def limpar_pycache():
    caminho_pycache = '__pycache__'
    limpar_diretorio(caminho_pycache)