import subprocess
import sys
import os
import logging

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log", mode="a")]
)

def check_dependencies():
    """Verifica se as dependências necessárias estão instaladas."""
    try:
        import streamlit  # Tenta importar o módulo Streamlit
        logging.info("Dependência 'streamlit' encontrada.")
    except ImportError:
        logging.error("O Streamlit não está instalado. Instale usando 'pip install streamlit'.")
        sys.exit(1)

def check_script_path():
    """Verifica se o arquivo dashboard.py existe no caminho especificado."""
    script_path = "src/visualization/dashboard.py"
    if not os.path.exists(script_path):
        logging.error(f"Arquivo '{script_path}' não encontrado. Verifique o caminho e tente novamente.")
        sys.exit(1)
    logging.info(f"Arquivo '{script_path}' encontrado com sucesso.")
    return script_path

def run_streamlit(script_path):
    """Inicia o Streamlit com o script especificado."""
    try:
        logging.info("Iniciando o Streamlit...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", script_path])
    except Exception as e:
        logging.error(f"Erro ao executar o Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    logging.info("Inicializando a aplicação...")
    check_dependencies()  # Verifica dependências
    script_path = check_script_path()  # Verifica o caminho do script
    run_streamlit(script_path)  # Inicia o Streamlit
