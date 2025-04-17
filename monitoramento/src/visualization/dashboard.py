import logging
import streamlit as st
import pandas as pd
import plotly.express as px
from database.queries import fetch_execution_status, monitor_relatorios74
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

# Função para carregar e processar dados de relatórios
def load_reports_data():
    data = pd.DataFrame()
    try:
        data = monitor_relatorios74()
        data["data_hora_extracao"] = pd.to_datetime(data["data_hora_extracao"], errors="coerce")
    except Exception as e:
        logger.error(f"Erro ao buscar ou processar dados de relatórios: {e}")
        st.error("Falha ao carregar os dados de relatórios.")
    return data

# Carregar dados
exec_data = load_execution_data()
report_data = load_reports_data()

# Separação de abas
menu = st.sidebar.radio("Menu", ["Execuções Ativas", "Relatórios Pendentes/Incompletos"])

if menu == "Execuções Ativas":
    st.header("Monitoramento das Execuções")
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
        st.warning("Nenhuma execução ativa ou recente encontrada.")

elif menu == "Relatórios Pendentes/Incompletos":
    st.header("Monitoramento dos Relatórios")
    if not report_data.empty:
        pendentes = report_data[report_data["status"] == 0]
        incompletos = report_data[report_data["data_hora_extracao"].isna()]

        st.subheader("Resumo dos Relatórios")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Relatórios Pendentes", len(pendentes))
        with col2:
            st.metric("Relatórios Incompletos", len(incompletos))

        st.subheader("Gráfico de Relatórios Pendentes por Status")
        status_counts = report_data["status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Quantidade"]
        fig_status = px.pie(
            status_counts,
            names="Status",
            values="Quantidade",
            title="Distribuição de Relatórios por Status",
            template="plotly_white",
        )
        st.plotly_chart(fig_status, use_container_width=True)

        st.subheader("Gráfico de Relatórios por Data de Extração")
        valid_extraction = report_data[report_data["data_hora_extracao"].notna()]
        valid_extraction["formatted_date"] = valid_extraction["data_hora_extracao"].dt.date
        date_counts = valid_extraction.groupby("formatted_date").size().reset_index(name="Quantidade")
        fig_date = px.bar(
            date_counts,
            x="formatted_date",
            y="Quantidade",
            title="Relatórios por Data de Extração",
            labels={"formatted_date": "Data", "Quantidade": "Quantidade"},
            template="plotly_white",
        )
        st.plotly_chart(fig_date, use_container_width=True)

        st.subheader("Tabela de Relatórios Pendentes")
        AgGrid(
            pendentes,
            editable=True,
            sortable=True,
            filter=True,
            resizable=True,
            fit_columns_on_grid_load=True,
            theme="streamlit",
        )

        st.subheader("Tabela de Relatórios Incompletos")
        AgGrid(
            incompletos,
            editable=True,
            sortable=True,
            filter=True,
            resizable=True,
            fit_columns_on_grid_load=True,
            theme="streamlit",
        )
    else:
        st.warning("Nenhum dado de relatório disponível para exibir.")
