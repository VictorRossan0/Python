# Bibliotecas principais
from datetime import date  # Para manipulação de datas
import logging  # Para logs de erro e informação
import streamlit as st  # Framework de dashboard web
import pandas as pd  # Manipulação de dados tabulares
import plotly.express as px  # Gráficos interativos

# Funções do projeto
from database.queries import monitor_jarvas_agendamento_13_update, monitor_relatorios74_update, monitor_relatorios_update, get_email_delivery_report
from processing.processing import calculate_execution_time, calculate_execution_time_2, calculate_execution_time_3
from dotenv import load_dotenv  # Carregar variáveis de ambiente
from st_aggrid import AgGrid  # Tabela interativa (não utilizada neste trecho)

# Configuração da página do Streamlit
# (deve ser a primeira chamada do Streamlit)
st.set_page_config(
    page_title="Painel de Monitoramento",  # Título da aba
    page_icon="📊",  # Ícone da aba
    layout="centered",  # Layout centralizado
)

# Carrega variáveis de ambiente e configura logging
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Título e descrição do dashboard
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
        # Consulta os dados da tabela jarvas_agendamento_13
        data = monitor_jarvas_agendamento_13_update()

        # Converte colunas de data/hora para datetime
        data["start_time"] = pd.to_datetime(data["start_time"],
                                            errors="coerce")
        data["end_time"] = pd.to_datetime(data["end_time"], errors="coerce")

        # Remove registros sem datas válidas
        data.dropna(subset=["start_time", "end_time"], inplace=True)

        # Calcula o tempo de execução (diferença entre end_time e start_time)
        data = calculate_execution_time(data)
    except Exception as e:
        # Loga e exibe erro caso haja falha no carregamento ou processamento
        logger.error(f"Erro ao buscar ou processar dados do Painel 1: {e}")
        st.error("Falha ao carregar os dados do Painel 1.")
    return data


# Função para carregar e processar dados do Painel 2 (relatorios74)
def load_reports_data_relatorios74():
    data = pd.DataFrame()
    try:
        # Consulta os dados da tabela relatorios74
        data = monitor_relatorios74_update()

        # Converte as colunas de data/hora para o tipo datetime
        data["data_hora_extracao"] = pd.to_datetime(data["data_hora_extracao"],
                                                    errors="coerce")
        data["updated_at"] = pd.to_datetime(data["updated_at"],
                                            errors="coerce")

        # Remove registros com valores nulos nas datas principais
        data.dropna(subset=["data_hora_extracao", "updated_at"], inplace=True)

        # Cria coluna booleana indicando se a observação começa com "Pré-Ativação:"
        data["valid_obs"] = data["obs"].astype(str).str.startswith(
            "Pré-Ativação:")

        # Calcula o backlog como a soma de valores nulos na coluna 'obs' (para uso em métricas)
        data["backlog"] = data["obs"].isnull().sum()

        # Calcula o tempo de execução (diferença entre updated_at e data_hora_extracao)
        data = calculate_execution_time_2(data)
    except Exception as e:
        # Loga e exibe erro caso haja falha no carregamento ou processamento
        logger.error(f"Erro ao buscar ou processar dados do Painel 2: {e}")
        st.error("Falha ao carregar os dados do Painel 2.")
    return data


# Função para carregar e processar dados do Painel 3 (relatorios)
def load_reports_data_relatorios():
    data = pd.DataFrame()
    try:
        # Consulta os dados da tabela relatorios
        data = monitor_relatorios_update()

        # Converte colunas de data/hora para datetime
        data["data_hora_extracao"] = pd.to_datetime(data["data_hora_extracao"],
                                                    errors="coerce")
        data["updated_at"] = pd.to_datetime(data["updated_at"],
                                            errors="coerce")

        # Remove registros sem datas válidas
        data.dropna(subset=["data_hora_extracao", "updated_at"], inplace=True)

        # Calcula o tempo de execução (diferença entre updated_at e data_hora_extracao)
        data = calculate_execution_time_3(data)
    except Exception as e:
        # Loga e exibe erro caso haja falha no carregamento ou processamento
        logger.error(f"Erro ao buscar ou processar dados do Painel 3: {e}")
        st.error("Falha ao carregar os dados do Painel 3.")
    return data


# Função para carregar e processar dados do De/Para (relatorios x email_logs)
def load_email_delivery_report():
    data = pd.DataFrame()
    try:
        # Consulta o relatório de entrega de e-mails (de/para)
        data = get_email_delivery_report()
    except Exception as e:
        # Loga e exibe erro caso haja falha no carregamento
        logger.error(f"Erro ao buscar dados de De/Para de e-mails: {e}")
        st.error("Falha ao carregar os dados de De/Para de e-mails.")
    return data


# Carregar dados

# Carrega todos os dados necessários para os painéis
exec_data = load_execution_data()  # Painel 1
report_data_2 = load_reports_data_relatorios74()  # Painel 2
report_data = load_reports_data_relatorios()  # Painel 3
email_delivery_data = load_email_delivery_report()  # Relatório de e-mails

# Menu principal de navegação entre os painéis
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

            # Filtrar os dados apenas para o dia atual e criar cópia
            execucoes_hoje = exec_data[exec_data["date"] == hoje].copy()

            # Adicionar uma coluna com a hora
            execucoes_hoje["hour"] = execucoes_hoje["entry_datetime"].dt.hour

            # Contar as horas distintas em que ocorreram execuções
            execucoes_distintas_por_hora = execucoes_hoje["hour"].nunique()

            casos_ativos = exec_data["ativo"].sum()
            ultimo_end_time = exec_data["end_time"].max()

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Total de Execuções(dia)",
                          execucoes_distintas_por_hora)
            with col2:
                st.metric("📥 Backlog do Dia", casos_ativos)
            with col3:
                st.metric(
                    "📅 Última Data (D/M/A)",
                    ultimo_end_time.strftime("%d/%m/%y")
                    if ultimo_end_time else "N/A")
            with col4:
                st.metric(
                    "⏱️ Último Horário (H:M:S)",
                    ultimo_end_time.strftime("%H:%M:%S")
                    if ultimo_end_time else "N/A")
        else:
            st.warning("Nenhuma execução ativa ou recente encontrada.")

    elif submenu == "Gráficos":
        st.header("Gráficos do Painel 1")
        if not exec_data.empty:
            # Gráfico original: Execuções por Hora
            st.subheader("Execuções por Hora")
            exec_data["hour"] = exec_data["entry_datetime"].dt.floor("h")
            exec_data["formatted_hour"] = exec_data["hour"].apply(
                lambda x: x.strftime("%H:%M") if not pd.isnull(x) else "N/A")
            exec_data["date"] = exec_data["entry_datetime"].dt.date
            execucoes_por_hora = exec_data[
                exec_data["formatted_hour"] != "N/A"].groupby(
                    ["formatted_hour",
                     "date"]).size().reset_index(name="count")
            execucoes_por_hora_distintas = execucoes_por_hora.groupby(
                "formatted_hour")["date"].nunique().reset_index(
                    name="dias_distintos")
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

            # Gráfico original: Execuções por Dia
            st.subheader("Execuções por Dia")
            exec_data["formatted_date"] = exec_data["date"].apply(
                lambda x: x.strftime("%d/%m/%y")
                if not pd.isnull(x) else "N/A")
            exec_data["hour_only"] = exec_data["entry_datetime"].dt.floor("h")
            execucoes_por_dia_distintas = exec_data[
                exec_data["formatted_date"] != "N/A"].drop_duplicates(
                    subset=["formatted_date", "hour_only"])
            execucoes_por_dia = execucoes_por_dia_distintas.groupby(
                "formatted_date").size().reset_index(name="count")
            execucoes_por_dia["formatted_date_sort"] = pd.to_datetime(
                execucoes_por_dia["formatted_date"], format="%d/%m/%y")
            execucoes_por_dia = execucoes_por_dia.sort_values(
                "formatted_date_sort")
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

            # Filtrar os dados apenas para o dia atual e criar cópia
            execucoes_hoje = report_data_2[report_data_2["date"] == hoje].copy()

            # Adicionar uma coluna com a hora
            execucoes_hoje["hour"] = execucoes_hoje["data_hora_extracao"].dt.hour

            # Contar as horas distintas em que ocorreram execuções
            execucoes_distintas_por_hora = execucoes_hoje["hour"].nunique()

            mensagens_validas_hoje = report_data_2["valid_obs"].sum()

            # Calcular o backlog
            backlog = report_data_2["backlog"].max()

            ultimo_end_time_2 = report_data_2["updated_at"].max()

            # Primeira linha: Total de Execuções(dia) e WF Feitos
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Total de Execuções(dia)",
                          execucoes_distintas_por_hora)
            with col2:
                st.metric("✅ WF Feitos", mensagens_validas_hoje)
            with col3:
                st.metric("📥 Backlog do Dia", backlog)

            # Segunda linha: Backlog do Dia, Última Data, Último Horário
            col4, col5 = st.columns(2)

            with col4:
                st.metric(
                    "📅 Última Data (D/M/A)",
                    ultimo_end_time_2.strftime("%d/%m/%y")
                    if ultimo_end_time_2 else "N/A",
                )
            with col5:
                st.metric(
                    "⏱️ Último Horário (H:M:S)",
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
                "data_hora_extracao"].dt.floor("h")

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

            # Filtrar os dados apenas para o dia atual e criar cópia
            execucoes_hoje = report_data[report_data["date"] == hoje].copy()

            # Adicionar uma coluna com a hora
            execucoes_hoje["hour"] = execucoes_hoje["data_hora_extracao"].dt.hour

            # Contar as horas distintas em que ocorreram execuções
            execucoes_distintas_por_hora = execucoes_hoje["hour"].nunique()

            ultimo_end_time = report_data["updated_at"].max()

            # --- NOVO: Buscar total de e-mails encaminhados ---
            total_encaminhados = 0
            if not email_delivery_data.empty:
                total_encaminhados = email_delivery_data[
                    "total_encaminhados"].sum()

            total_nao_encaminhados = 0
            if not email_delivery_data.empty:
                total_nao_encaminhados = email_delivery_data[
                    "total_nao_encaminhados"].sum()

            # --- NOVO: Backlog do dia ---
            backlog_hoje = execucoes_hoje.shape[0]

            # --- NOVO: Tempo médio de tratativa (created_at -> updated_at) ---
            if not execucoes_hoje.empty:
                execucoes_hoje["tempo_tratativa"] = (
                    execucoes_hoje["updated_at"] - execucoes_hoje["created_at"]
                ).dt.total_seconds() / 60  # minutos
                tempo_medio_tratativa = execucoes_hoje["tempo_tratativa"].mean(
                )
            else:
                tempo_medio_tratativa = 0

            # Primeira linha de métricas
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Total de Execuções(dia)",
                          execucoes_distintas_por_hora)
            with col2:
                st.metric(
                    "📅 Última Data (D/M/A)",
                    ultimo_end_time.strftime("%d/%m/%y")
                    if ultimo_end_time else "N/A",
                )
            with col3:
                st.metric(
                    "⏱️ Último Horário (H:M:S)",
                    ultimo_end_time.strftime("%H:%M:%S")
                    if ultimo_end_time else "N/A",
                )
            with col4:
                st.metric("⏱️ Duração Média (min)",
                          f"{tempo_medio_tratativa:.1f}")

            # Segunda linha de métricas
            col5, col6, col7 = st.columns(3)
            with col5:
                st.metric("📥 Backlog do Dia", backlog_hoje)
            with col6:
                st.metric("📤 E-mails Encaminhados", int(total_encaminhados))
            with col7:
                st.metric("📤 E-mails Não Encaminhados",
                          int(total_nao_encaminhados))
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
                "data_hora_extracao"].dt.floor("h")

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
