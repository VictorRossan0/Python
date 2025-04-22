import logging
import streamlit as st
import pandas as pd
import plotly.express as px
from database.queries import fetch_execution_status
from processing.processing import calculate_execution_time
from dotenv import load_dotenv
from st_aggrid import AgGrid

# Configurações iniciais
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Título do Painel
st.title("Painel de Monitoramento de Automações")

# Função para carregar e processar dados de execuções
def load_execution_data():
    data = pd.DataFrame()
    try:
        data = fetch_execution_status()
        data["start_time"] = pd.to_datetime(data["start_time"], errors="coerce")
        data["end_time"] = pd.to_datetime(data["end_time"], errors="coerce")
        data.dropna(subset=["start_time", "end_time"], inplace=True)
        data = calculate_execution_time(data)
    except Exception as e:
        logger.error(f"Erro ao buscar ou processar dados de execuções: {e}")
        st.error("Falha ao carregar os dados de execuções.")
    return data

# Carregar dados
exec_data = load_execution_data()

# Menu de Navegação
menu = st.sidebar.radio("Menu", ["Resumo", "Detalhes", "Gráfico"])

if menu == "Resumo":
    st.header("Resumo das Execuções")
    if not exec_data.empty:
        total_execucoes = exec_data["entry_datetime"].notnull().sum()
        casos_ativos = exec_data["ativo"].sum()
        ultimo_end_time = exec_data["end_time"].max()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Execuções", total_execucoes)
        with col2:
            st.metric("Casos Ativos", casos_ativos)
        with col3:
            st.metric(
                "Última Data (D/M/A)",
                ultimo_end_time.strftime("%d/%m/%y") if ultimo_end_time else "N/A"
            )
        with col4:
            st.metric(
                "Último Horário (H:M:S)",
                ultimo_end_time.strftime("%H:%M:%S") if ultimo_end_time else "N/A"
            )
    else:
        st.warning("Nenhuma execução ativa ou recente encontrada.")

elif menu == "Detalhes":
    st.header("Detalhes das Execuções")
    if not exec_data.empty:
        st.subheader("Tabela de Execuções")
        AgGrid(
            exec_data,
            editable=True,
            sortable=True,
            filter=True,
            resizable=True,
            fit_columns_on_grid_load=True,
            theme="streamlit",
        )
    else:
        st.warning("Nenhum dado disponível para exibir.")

elif menu == "Gráfico":
    st.header("Gráficos das Execuções")
    if not exec_data.empty:
        # Gráfico de Execuções por Hora
        st.subheader("Execuções por Hora")
        exec_data["hour"] = exec_data["entry_datetime"].dt.floor("H")
        exec_data["formatted_hour"] = exec_data["hour"].apply(
            lambda x: x.strftime("%H:%M") if not pd.isnull(x) else "N/A"
        )
        execucoes_por_hora = exec_data[exec_data["formatted_hour"] != "N/A"].groupby(
            "formatted_hour"
        ).size().reset_index(name="count")
        fig_hora = px.bar(
            execucoes_por_hora,
            x="formatted_hour",
            y="count",
            title="Execuções por Hora",
            labels={"formatted_hour": "Hora (hh:mm)", "count": "Quantidade"},
            text="count",
        )
        fig_hora.update_layout(
            title_font_size=18,
            xaxis_title="Hora",
            yaxis_title="Execuções",
            template="plotly_white",
        )
        st.plotly_chart(fig_hora, use_container_width=True)

        # Gráfico de Execuções por Dia
        st.subheader("Execuções por Dia")
        exec_data["date"] = exec_data["entry_datetime"].dt.date
        exec_data["formatted_date"] = exec_data["date"].apply(
            lambda x: x.strftime("%d/%m/%y") if not pd.isnull(x) else "N/A"
        )
        execucoes_por_dia = exec_data[exec_data["formatted_date"] != "N/A"].groupby(
            "formatted_date"
        ).size().reset_index(name="count")
        execucoes_por_dia["formatted_date_sort"] = pd.to_datetime(
            execucoes_por_dia["formatted_date"], format="%d/%m/%y"
        )
        execucoes_por_dia = execucoes_por_dia.sort_values("formatted_date_sort")
        fig_dia = px.bar(
            execucoes_por_dia,
            x="formatted_date",
            y="count",
            title="Execuções por Dia",
            labels={"formatted_date": "Data (dd/mm/yy)", "count": "Quantidade"},
            text="count",
        )
        fig_dia.update_layout(
            title_font_size=18,
            xaxis_title="Data",
            yaxis_title="Execuções",
            template="plotly_white",
        )
        st.plotly_chart(fig_dia, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir.")
