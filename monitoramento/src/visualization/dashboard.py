from datetime import date
import logging
import streamlit as st
import pandas as pd
import plotly.express as px
from database.queries import monitor_jarvas_agendamento_13_update, monitor_relatorios74_update, monitor_relatorios_update
from processing.processing import calculate_execution_time, calculate_execution_time_2, calculate_execution_time_3
from dotenv import load_dotenv
from st_aggrid import AgGrid

# Configuração da página deve ser a primeira chamada do Streamlit
st.set_page_config(
    page_title="Painel de Monitoramento",
    page_icon="📊",
    layout="wide",
)

# Configurações iniciais
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""Função principal para executar o aplicativo Streamlit."""
# Título e descrição
st.title("📊 Painel de Monitoramento de Automações")
st.markdown(
    "Este painel fornece informações em tempo real sobre o desempenho e histórico das suas automações. Visualize métricas, tendências e detalhes relevantes."
)
st.sidebar.title("Menu de Navegação")
st.sidebar.markdown("Selecione uma opção no menu para visualizar os dados.")


# Função para carregar e processar dados do Painel 1 (jarvas_agendamento_13)
def load_execution_data():
    data = pd.DataFrame()
    try:
        data = monitor_jarvas_agendamento_13_update()
        data["start_time"] = pd.to_datetime(data["start_time"],
                                            errors="coerce")
        data["end_time"] = pd.to_datetime(data["end_time"], errors="coerce")
        data.dropna(subset=["start_time", "end_time"], inplace=True)
        data = calculate_execution_time(data)
    except Exception as e:
        logger.error(f"Erro ao buscar ou processar dados do Painel 1: {e}")
        st.error("Falha ao carregar os dados do Painel 1.")
    return data


# Função para carregar e processar dados do Painel 2 (relatorios74)
def load_reports_data_relatorios74():
    data = pd.DataFrame()
    try:
        data = monitor_relatorios74_update()

        # Converter colunas de data/hora
        data["data_hora_extracao"] = pd.to_datetime(data["data_hora_extracao"],
                                                    errors="coerce")
        data["updated_at"] = pd.to_datetime(data["updated_at"],
                                            errors="coerce")

        # Remover valores nulos
        data.dropna(subset=["data_hora_extracao", "updated_at"], inplace=True)

        # Filtrar apenas mensagens que começam com "Pré-Ativação:"
        data["valid_obs"] = data["obs"].astype(str).str.startswith(
            "Pré-Ativação:")

        # Calcular tempo de execução
        data = calculate_execution_time_2(data)
    except Exception as e:
        logger.error(f"Erro ao buscar ou processar dados do Painel 2: {e}")
        st.error("Falha ao carregar os dados do Painel 2.")
    return data


# Função para carregar e processar dados do Painel 3 (relatorios)
def load_reports_data_relatorios():
    data = pd.DataFrame()
    try:
        data = monitor_relatorios_update()
        data["data_hora_extracao"] = pd.to_datetime(data["data_hora_extracao"],
                                                    errors="coerce")
        data["updated_at"] = pd.to_datetime(data["updated_at"],
                                            errors="coerce")
        data.dropna(subset=["data_hora_extracao", "updated_at"], inplace=True)
        data = calculate_execution_time_3(data)
    except Exception as e:
        logger.error(f"Erro ao buscar ou processar dados do Painel 3: {e}")
        st.error("Falha ao carregar os dados do Painel 3.")
    return data


# Carregar dados
exec_data = load_execution_data()
report_data_2 = load_reports_data_relatorios74()
report_data = load_reports_data_relatorios()

# Menu Principal
menu = st.sidebar.radio("Menu", ["Painel 1", "Painel 2", "Painel 3"])

if menu == "Painel 1":
    submenu = st.sidebar.radio("Submenu", ["Resumo", "Gráficos"])

    if submenu == "Resumo":
        st.header("Resumo do Painel 1 - jarvas_agendamento_13")
        if not exec_data.empty:
            # Criar a coluna "date" com base na coluna "exec_data"
            exec_data["date"] = exec_data["entry_datetime"].dt.date

            # Obter a data atual
            hoje = date.today()

            # Filtrar os dados apenas para o dia atual
            execucoes_hoje = exec_data[exec_data["date"] == hoje]

            # Adicionar uma coluna com a hora
            execucoes_hoje.loc[:, "hour"] = execucoes_hoje[
                "entry_datetime"].dt.hour

            # Contar as horas distintas em que ocorreram execuções
            execucoes_distintas_por_hora = execucoes_hoje["hour"].nunique()

            casos_ativos = exec_data["ativo"].sum()
            ultimo_end_time = exec_data["end_time"].max()

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total de Execuções no Dia",
                          execucoes_distintas_por_hora)
            with col2:
                st.metric("Casos Ativos na Fila", casos_ativos)
            with col3:
                st.metric(
                    "Última Data (D/M/A)",
                    ultimo_end_time.strftime("%d/%m/%y")
                    if ultimo_end_time else "N/A")
            with col4:
                st.metric(
                    "Último Horário (H:M:S)",
                    ultimo_end_time.strftime("%H:%M:%S")
                    if ultimo_end_time else "N/A")
        else:
            st.warning("Nenhuma execução ativa ou recente encontrada.")

    elif submenu == "Gráficos":
        st.header("Gráficos do Painel 1")
        if not exec_data.empty:
            # Gráfico de Execuções por Hora
            st.subheader("Execuções por Hora")
            # Criar a coluna de hora arredondada para a hora exata
            exec_data["hour"] = exec_data["entry_datetime"].dt.floor("H")
            exec_data["formatted_hour"] = exec_data["hour"].apply(
                lambda x: x.strftime("%H:%M") if not pd.isnull(x) else "N/A")

            # Agrupar por hora e contar os dias distintos (usando "date" e "hour")
            exec_data["date"] = exec_data["entry_datetime"].dt.date
            execucoes_por_hora = exec_data[
                exec_data["formatted_hour"] != "N/A"].groupby(
                    ["formatted_hour",
                     "date"]).size().reset_index(name="count")

            # Agora, para cada hora, contar os dias distintos
            execucoes_por_hora_distintas = execucoes_por_hora.groupby(
                "formatted_hour")["date"].nunique().reset_index(
                    name="dias_distintos")

            # Gerar o gráfico de execuções por hora
            fig_hora = px.bar(
                execucoes_por_hora_distintas,
                x="formatted_hour",
                y="dias_distintos",
                title="Execuções por Hora (em Dias Distintos)",
                labels={
                    "formatted_hour": "Hora (hh:mm)",
                    "dias_distintos": "Quantidade de Dias"
                },
                text="dias_distintos",
            )
            fig_hora.update_layout(
                title_font_size=18,
                xaxis_title="Hora",
                yaxis_title="Dias Distintos",
                template="plotly_white",
            )
            st.plotly_chart(fig_hora, use_container_width=True)

            # Gráfico de Execuções por Dia
            st.subheader("Execuções por Dia")
            # Criar a coluna de data
            exec_data["formatted_date"] = exec_data["date"].apply(
                lambda x: x.strftime("%d/%m/%y")
                if not pd.isnull(x) else "N/A")

            # Criar a coluna de hora, mas agora considerando apenas a hora (ignorando minutos e segundos)
            exec_data["hour_only"] = exec_data["entry_datetime"].dt.floor("H")

            # Agrupar por data e hora, e contar os horários distintos em que ocorreram execuções no dia
            execucoes_por_dia_distintas = exec_data[
                exec_data["formatted_date"] != "N/A"].drop_duplicates(
                    subset=["formatted_date",
                            "hour_only"])  # Remover duplicatas de data e hora

            # Contar a quantidade de horas distintas por data
            execucoes_por_dia = execucoes_por_dia_distintas.groupby(
                "formatted_date").size().reset_index(name="count")

            # Ordenar as datas de forma crescente
            execucoes_por_dia["formatted_date_sort"] = pd.to_datetime(
                execucoes_por_dia["formatted_date"], format="%d/%m/%y")
            execucoes_por_dia = execucoes_por_dia.sort_values(
                "formatted_date_sort")

            # Criar o gráfico de barras
            fig_dia = px.bar(
                execucoes_por_dia,
                x="formatted_date",
                y="count",
                title="Execuções por Dia (em Horas Distintos)",
                labels={
                    "formatted_date": "Data (dd/mm/yy)",
                    "count": "Quantidade de Horários Distintos"
                },
                text="count",
            )

            fig_dia.update_layout(
                title_font_size=18,
                xaxis_title="Data",
                yaxis_title="Quantidade de Horários Distintos",
                template="plotly_white",
            )

            # Exibir o gráfico
            st.plotly_chart(fig_dia, use_container_width=True)

elif menu == "Painel 2":
    submenu = st.sidebar.radio("Submenu", ["Resumo", "Gráficos"])

    if submenu == "Resumo":
        st.header("Resumo do Painel 2 - relatorios74")
        if not report_data_2.empty:
            # Criar a coluna "date" com base na coluna "data_hora_extracao"
            report_data_2["date"] = report_data_2["data_hora_extracao"].dt.date

            # Obter a data atual
            hoje = date.today()

            # Filtrar os dados apenas para o dia atual
            execucoes_hoje = report_data_2[report_data_2["date"] == hoje]

            # Adicionar uma coluna com a hora
            execucoes_hoje.loc[:, "hour"] = execucoes_hoje[
                "data_hora_extracao"].dt.hour

            # Contar as horas distintas em que ocorreram execuções
            execucoes_distintas_por_hora = execucoes_hoje["hour"].nunique()

            mensagens_validas_hoje = report_data_2["valid_obs"].sum()

            ultimo_end_time_2 = report_data_2["updated_at"].max()

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total de Execuções no Dia",
                          execucoes_distintas_por_hora)
            with col2:
                st.metric("Total de Processos Válidos no WF",
                          mensagens_validas_hoje)
            with col3:
                st.metric(
                    "Última Data (D/M/A)",
                    ultimo_end_time_2.strftime("%d/%m/%y")
                    if ultimo_end_time_2 else "N/A",
                )
            with col4:
                st.metric(
                    "Último Horário (H:M:S)",
                    ultimo_end_time_2.strftime("%H:%M:%S")
                    if ultimo_end_time_2 else "N/A",
                )
        else:
            st.warning("Nenhum dado encontrado no Painel 2.")

    elif submenu == "Gráficos":
        st.header("Gráficos do Painel 2")
        if not report_data_2.empty:
            # Gráfico de Execuções por Hora
            st.subheader("Execuções por Hora")
            # Criar a coluna de hora arredondada para a hora exata
            report_data_2["hour"] = report_data_2[
                "data_hora_extracao"].dt.floor("h")
            report_data_2["formatted_hour"] = report_data_2["hour"].apply(
                lambda x: x.strftime("%H:%M") if not pd.isnull(x) else "N/A")

            # Agrupar por hora e contar os dias distintos (usando "date" e "hour")
            report_data_2["date"] = report_data_2["data_hora_extracao"].dt.date
            execucoes_por_hora = report_data_2[
                report_data_2["formatted_hour"] != "N/A"].groupby(
                    ["formatted_hour",
                     "date"]).size().reset_index(name="count")

            # Agora, para cada hora, contar os dias distintos
            execucoes_por_hora_distintas = execucoes_por_hora.groupby(
                "formatted_hour")["date"].nunique().reset_index(
                    name="dias_distintos")

            # Gerar o gráfico de execuções por hora
            fig_hora = px.bar(
                execucoes_por_hora_distintas,
                x="formatted_hour",
                y="dias_distintos",
                title="Execuções por Hora (em Dias Distintos)",
                labels={
                    "formatted_hour": "Hora (hh:mm)",
                    "dias_distintos": "Quantidade de Dias"
                },
                text="dias_distintos",
            )
            fig_hora.update_layout(
                title_font_size=18,
                xaxis_title="Hora",
                yaxis_title="Dias Distintos",
                template="plotly_white",
            )
            st.plotly_chart(fig_hora, use_container_width=True)

            # Gráfico de Execuções por Dia
            st.subheader("Execuções por Dia")
            # Criar a coluna de data
            report_data_2["formatted_date"] = report_data_2["date"].apply(
                lambda x: x.strftime("%d/%m/%y")
                if not pd.isnull(x) else "N/A")

            # Criar a coluna de hora, mas agora considerando apenas a hora (ignorando minutos e segundos)
            report_data_2["hour_only"] = report_data_2[
                "data_hora_extracao"].dt.floor("H")

            # Agrupar por data e hora, e contar os horários distintos em que ocorreram execuções no dia
            execucoes_por_dia_distintas = report_data_2[
                report_data_2["formatted_date"] != "N/A"].drop_duplicates(
                    subset=["formatted_date",
                            "hour_only"])  # Remover duplicatas de data e hora

            # Contar a quantidade de horas distintas por data
            execucoes_por_dia = execucoes_por_dia_distintas.groupby(
                "formatted_date").size().reset_index(name="count")

            # Ordenar as datas de forma crescente
            execucoes_por_dia["formatted_date_sort_2"] = pd.to_datetime(
                execucoes_por_dia["formatted_date"], format="%d/%m/%y")
            execucoes_por_dia = execucoes_por_dia.sort_values(
                "formatted_date_sort_2")

            # Criar o gráfico de barras
            fig_dia = px.bar(
                execucoes_por_dia,
                x="formatted_date",
                y="count",
                title="Execuções por Dia (em Horas Distintos)",
                labels={
                    "formatted_date": "Data (dd/mm/yy)",
                    "count": "Quantidade de Horários Distintos"
                },
                text="count",
            )

            fig_dia.update_layout(
                title_font_size=18,
                xaxis_title="Data",
                yaxis_title="Quantidade de Horários Distintos",
                template="plotly_white",
            )

            # Exibir o gráfico
            st.plotly_chart(fig_dia, use_container_width=True)

elif menu == "Painel 3":
    submenu = st.sidebar.radio("Submenu", ["Resumo", "Gráficos"])

    if submenu == "Resumo":
        st.header("Resumo do Painel 3 - relatorios")
        if not report_data.empty:
            # Criar a coluna "date" com base na coluna "data_hora_extracao"
            report_data["date"] = report_data["data_hora_extracao"].dt.date

            # Obter a data atual
            hoje = date.today()

            # Filtrar os dados apenas para o dia atual
            execucoes_hoje = report_data[report_data["date"] == hoje]

            # Adicionar uma coluna com a hora
            execucoes_hoje.loc[:, "hour"] = execucoes_hoje[
                "data_hora_extracao"].dt.hour

            # Contar as horas distintas em que ocorreram execuções
            execucoes_distintas_por_hora = execucoes_hoje["hour"].nunique()

            ultimo_end_time = report_data["updated_at"].max()

            col1, col2, col4 = st.columns(3)
            with col1:
                st.metric("Total de Execuções no Dia",
                          execucoes_distintas_por_hora)
            with col2:
                st.metric(
                    "Última Data (D/M/A)",
                    ultimo_end_time.strftime("%d/%m/%y")
                    if ultimo_end_time else "N/A",
                )
            with col4:
                st.metric(
                    "Último Horário (H:M:S)",
                    ultimo_end_time.strftime("%H:%M:%S")
                    if ultimo_end_time else "N/A",
                )
        else:
            st.warning("Nenhum dado encontrado no Painel 2.")

    elif submenu == "Gráficos":
        st.header("Gráficos do Painel 2")
        if not report_data.empty:
            # Gráfico de Execuções por Hora
            st.subheader("Execuções por Hora")
            # Criar a coluna de hora arredondada para a hora exata
            report_data["hour"] = report_data["data_hora_extracao"].dt.floor(
                "h")
            report_data["formatted_hour"] = report_data["hour"].apply(
                lambda x: x.strftime("%H:%M") if not pd.isnull(x) else "N/A")

            # Agrupar por hora e contar os dias distintos (usando "date" e "hour")
            report_data["date"] = report_data["data_hora_extracao"].dt.date
            execucoes_por_hora = report_data[
                report_data["formatted_hour"] != "N/A"].groupby(
                    ["formatted_hour",
                     "date"]).size().reset_index(name="count")

            # Agora, para cada hora, contar os dias distintos
            execucoes_por_hora_distintas = execucoes_por_hora.groupby(
                "formatted_hour")["date"].nunique().reset_index(
                    name="dias_distintos")

            # Gerar o gráfico de execuções por hora
            fig_hora = px.bar(
                execucoes_por_hora_distintas,
                x="formatted_hour",
                y="dias_distintos",
                title="Execuções por Hora (em Dias Distintos)",
                labels={
                    "formatted_hour": "Hora (hh:mm)",
                    "dias_distintos": "Quantidade de Dias"
                },
                text="dias_distintos",
            )
            fig_hora.update_layout(
                title_font_size=18,
                xaxis_title="Hora",
                yaxis_title="Dias Distintos",
                template="plotly_white",
            )
            st.plotly_chart(fig_hora, use_container_width=True)

            # Gráfico de Execuções por Dia
            st.subheader("Execuções por Dia")
            # Criar a coluna de data
            report_data["formatted_date"] = report_data["date"].apply(
                lambda x: x.strftime("%d/%m/%y")
                if not pd.isnull(x) else "N/A")

            # Criar a coluna de hora, mas agora considerando apenas a hora (ignorando minutos e segundos)
            report_data["hour_only"] = report_data[
                "data_hora_extracao"].dt.floor("H")

            # Agrupar por data e hora, e contar os horários distintos em que ocorreram execuções no dia
            execucoes_por_dia_distintas = report_data[
                report_data["formatted_date"] != "N/A"].drop_duplicates(
                    subset=["formatted_date",
                            "hour_only"])  # Remover duplicatas de data e hora

            # Contar a quantidade de horas distintas por data
            execucoes_por_dia = execucoes_por_dia_distintas.groupby(
                "formatted_date").size().reset_index(name="count")

            # Ordenar as datas de forma crescente
            execucoes_por_dia["formatted_date_sort"] = pd.to_datetime(
                execucoes_por_dia["formatted_date"], format="%d/%m/%y")
            execucoes_por_dia = execucoes_por_dia.sort_values(
                "formatted_date_sort")

            # Criar o gráfico de barras
            fig_dia = px.bar(
                execucoes_por_dia,
                x="formatted_date",
                y="count",
                title="Execuções por Dia (em Horas Distintos)",
                labels={
                    "formatted_date": "Data (dd/mm/yy)",
                    "count": "Quantidade de Horários Distintos"
                },
                text="count",
            )

            fig_dia.update_layout(
                title_font_size=18,
                xaxis_title="Data",
                yaxis_title="Quantidade de Horários Distintos",
                template="plotly_white",
            )

            # Exibir o gráfico
            st.plotly_chart(fig_dia, use_container_width=True)
