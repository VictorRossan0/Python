from Models import Window
from dotenv.main import load_dotenv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import time

class Login:

    def __init__(self):

        #ENV
        load_dotenv()
        self.login_page = os.environ['SGP_LOGIN_PAGE']
        self.username = os.environ['SGP_USERNAME']
        self.password = os.environ['SGP_PASSWORD']
        
        # Open window and Redirect
        self.window = Window()
        self.window.redirect(self.login_page)
        self.do()

    def do(self):
        # Getting inputs to do login
        input_username = self.window.driver.find_element(By.XPATH, "//input[@data-vv-as='Usuário']")
        input_password = self.window.driver.find_element(By.XPATH, "//input[@data-vv-as='Senha']")

        #User
        input_username.click()
        input_username.clear()
        input_username.send_keys(self.username)
        
        #Password
        input_password.clear()
        input_password.send_keys(self.password)
        input_password.send_keys(Keys.RETURN)

        time.sleep(5)

    def undo(self):
       print("fechou")