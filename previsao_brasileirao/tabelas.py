import pandas as pd
import requests
from scipy.stats import poisson
from bs4 import BeautifulSoup

# Fazendo a requisição para a página da Wikipedia
requisicao = requests.get("https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_2023_-_S%C3%A9rie_A")
if requisicao.status_code == 200:
    soup = BeautifulSoup(requisicao.text, 'html.parser')

# Lendo as tabelas presentes na página
tabelas = pd.read_html(requisicao.text)

# Selecionando as tabelas de classificação e de jogos
tabela_classificacao = tabelas[6]
tabela_jogos = tabelas[7]

# Exibindo as tabelas
print("\nTabela de Classificação")
print(tabela_classificacao)
print("\nTabela de Jogos")
print(tabela_jogos)

# Criando listas de nomes e apelidos dos times
nomes_times = list(tabela_jogos["Casa \ Fora"])
apelidos = list(tabela_jogos.columns)
apelidos.pop(0)
print("\nTabela de Times")
print(nomes_times)
print("\nTabela de Sigla")
print(apelidos)

# Criando um dicionário de correspondência entre apelidos e nomes dos times
de_para_times = dict(zip(apelidos, nomes_times))

print("\nDicionário dos times")
print(de_para_times)

# Ajustando a tabela de jogos
tabela_jogos_ajustada = tabela_jogos.set_index("Casa \ Fora")
tabela_jogos_ajustada = tabela_jogos_ajustada.unstack().reset_index()
tabela_jogos_ajustada = tabela_jogos_ajustada.rename(columns={"level_0": "fora", "Casa \ Fora": "casa", 0: "resultado"})

# Definindo uma função para ajustar o apelido do time
def ajustar_apelido_time(linha):
    apelido = linha["fora"]
    nome = de_para_times[apelido]
    return nome

# Aplicando a função à coluna "fora" da tabela de jogos ajustada
tabela_jogos_ajustada["fora"] = tabela_jogos_ajustada.apply(ajustar_apelido_time, axis=1)

# Filtrando os jogos onde os times são diferentes
tabela_jogos_ajustada = tabela_jogos_ajustada[tabela_jogos_ajustada["fora"] != tabela_jogos_ajustada["casa"]]

print("\nTabela de Jogos Ajustados")
print(tabela_jogos_ajustada)

# Preenchendo valores nulos na coluna "resultado" e filtrando jogos realizados e faltantes
tabela_jogos_ajustada["resultado"] = tabela_jogos_ajustada["resultado"].fillna("a jogar")
tabela_jogos_realizados = tabela_jogos_ajustada[tabela_jogos_ajustada["resultado"].str.contains("–")]

print("\nTabela de Jogos Realizados")
print(tabela_jogos_realizados)

tabela_jogos_faltantes = tabela_jogos_ajustada[~tabela_jogos_ajustada["resultado"].str.contains("–")]
tabela_jogos_faltantes = tabela_jogos_faltantes.drop(columns=["resultado"])

print("\nTabela de Jogos Faltantes")
print(tabela_jogos_faltantes)

# Separando gols marcados e sofridos nos jogos realizados
tabela_jogos_realizados[["gols_casa", "gols_fora"]] = tabela_jogos_realizados["resultado"].str.split("–", expand=True)
tabela_jogos_realizados = tabela_jogos_realizados.drop(columns=["resultado"])
tabela_jogos_realizados["gols_casa"] = tabela_jogos_realizados["gols_casa"].astype(int)
tabela_jogos_realizados["gols_fora"] = tabela_jogos_realizados["gols_fora"].astype(int)

print("\nTabela de Jogos Realizados")
print(tabela_jogos_realizados)

# Calculando médias de gols feitos e sofridos em casa e fora
media_gols_casa = tabela_jogos_realizados.groupby("casa").mean(numeric_only=True)
media_gols_casa = media_gols_casa.rename(columns={"gols_casa": "gols_feitos_casa", "gols_fora": "gols_sofridos_casa"})

print("\nMédia de gols casa")
print(media_gols_casa)

media_gols_fora = tabela_jogos_realizados.groupby("fora").mean(numeric_only=True)
media_gols_fora = media_gols_fora.rename(columns={"gols_casa": "gols_sofridos_fora", "gols_fora": "gols_feitos_fora"})

print("\nMédia de gols fora")
print(media_gols_fora)

# Criando tabela de estatísticas combinando médias de gols feitos e sofridos em casa e fora
tabela_estatisticas = media_gols_casa.merge(media_gols_fora, left_index=True, right_index=True)
tabela_estatisticas = tabela_estatisticas.reset_index()
tabela_estatisticas = tabela_estatisticas.rename(columns={"casa": "time"})

print("\nTabela de Estatísticas")
print(tabela_estatisticas)

# Função para calcular pontuação esperada usando modelo de Poisson
def calcular_pontuacao_esperada(linha):
    time_casa = linha["casa"]
    time_fora = linha["fora"]

    lambda_casa = (
        tabela_estatisticas.loc[tabela_estatisticas["time"] == time_casa, "gols_feitos_casa"].iloc[0]
        * tabela_estatisticas.loc[tabela_estatisticas["time"] == time_fora, "gols_sofridos_fora"].iloc[0]
    )

    lambda_fora = (
        tabela_estatisticas.loc[tabela_estatisticas["time"] == time_fora, "gols_feitos_fora"].iloc[0]
        * tabela_estatisticas.loc[tabela_estatisticas["time"] == time_casa, "gols_sofridos_casa"].iloc[0]
    )

    pv_casa, p_empate, pv_fora = 0, 0, 0

    for gols_casa in range(8):
        for gols_fora in range(8):
            probabilidade_resultado = poisson.pmf(gols_casa, lambda_casa) * poisson.pmf(gols_fora, lambda_fora)
            if gols_casa == gols_fora:
                p_empate += probabilidade_resultado
            elif gols_casa > gols_fora:
                pv_casa += probabilidade_resultado
            elif gols_casa < gols_fora:
                pv_fora += probabilidade_resultado

    ve_casa = pv_casa * 3 + p_empate
    ve_fora = pv_fora * 3 + p_empate
    linha["pontos_casa"] = ve_casa
    linha["pontos_fora"] = ve_fora
    return linha

# Aplicando a função aos jogos faltantes
tabela_jogos_faltantes = tabela_jogos_faltantes.apply(calcular_pontuacao_esperada, axis=1)

print("\nTabela Jogos Faltantes")
print(tabela_jogos_faltantes)

# Função para ajustar o nome do time
def ajustar_nome_time(linha):
    equipevde = linha["Equipevde"].lower()

    for nome in nomes_times:
        if nome.lower() in equipevde:
            return nome

# Aplicando a função à coluna "time" da tabela de classificação
tabela_classificacao["time"] = tabela_classificacao.apply(ajustar_nome_time, axis=1)
tabela_classificacao_atualizada = tabela_classificacao[["time", "Pts"]]
tabela_classificacao_atualizada["Pts"] = tabela_classificacao_atualizada["Pts"].astype(int)

print("\nTabela Classificação Atualizada")
print(tabela_classificacao_atualizada)

# Agrupando e somando pontuações para casa e fora
tabela_pontuacao_casa = tabela_jogos_faltantes.groupby("casa").sum(numeric_only=True)[["pontos_casa"]]
tabela_pontuacao_fora = tabela_jogos_faltantes.groupby("fora").sum(numeric_only=True)[["pontos_fora"]]

print("\nTabela Pontuação Casa")
print(tabela_pontuacao_casa)

print("\nTabela Pontuação Fora")
print(tabela_pontuacao_fora)

# Atualizando a pontuação prevista na tabela de classificação
def atualizar_pontuacao_previsao(linha):
    time = linha["time"]
    pontuacao = int(linha["Pts"]) + float(tabela_pontuacao_casa.loc[time, "pontos_casa"]) + float(
        tabela_pontuacao_fora.loc[time, "pontos_fora"]
    )
    # Usando .loc[] para atribuir valores diretamente
    tabela_classificacao_atualizada.loc[tabela_classificacao_atualizada["time"] == time, "Pts"] = pontuacao
    return linha

# Aplicando a função aos dados da tabela de classificação
tabela_classificacao_atualizada = tabela_classificacao.apply(atualizar_pontuacao_previsao, axis=1)
tabela_classificacao_atualizada["Pts"] = tabela_classificacao_atualizada["Pts"].astype(int)

print("\nTabela Classificada Atualizada")
print(tabela_classificacao_atualizada)

# Função para salvar os resultados em um arquivo
def salvar_resultados(filename, tabela_classificacao_atualizada):
    # Usando 'utf-8' como codec para evitar problemas com caracteres Unicode
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(tabela_classificacao_atualizada.to_string())

# Chamando a função para salvar os resultados
salvar_resultados('resultados.txt', tabela_classificacao_atualizada)