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
