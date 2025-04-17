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

# Função para monitorar a tabela relatorios74
def monitor_relatorios74():
    """
    Monitoramento da tabela `relatorios74`:
    - Registros pendentes.
    - Registros incompletos.
    """
    engine = get_engine()  # Reutiliza a configuração do SQLAlchemy

    # Consulta para registros pendentes
    pending_query = """
    SELECT id, cod_cir, designacao, cliente, servico, tarefa, status
    FROM relatorios74
    WHERE status = 0
    ORDER BY id ASC;
    """

    # Consulta para registros incompletos
    incomplete_query = """
    SELECT id, cod_cir, designacao, cliente, servico, tarefa, status
    FROM relatorios74
    WHERE (cod_cir IS NULL OR designacao IS NULL OR cliente IS NULL OR servico IS NULL)
    AND status = 0
    ORDER BY id ASC;
    """

    try:
        # Executa as consultas
        pending_data = pd.read_sql(pending_query, engine)
        incomplete_data = pd.read_sql(incomplete_query, engine)

        # Loga os resultados
        print(f"Registros pendentes: {len(pending_data)}")
        print(f"Registros incompletos: {len(incomplete_data)}")
        print("\nExemplo de registros pendentes:")
        print(pending_data.head())  # Mostra os 5 primeiros registros pendentes

        return pending_data, incomplete_data
    except Exception as e:
        print(f"Erro ao monitorar a tabela relatorios74: {e}")
        raise
