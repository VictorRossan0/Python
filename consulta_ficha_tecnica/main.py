import os
import time
import pyautogui
import sqlalchemy
from Models.Db import Db
from Models.Login import Login
from Models.Navigate import Navigate
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from selenium.webdriver.common.by import By
from dotenv.main import load_dotenv
import logging

Base = sqlalchemy.orm.declarative_base()

# Configuração básica do logging
logging.basicConfig(filename='main.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    pyautogui.hotkey('alt', 'f4')

if __name__ == "__main__":
    main()
