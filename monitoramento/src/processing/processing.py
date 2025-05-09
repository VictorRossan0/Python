import pandas as pd

def calculate_execution_time(data):
    """
    Calcula o tempo de execução para cada registro.

    Args:
        data (pd.DataFrame): Dados das execuções.

    Returns:
        pd.DataFrame: Dados com coluna adicional `execution_time`.
    """
    data["execution_time"] = (
        pd.to_datetime(data["end_time"]) - pd.to_datetime(data["start_time"])
    ).dt.total_seconds()
    return data

def calculate_execution_time_2(data):
    """
    Calcula o tempo de execução para cada registro.

    Args:
        data (pd.DataFrame): Dados das execuções.

    Returns:
        pd.DataFrame: Dados com coluna adicional `execution_time`.
    """
    data["execution_time"] = (
        pd.to_datetime(data["updated_at"]) - pd.to_datetime(data["data_hora_extracao"])
    ).dt.total_seconds()
    return data