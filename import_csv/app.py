import MySQLdb
import pandas as pd
import numpy as np
import os
from flask import Flask, render_template, request, redirect, flash, send_file, session

app = Flask(__name__)
app.secret_key = 'f4ba927418799709b1e16a2b3f965b69e4bc90025be660bb271a49291bf2d1a5'

UPLOAD_DIRECTORY = 'upload'  # Diretório de upload

# Rota padrão para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para a conversão de CSV para Excel
@app.route('/convert_csv_to_excel', methods=['POST'])
def convert_csv_to_excel():
    if 'csv_file' not in request.files:
        flash('Nenhum arquivo CSV foi enviado.', 'error')
        return redirect('/')
    
    csv_file = request.files['csv_file']
    
    if csv_file.filename == '':
        flash('Nenhum arquivo selecionado.', 'error')
        return redirect('/')
    
    try:
        # Ler o arquivo CSV
        df = pd.read_csv(csv_file, sep=';', decimal=',')
        
        # Converter o arquivo CSV para Excel
        excel_file_path = os.path.join(UPLOAD_DIRECTORY, 'converted_file.xlsx')
        df.to_excel(excel_file_path, index=False)
        
        flash('Arquivo CSV convertido para Excel com sucesso.', 'success')
        
        # Enviar o arquivo para download
        return send_file(excel_file_path, as_attachment=True)
    except:
        flash('Erro ao converter o arquivo CSV para Excel.', 'error')
        return redirect('/')

# Rota para processar o arquivo Excel
@app.route('/process_excel', methods=['POST'])
def process_excel():
    if 'excel_file' not in request.files:
        flash('Nenhum arquivo Excel foi enviado.', 'error')
        return redirect('/')
    
    excel_file = request.files['excel_file']
    
    if excel_file.filename == '':
        flash('Nenhum arquivo selecionado.', 'error')
        return redirect('/')
    
    try:
        # Ler o arquivo Excel em um DataFrame
        df = pd.read_excel(excel_file)
        
        # Remover o símbolo de porcentagem das colunas
        df['EBITDA Real Mensal'] = df['EBITDA Real Mensal'].str.replace('%', '')
        df['EBITDA Real Consolidado'] = df['EBITDA Real Consolidado'].str.replace('%', '')
        
        # Substituir vírgulas por pontos nas colunas
        df['EBITDA Real Mensal'] = df['EBITDA Real Mensal'].str.replace(',', '.')
        df['EBITDA Real Consolidado'] = df['EBITDA Real Consolidado'].str.replace(',', '.')
        
        # Converter as colunas para o tipo de dado correto
        df['EBITDA Real Mensal'] = df['EBITDA Real Mensal'].astype(np.float64)
        df['EBITDA Real Consolidado'] = df['EBITDA Real Consolidado'].astype(np.float64)
        
        # Salvar o DataFrame modificado em um novo arquivo Excel
        excel_file_path = os.path.join(UPLOAD_DIRECTORY, 'colunas_convertidas.xlsx')
        df.to_excel(excel_file_path, index=False)
        
        flash('Colunas convertidas e salvas em um novo arquivo Excel.', 'success')
        
        # Salvar o DataFrame em um arquivo CSV
        csv_file_path = os.path.join(UPLOAD_DIRECTORY, 'dados_convertidos.csv')
        df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')
        
        flash('DataFrame salvo em um arquivo CSV.', 'success')
        
        # Enviar o arquivo CSV para download
        return send_file(csv_file_path, as_attachment=True)
    except:
        flash('Erro ao processar o arquivo Excel.', 'error')
        return redirect('/')

# Rota para importar os dados para o MySQL
@app.route('/import_data', methods=['POST'])
def import_data():
    # Conexão com o banco de dados MySQL
    conn = MySQLdb.connect(host="10.230.43.179", user="victor", passwd="victor", db="financbpo")
    cursor = conn.cursor()
    print("Conexão feita com sucesso")

    # Ler o arquivo CSV
    csv_file = request.files['csv_file']
    df = pd.read_csv(csv_file, encoding='utf-8')
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

    print("Iteração das linhas realizada com sucesso")

    # Commit para salvar as alterações no banco de dados
    conn.commit()
    print("Commit feito com sucesso")

    # Fechar a conexão
    conn.close()
    print("Conexão fechada com sucesso")

    session['message'] = 'Dados importados com sucesso!'
    return redirect('/')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    app.run(host='0.0.0.0', debug=True, port=5001)