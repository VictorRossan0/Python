from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

class Window:
            
    def __init__(self):
        firefox_options = Options()
        firefox_options.add_argument('--log-level=3')
        self.driver = webdriver.Firefox(executable_path=r"C:/Documents/geckodriver.exe", options=firefox_options)
        

    def redirect(self, url):
        self.driver.get(url)