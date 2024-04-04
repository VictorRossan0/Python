import os
import time
import sqlalchemy
from Models.Db import Db
from Models.Login import Login
from Models.Navigate import Navigate
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from selenium.webdriver.common.by import By
from dotenv.main import load_dotenv
from datetime import datetime

Base = sqlalchemy.orm.declarative_base()

class Agendamento(Base):
    __tablename__ = 'consulta_cir'
    id = Column(Integer, primary_key=True)
    cir = Column(String)
    pendencia = Column(String)
    cm = Column(String)
    tecnologia = Column(String)
    atividade_remota = Column(String)
    pcl = Column(String)
    solid = Column(String)
    oe = Column(String)
    ots = Column(String)
    servico = Column(String)
    atividade = Column(String)
    velocidade = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

def process_data(data_list, session):
    insert_count = 0
    update_count = 0
    delete_count = 0

    for row in data_list:
        try:
            existing_agendamento = session.query(Agendamento).filter_by(cir=row.get("cir"), list=os.getenv("LIST")).one()
            if any(getattr(existing_agendamento, key) != value for key, value in row.items()):
                for key, value in row.items():
                    setattr(existing_agendamento, key, value)
                existing_agendamento.no_agendamento = True
                existing_agendamento.ativo = True
                existing_agendamento.deleted_at = None
                existing_agendamento.updated_at = datetime.now()
                update_count += 1
                print("Atualizados:", row.get("cir"))
        except NoResultFound:
            new_agendamento = Agendamento(**row, list=os.getenv("LIST"))
            session.add(new_agendamento)
            insert_count += 1
            print("Inseridos:", row.get("cir"))

    # Soft delete logic
    soft_delete_list = session.query(Agendamento).filter_by(list=os.getenv("LIST")).filter(Agendamento.cir.notin_([row.get("cir") for row in data_list])).all()
    for deleted_agendamento in soft_delete_list:
        if deleted_agendamento.no_agendamento:
            deleted_agendamento.no_agendamento = False
            deleted_agendamento.ativo = False
            deleted_agendamento.updated_at = datetime.now()
            deleted_agendamento.deleted_at = datetime.now()
            delete_count += 1
            print("Deletados:", deleted_agendamento.cir)

    session.commit()

    print("Total Inserido na tabela:", insert_count)
    print("Total Atualizado na tabela:", update_count)
    print("Total Deletado na tabela:", delete_count)

# def scrap(login):
#     print("START SCRAP")
#     columns = {
#         4: "atividade_remota", 
#         5: "pcl",
#         6: "solid", 
#         7: "oe", 
#         8: "ots",
#         9: "servico",
#         10: "atividade",
#         11: "velocidade",
#     }
#
#     terminals = []
#     tbody = login.window.driver.find_element(By.TAG_NAME, "tbody")
#     for row in tbody.find_elements(By.XPATH, ".//tr"):
#         qtd = 1
#         list_to_insert = {}
#         cir_value = None
#         for td in row.find_elements(By.XPATH, ".//td"):
#             if qtd in list(columns.keys()):
#                 value = td.text.strip()
#                 if columns[qtd] == "cir":
#                     cir_value = value
#                 else:
#                     list_to_insert[columns[qtd]] = value
#             qtd += 1
#         if cir_value is not None:
#             list_to_insert["cir"] = cir_value
#         terminals.append(list_to_insert)

#     engine = create_engine('mysql+pymysql://root:@localhost/jarvas')
#     Base.metadata.create_all(engine)
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     process_data(terminals, session)
#     session.close()

#     login.window.driver.quit()
#     print("END SCRAP")

def main():
    start_time = time.time()
    load_dotenv()
    db_instance = Db()
    db_instance.run_query_and_insert()
    login_instance = Login()
    navigate_instance = Navigate(login_instance.window, os.getenv("LIST"))
    navigate_instance
    # scrap(login_instance)
    end_time = time.time()
    execution_time = end_time - start_time
    execution_time_minutes = execution_time / 60
    print(f"Tempo de execução: {execution_time_minutes:.2f} minutos")

if __name__ == "__main__":
    main()

