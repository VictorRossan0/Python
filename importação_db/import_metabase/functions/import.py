import pandas as pd
import MySQLdb

# Conexão com o banco de dados MySQL
conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="financbpo")
cursor = conn.cursor()
print("Conexão feito com sucesso")

# Ler o arquivo CSV
df = pd.read_csv('dados_convertidos.csv', encoding='utf-8')
print("Leitura feita com sucesso")

# Selecionar as colunas desejadas
selected_columns = ['Bloco', 'IdOper', 'CodStatusProjecao', 'HC', 'CustoTotal', 'ReceitaBruta', 'AlocRecursosCaixa', 'AlocRecursosPetr?olis', 'AlocRecursosAgendamento', 'Devengado', 'Custo Recursos', 'Desonera?o', 'Custo Outros', 'Custo subcontratados', 'Compet?cia', 'HEs', 'hes_pagas', 'EBITDA Devegado Mensal', 'EBITDA Devegado Consolidado', 'EBITDA Real Mensal', 'EBITDA Real Consolidado', 'BH Realizado', 'BH +', 'BH -']
print("Colunas selecionadas com sucesso")

# Iterar sobre as linhas do DataFrame, ignorando a primeira linha
for index, row in df.iloc[1:].iterrows():
    values = [row[col] for col in selected_columns]
    
    # Substituir valores nan por None
    values = [None if pd.isna(value) else value for value in values]

    # Inserir os valores no banco de dados
    cursor.execute("REPLACE INTO basefin (visao, id_operacao, projecao, hc, custo_total, receita_bruta, custo_rec_caixa, custo_rec_petropolis, custo_rec_agenda, devengado, custo_rh, custo_desoner, custo_outros, custo_subcontra, competencia, hes_valor, hes_qtda, ebtida_dev_mensal, ebtida_dev_conso, ebtida_real_mensal, ebtida_real_conso, bh_realizado, bh_mais, bh_menos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", values)

print("Iteração das linhas realizadas com sucesso")

# Commit para salvar as alterações no banco de dados
conn.commit()
print("Commit feito com sucesso")

# Fechar a conexão
conn.close()
print("Conexão fechada com sucesso")