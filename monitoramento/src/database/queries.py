from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime, timedelta
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

# Função para monitorar atualizações na tabela jarvas_agendamento_13
def monitor_jarvas_agendamento_13_update():
    """
    Busca o status das execuções na tabela `jarvas_agendamento_13`.
    """
    engine = get_engine()
    query = """
    SELECT id, entry_datetime, start_time, end_time, updated_at, ativo
    FROM jarvas_agendamento_13
    WHERE ativo = 1
    ORDER BY id DESC;
    """
    try:
        data = pd.read_sql(query, engine)
        print("Consulta de agendamentos executada com sucesso!")
        return data
    except Exception as e:
        print(f"Erro ao executar a consulta de agendamentos: {e}")
        raise

# Função para monitorar atualizações na tabela relatorios74
def monitor_relatorios74_update():
    """
    Busca registros da tabela `relatorios74` para monitorar atualizações de status e data/hora.
    """
    engine = get_engine()
    query = f"""
    SELECT id, status, created_at, updated_at, data_hora_extracao, obs
    FROM relatorios74
    WHERE status = 1
    ORDER BY id DESC;
    """

    try:
        data = pd.read_sql(query, engine)
        print("Consulta de monitoramento executada com sucesso!")
        return data
    except Exception as e:
        print(f"Erro ao monitorar status e atualizações: {e}")
        raise

# Função para monitorar atualizações na tabela relatorios
def monitor_relatorios_update():
    """
    Busca registros da tabela `relatorios` para monitorar atualizações de status e data/hora.
    """
    engine = get_engine()
    query = f"""
    SELECT id, status, created_at, updated_at, data_hora_extracao, obs
    FROM relatorios
    WHERE status = 1
    ORDER BY id DESC;
    """

    try:
        data = pd.read_sql(query, engine)
        print("Consulta de monitoramento executada com sucesso!")
        return data
    except Exception as e:
        print(f"Erro ao monitorar status e atualizações: {e}")
        raise