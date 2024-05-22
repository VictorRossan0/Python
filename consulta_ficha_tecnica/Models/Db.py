from dotenv import load_dotenv
import os
import mysql.connector
from datetime import datetime

class Db:
    def run_query_and_insert(self):
        print("Carregando variáveis de ambiente...")
        load_dotenv()

        print("Configurando conexão com o banco de dados...")
        db_host = os.getenv('HOST_NAME')
        db_user = os.getenv('DBUSERNAME')
        db_password = os.getenv('PASSWORD')
        db_name = os.getenv('DBNAME')
        db_port = os.getenv('PORT')

        conn = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database=db_name, port=db_port)
        cursor = conn.cursor(buffered=True)  # Usando cursor bufferizado para leitura eficiente

        # Consulta para selecionar as colunas desejadas da tabela_origem com filtro
        query = "SELECT cir, pendencia, regional, cm, tecnologia, servico, ativ_agend, designacao FROM jarvas_agendamento_13 WHERE pendencia = 'PA0201 - Agendar Atividade (6.6)' AND no_agendamento = 1 AND ativo = 1 AND list = 13 AND aging_status_disponivel = '0 dia'"
        cursor.execute(query)
        
        print("Inserindo dados na tabela_destino...")
        rows = cursor.fetchall()
        data = []
        for row in rows:
            cir_value = row[0]
            ins_query = "INSERT INTO consulta_cir (cir, pendencia, regional, cm, tecnologia, servico, atividade_remota, designacao, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (cir_value, row[1], row[2], row[3], row[4], row[5], row[6], row[7], datetime.now())
            data.append(cir_value)
            
            # Verifica se o cir já existe na tabela de destino
            check_query = "SELECT COUNT(*) FROM consulta_cir WHERE cir = %s"
            cursor.execute(check_query, (cir_value,))
            result = cursor.fetchone()
            
            if result[0] == 0:
                cursor.execute(ins_query, values)
            else:
                print(f"O cir {cir_value} já existe na tabela de destino. Ignorando inserção.")

        print("Commit da transação e fechando a conexão...")
        conn.commit()
        cursor.close()
        conn.close()
        
        return data
    
    def update(self, table_name, column_name, value, condition):
        print(f"Atualizando dados na tabela {table_name}...")
        load_dotenv()

        db_host = os.getenv('HOST_NAME')
        db_user = os.getenv('DBUSERNAME')
        db_password = os.getenv('PASSWORD')
        db_name = os.getenv('DBNAME')
        db_port = os.getenv('PORT')

        conn = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database=db_name, port=db_port)
        cursor = conn.cursor()

        try:
            ins_query = f"UPDATE {table_name} SET {column_name} = %s, updated_at = %s, clicked = 1 WHERE {condition}"
            params = (value, datetime.now())
            cursor.execute(ins_query, params)
            conn.commit()
            print("Dados atualizados com sucesso.")
        except mysql.connector.Error as error:
            print(f"Erro ao atualizar dados: {error}")
        finally:
            cursor.close()
            conn.close()

    def get_filtered_cirs(self):
        print("Carregando variáveis de ambiente...")
        load_dotenv()

        print("Configurando conexão com o banco de dados...")
        db_host = os.getenv('HOST_NAME')
        db_user = os.getenv('DBUSERNAME')
        db_password = os.getenv('PASSWORD')
        db_name = os.getenv('DBNAME')
        db_port = os.getenv('PORT')

        conn = mysql.connector.connect(user=db_user, password=db_password, host=db_host, database=db_name, port=db_port)
        cursor = conn.cursor()

        # Consulta para selecionar os CIRs com filtros de updated_at e clicked
        query = "SELECT cir FROM consulta_cir WHERE updated_at IS NULL AND clicked IS NULL"
        cursor.execute(query)

        rows = cursor.fetchall()
        cirs = []
        for row in rows:
            cir_value = row[0]
            cirs.append(cir_value)

        print("Fechando a conexão...")
        conn.commit()
        cursor.close()
        conn.close()

        return cirs
    
    def main(self):
        """Função principal para execução do login."""
        print("Executando método principal...")
        self.run_query_and_insert()  # Chama o método de consulta e inserção

# Executa a função principal
db = Db()
db.main()
