import logging
import streamlit as st
import pandas as pd
import plotly.express as px
from database.queries import fetch_execution_status, monitor_status_updates
from processing.processing import calculate_execution_time
from dotenv import load_dotenv
from st_aggrid import AgGrid

# Configurações iniciais
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Título do Painel
st.title("Painel de Monitoramento de Automações")

# Função para carregar e processar dados do Relatório 1 (jarvas_agendamento_13)
def load_execution_data():
    data = pd.DataFrame()
    try:
        data = fetch_execution_status()
        data["start_time"] = pd.to_datetime(data["start_time"], errors="coerce")
        data["end_time"] = pd.to_datetime(data["end_time"], errors="coerce")
        data.dropna(subset=["start_time", "end_time"], inplace=True)
        data = calculate_execution_time(data)
    except Exception as e:
        logger.error(f"Erro ao buscar ou processar dados do Relatório 1: {e}")
        st.error("Falha ao carregar os dados do Relatório 1.")
    return data

# Função para carregar e processar dados do Relatório 2 (relatorios74)
def load_reports_data():
    data = pd.DataFrame()
    try:
        data = monitor_status_updates()
        data["data_hora_extracao"] = pd.to_datetime(data["data_hora_extracao"], errors="coerce")
        data.dropna(subset=["data_hora_extracao"], inplace=True)
    except Exception as e:
        logger.error(f"Erro ao buscar ou processar dados do Relatório 2: {e}")
        st.error("Falha ao carregar os dados do Relatório 2.")
    return data

# Carregar dados
exec_data = load_execution_data()
report_data = load_reports_data()

# Menu Principal
menu = st.sidebar.radio("Menu", ["Relatório 1", "Relatório 2"])

if menu == "Relatório 1":
    submenu = st.sidebar.radio("Submenu", ["Resumo", "Detalhes", "Gráficos"])

    if submenu == "Resumo":
        st.header("Resumo do Relatório 1")
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
                    ultimo_end_time.strftime("%d/%m/%y") if ultimo_end_time else "N/A")
            with col4:
                st.metric(
                    "Último Horário (H:M:S)",
                    ultimo_end_time.strftime("%H:%M:%S") if ultimo_end_time else "N/A")
        else:
            st.warning("Nenhuma execução ativa ou recente encontrada.")

    elif submenu == "Detalhes":
        st.header("Detalhes do Relatório 1")
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
            st.warning("Nenhuma execução ativa ou recente encontrada.")

    elif submenu == "Gráficos":
        st.header("Gráficos das Execuções")
        if not exec_data.empty:
            # Gráfico de Execuções por Hora
            st.subheader("Execuções por Hora")
            exec_data["hour"] = exec_data["entry_datetime"].dt.floor("h")  # Atualizado de "H" para "h"
            exec_data["formatted_hour"] = exec_data["hour"].apply(
                lambda x: x.strftime("%H:%M") if not pd.isnull(x) else "N/A")
            execucoes_por_hora = exec_data[exec_data["formatted_hour"] != "N/A"].groupby(
                "formatted_hour").size().reset_index(name="count")
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
                lambda x: x.strftime("%d/%m/%y") if not pd.isnull(x) else "N/A")
            execucoes_por_dia = exec_data[exec_data["formatted_date"] != "N/A"].groupby(
                "formatted_date").size().reset_index(name="count")
            execucoes_por_dia["formatted_date_sort"] = pd.to_datetime(
                execucoes_por_dia["formatted_date"], format="%d/%m/%y")
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

elif menu == "Relatório 2":
    submenu = st.sidebar.radio("Submenu", ["Resumo", "Detalhes", "Gráficos"])

    if submenu == "Resumo":
        st.header("Resumo do Relatório 2")
        if not report_data.empty:
            total_execucoes_2 = report_data["data_hora_extracao"].notnull().sum()
            casos_ativos_2 = report_data["status"].sum()
            ultimo_end_time_2 = report_data["data_hora_extracao"].max()

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total de Execuções", total_execucoes_2)
            with col2:
                st.metric("Casos Ativos", casos_ativos_2)
            with col3:
                st.metric(
                    "Última Data (D/M/A)",
                    ultimo_end_time_2.strftime("%d/%m/%y") if ultimo_end_time_2 else "N/A")
            with col4:
                st.metric(
                    "Último Horário (H:M:S)",
                    ultimo_end_time_2.strftime("%H:%M:%S") if ultimo_end_time_2 else "N/A")
        else:
            st.warning("Nenhum dado encontrado no Relatório 2.")

    elif submenu == "Detalhes":
        st.header("Detalhes do Relatório 2")
        if not report_data.empty:
            st.subheader("Tabela de Relatórios")
            AgGrid(
                report_data,
                editable=True,
                sortable=True,
                filter=True,
                resizable=True,
                fit_columns_on_grid_load=True,
                theme="streamlit",
            )
        else:
            st.warning("Nenhum dado disponível para exibir.")

    elif submenu == "Gráficos":
        st.header("Gráficos do Relatório 2")
        if not report_data.empty:
            # Gráfico de Execuções por Hora
            st.subheader("Execuções por Hora")
            report_data["hour_2"] = report_data["data_hora_extracao"].dt.floor("h")  # Atualizado de "H" para "h"
            report_data["formatted_hour_2"] = report_data["hour_2"].apply(
                lambda x: x.strftime("%H:%M") if not pd.isnull(x) else "N/A")
            execucoes_por_hora = report_data[
                report_data["formatted_hour_2"] != "N/A"].groupby(
                    "formatted_hour_2").size().reset_index(name="count")
            fig_hora = px.bar(
                execucoes_por_hora,
                x="formatted_hour_2",
                y="count",
                title="Execuções por Hora",
                labels={"formatted_hour_2": "Hora (hh:mm)", "count": "Quantidade"},
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
            report_data["date_2"] = report_data["data_hora_extracao"].dt.date
            report_data["formatted_date_2"] = report_data["date_2"].apply(
                lambda x: x.strftime("%d/%m/%y") if not pd.isnull(x) else "N/A")
            execucoes_por_dia = report_data[
                report_data["formatted_date_2"] != "N/A"].groupby(
                    "formatted_date_2").size().reset_index(name="count")
            execucoes_por_dia["formatted_date_sort_2"] = pd.to_datetime(
                execucoes_por_dia["formatted_date_2"], format="%d/%m/%y")
            execucoes_por_dia = execucoes_por_dia.sort_values("formatted_date_sort_2")
            fig_dia = px.bar(
                execucoes_por_dia,
                x="formatted_date_2",
                y="count",
                title="Execuções por Dia",
                labels={"formatted_date_2": "Data (dd/mm/yy)", "count": "Quantidade"},
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
