from sqlalchemy import create_engine
import pandas as pd
from utils.helpers import get_env_variable

# Configuração do SQLAlchemy
def get_engine():
    """
    Cria uma conexão com o banco de dados usando SQLAlchemy.
    """
    db_host = get_env_variable("DB_HOST")
    db_user = get_env_variable("DB_USER")
    db_password = get_env_variable("DB_PASSWORD")
    db_name = get_env_variable("DB_NAME")

    engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
    return engine

# Função para buscar status de execução de agendamentos
def fetch_execution_status():
    """
    Busca o status das execuções na tabela `jarvas_agendamento_13`.
    """
    engine = get_engine()
    query = """
    SELECT id, entry_datetime, start_time, end_time, updated_at, ativo
    FROM jarvas_agendamento_13
    WHERE ativo = 1
    ORDER BY id ASC;
    """
    try:
        data = pd.read_sql(query, engine)
        print("Consulta de agendamentos executada com sucesso!")
        return data
    except Exception as e:
        print(f"Erro ao executar a consulta de agendamentos: {e}")
        raise
