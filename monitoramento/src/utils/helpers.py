import os
from datetime import timedelta

def format_timedelta_to_string(td):
    """
    Converte um objeto timedelta em uma string formatada (horas:minutos:segundos).

    Args:
        td (timedelta): Objeto timedelta.

    Returns:
        str: String formatada (ex: "1:23:45").
    """
    if not isinstance(td, timedelta):
        return "N/A"
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}:{minutes:02}:{seconds:02}"

def get_env_variable(key, default=None):
    """
    Busca uma variável de ambiente.

    Args:
        key (str): Nome da variável.
        default: Valor padrão caso a variável não esteja configurada.

    Returns:
        str: Valor da variável de ambiente.
    """
    return os.getenv(key, default)
