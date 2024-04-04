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
        query = "SELECT cir, pendencia, cm, tecnologia FROM jarvas_agendamento_13 WHERE pendencia = 'PA0201 - Agendar Atividade (6.6)' AND no_agendamento = 1 AND ativo = 1 AND list = 13 AND aging_status_disponivel = '0 dia'"
        # Verificar se iremos filtrar algum campo à mais além do aging_status_disponivel, pensando em filtrar também aging_macro_processo_sem_inter
        # Possibilidade de inserir as informações de ativ_agend, pois consta como Atividade Remota dentro da ficha técnica, perguntar ao Will e a Thais
        cursor.execute(query)
        
        print("Inserindo dados na tabela_destino...")
        rows = cursor.fetchall()
        for row in rows:
            cir_value = row[0]
            ins_query = "INSERT INTO consulta_cir (cir, pendencia, cm, tecnologia, created_at) VALUES (%s, %s, %s, %s, %s)"
            values = (cir_value, row[1], row[2], row[3], datetime.now())
            
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
    
    def main(self):
        """Função principal para execução do login."""
        print("Executando método principal...")
        self.run_query_and_insert()  # Chama o método de consulta e inserção

# Executa a função principal
db = Db()
db.main()
