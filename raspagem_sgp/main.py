from Models import Login
from Models import Navigate
from datetime import datetime
# from Models import Email
from selenium.webdriver.common.by import By
from dotenv.main import load_dotenv
import mysql.connector
import os
import importlib
import time
import pandas as pd

def validate(key, row):
    if key in row.keys():
        return row[key]
    else:
        return ""

# CONEXÃO
def conexao(sql, type):
    load_dotenv()
    mydb = mysql.connector.connect(
        port=os.environ['PORT'],
        host=os.environ['HOST_NAME'],
        user=os.environ['DBUSERNAME'],
        password=os.environ['PASSWORD'],
        database=os.environ['DBNAME']
    )

    cursor = mydb.cursor(buffered=True)
    myresult = None  # Inicializa a variável com um valor padrão
    try:
        cursor.execute(sql)
        mydb.commit()
        if type == "SELECT":
            myresult = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erro MySQL: {err}")
        raise
    finally:
        cursor.close()
        return myresult

# SELECT
def select():
    query = 'SELECT cir from jarvas.jarvas_agendamento_13 WHERE list = '+os.environ['LIST']
    return conexao(query, "SELECT")

# UPDATE
def update(list):
    size = len(list)
    print("DESATIVANDO E ATUALIZANDO NO AGENDAMENTO...")
    qtd_desativando = 0
    if size > 0:
        qtd_atualizando = 0
        query_insert = 'INSERT INTO jarvas.jarvas_agendamento_13 (cir,oi,cm,cliente,macro,pendencia,status,tarefa_inter,tarefa_ant,analista,designacao,terminal,servico,tipo_alt,tipo_serv,projeto,aging_macro_processo_sem_inter,aging_tarefa,aging_status_disponivel,inter,log,cli_black,cli_difer,ativ_agend,obs_agend,data_pre_agend,data_solus_agend,data_agend,created_at,no_agendamento,ativo,list) VALUES '
        for row in list:
            query = 'SELECT created_at FROM jarvas.jarvas_agendamento_13 WHERE cir = "'+validate("cir", row)+'" AND pendencia <> "'+validate("pendencia", row)+'" AND no_agendamento = 1 AND ativo = 1 AND list = '+os.environ['LIST']
            data = conexao(query+";", "SELECT")
            create_datetime = None
            if len(data) > 0:
                for eachone in data:
                    create_datetime_str = eachone[0]
                    if create_datetime_str:
                        create_datetime = datetime.strptime(create_datetime_str, '%Y-%m-%d %H:%M:%S.%f')
                qtd_desativando += 1
                query = 'UPDATE jarvas.jarvas_agendamento_13 SET no_agendamento = 1, ativo = 0, updated_at = NOW() WHERE cir = "'+validate("cir", row)+'"'
                conexao(query+";", "UPDATE")
                if create_datetime is not None:
                    query_insert += '("'+validate('cir', row)+'","'+validate('oi', row)+'","'+validate('cm', row)+'","'+validate('cliente', row)+'","'+validate('macro', row)+'","'+validate('bloco', row)+'","'+validate('gross', row)+'","'+validate('pendencia', row)+'","'+validate('status', row)+'","'+validate('tarefa_inter', row)+'","'+validate('tarefa_ant', row)+'","'+validate('analista', row)+'","'+validate('designacao', row)+'","'+validate('terminal', row)+'","'+validate('provedor', row)+'","'+validate('servico', row)+'","'+validate('ticket_cpe', row)+'","'+validate('os_agen', row)+'","'+validate('tipo_alt', row)+'","'+validate('tipo_serv', row)+'","'+validate('projeto', row)+'","'+validate('aging_macro_processo_sem_inter', row)+'","'+validate('aging_tarefa', row)+'","'+validate('aging_status_disponivel', row)+'","'+validate('inter', row)+'","'+validate('log', row)+'","'+validate('cli_black', row)+'","'+validate('cli_difer', row)+'","'+validate('ativ_agend', row)+'","'+validate('obs_agend', row)+'","'+validate('data_pre_agend', row)+'","'+validate('data_solus_agend', row)+'","'+validate('data_agend', row)+'","'+validate('disponibilizado', row)+'","'+create_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]+'",1,1,'+os.environ['LIST']+'),'
                qtd_atualizando += 1
            
        # Verifique se há algo para inserir antes de executar a consulta
        if qtd_atualizando > 0:
            conexao(query_insert.rstrip(',')+";", "INSERT")
        
    print("FIM ATUALIZAÇÃO, ATUALIZADOS:")
    print(qtd_atualizando)
    print("FIM DESATIVAÇÃO, DESATIVADOS:")
    print(qtd_desativando)

# DELETE
def delete(list):
    size = len(list)
    print("SAIRAM DO AGENDAMENTO...")
    print(size)
    query = 'UPDATE jarvas.jarvas_agendamento_13 SET no_agendamento = "0", ativo = "0", updated_at = NOW() WHERE cir IN ('
    qtd = 1
    for r in list:
      if(qtd == size):
          query += '"'+r+'")'   
      else:
          query += '"'+r+'",'
      qtd += 1
    conexao(query+";", "RETIRANDO DO AGENDAMENTO")
    print("FIM")

# INSERT
def insert(list):
    size = len(list)
    print("ENTRARAM NO AGENDAMENTO...")
    print(size)
    query = 'INSERT INTO jarvas.jarvas_agendamento_13 (cir,oi,cm,cliente,macro,bloco,gross,pendencia,status,tarefa_inter,tarefa_ant,analista,designacao,terminal,provedor,servico,ticket_cpe,os_agen,tipo_alt,tipo_serv,projeto,aging_macro_processo_sem_inter,aging_tarefa,aging_status_disponivel,inter,log,cli_black,cli_difer,ativ_agend,obs_agend,data_pre_agend,data_solus_agend,data_agend,disponibilizado,created_at,no_agendamento,ativo,list) VALUES '
    result = ""
    if size > 0:
        for row in list:
            create_datetime = datetime.now()
            query += '("'+validate('cir', row)+'","'+validate('oi', row)+'","'+validate('cm', row)+'","'+validate('cliente', row)+'","'+validate('macro', row)+'","'+validate('bloco', row)+'","'+validate('gross', row)+'","'+validate('pendencia', row)+'","'+validate('status', row)+'","'+validate('tarefa_inter', row)+'","'+validate('tarefa_ant', row)+'","'+validate('analista', row)+'","'+validate('designacao', row)+'","'+validate('terminal', row)+'","'+validate('provedor', row)+'","'+validate('servico', row)+'","'+validate('ticket_cpe', row)+'","'+validate('os_agen', row)+'","'+validate('tipo_alt', row)+'","'+validate('tipo_serv', row)+'","'+validate('projeto', row)+'","'+validate('aging_macro_processo_sem_inter', row)+'","'+validate('aging_tarefa', row)+'","'+validate('aging_status_disponivel', row)+'","'+validate('inter', row)+'","'+validate('log', row)+'","'+validate('cli_black', row)+'","'+validate('cli_difer', row)+'","'+validate('ativ_agend', row)+'","'+validate('obs_agend', row)+'","'+validate('data_pre_agend', row)+'","'+validate('data_solus_agend', row)+'","'+validate('data_agend', row)+'","'+validate('disponibilizado', row)+'","'+str(create_datetime)+'",1,1,'+os.environ['LIST']+'),'
        try:
            result = conexao(query.rstrip(',')+";", "INSERT")
            print("END INSERT")
        except mysql.connector.Error as err:
            print(f"Erro MySQL: {err}")
            raise
    return result

# SCRAP
def scrap(login):
    print("START SCRAP")
    # COLUMNS
    columns = {
        4: "cir", 
        5: "oi",
        6: "cm", 
        7: "cliente", 
        8: "macro",
        9: "bloco",
        10: "gross",
        11: "pendencia", 
        12: "status", 
        13: "tarefa_inter", 
        14: "tarefa_ant", 
        15: "analista", 
        16: "designacao", 
        17: "terminal", 
        18: "provedor",
        19: "servico", 
        20: "ticket_cpe",
        21: "os_agen",
        22: "tipo_alt", 
        23: "tipo_serv", 
        24: "projeto", 
        25: "aging_macro_processo_sem_inter", 
        26: "aging_tarefa", 
        27: "aging_status_disponivel", 
        28: "inter", 
        29: "log", 
        30: "cli_black", 
        31: "cli_difer", 
        32: "ativ_agend", 
        33: "obs_agend", 
        34: "data_pre_agend",
        35: "data_solus_agend",
        36: "data_agend",
        37: "disponibilizado"
    }
    # GETTING FROM TABLE
    terminals = []
    tbody = login.window.driver.find_element(By.TAG_NAME, "tbody")
    for row in tbody.find_elements(By.XPATH, ".//tr"):
        qtd = 1
        list_to_insert = {}
        for td in row.find_elements(By.XPATH, ".//td"):
            if qtd in list(columns.keys()):
                list_to_insert[columns[qtd]] = td.text
            qtd += 1
        terminals.append(list_to_insert)
    print("END SCRAP")
    # Criar DataFrame do Pandas para os dados raspados
    df_scraped = pd.DataFrame(terminals)
    
    # Salvar DataFrame em arquivo Excel
    caminho_excel_scraped = 'dados_raspados.xlsx'
    df_scraped.to_excel(caminho_excel_scraped, index=False)
    print(f"\nDados raspados salvos em '{caminho_excel_scraped}'")

    result = select()
    print("REGISTROS NO BANCO")
    if not len(result) == 0:
        # IF NOT EMPTY DATABASE
        db_outlist = [row[0] for row in result]
        insert_list = []
        update_list = []
        delete_list = []
        for row in terminals:
            if not row['cir'] in db_outlist:
                insert_list.append(row)
            else: 
                update_list.append(row)
        for row_db in db_outlist:
            if not any(row_db == d['cir'] for d in terminals):
                delete_list.append(row_db)
        if(len(delete_list) > 0):
            delete(delete_list)
        if(len(insert_list) > 0):
            insert(insert_list)
        if(len(update_list) > 0):
            update(update_list)
    else:
        # IF EMPTY DATABASE
        insert(terminals)
    print("TERMINOU")

# Example usage
try:
        importlib.invalidate_caches()
        start_time = time.time()

        login = Login()
        navigate = Navigate(login.window, os.environ['LIST'])
        scrap(login)

        end_time = time.time()
        elapsed_time_seconds = end_time - start_time
        elapsed_time_minutes = elapsed_time_seconds / 60
        print(f"Total execution time: {elapsed_time_minutes:.2f} minutes")

        del navigate
        login.window.driver.quit()
except mysql.connector.Error as err:
        print(f"Error MySQL ({err.errno}): {err.msg}")
        raise