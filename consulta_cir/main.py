import os
import time
import sqlalchemy
from Models.Db import Db
from Models.Login import Login
from Models.Navigate import Navigate
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
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

def main():
    start_time = time.time()
    load_dotenv()
    db_instance = Db()
    db_instance.run_query_and_insert()
    login_instance = Login()
    navigate_instance = Navigate(login_instance.window, os.getenv("LIST"))
    navigate_instance
    end_time = time.time()
    execution_time = end_time - start_time
    execution_time_minutes = execution_time / 60
    print(f"Tempo de execução: {execution_time_minutes:.2f} minutos")

if __name__ == "__main__":
    main()

