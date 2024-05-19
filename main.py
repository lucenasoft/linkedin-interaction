import os
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

email = os.getenv('LINKEDIN_EMAIL')
password = os.getenv('LINKEDIN_PASSWORD')

class LinkedInInteraction:
    def __init__(self):
        self.driver = self.setup_driver()

    def setup_driver(self):
        ChromeDriverManager().install()
        driver = webdriver.Chrome()
        return driver

    def navigate_to_linkedin(self):
        self.driver.get('https://www.linkedin.com/')
        self.driver.find_element(By.CLASS_NAME, 'nav__button-secondary').click()
    
    def wait_for_element(self, by, value, time):
        try:
            wait = WebDriverWait(self.driver, time)
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except NoSuchElementException:
            print(f"Elemento com {by}={value} não encontrado.")
            return None

    def login(self, email, password):
        self.driver.find_element(By.NAME ,'session_key').send_keys(email)
        self.driver.find_element(By.NAME, 'session_password').send_keys(password)
        self.driver.find_element(By.CLASS_NAME, 'btn__primary--large').click()

# Uso da classe
bot = LinkedInInteraction()
bot.navigate_to_linkedin()
bot.login(email, password)
if (bot.wait_for_element(By.CLASS_NAME, 'recognizedDevice__label', 20)):
    print('Check o LinkedIn no Celular...')
if (bot.wait_for_element(By.CLASS_NAME, 'scaffold-layout__sidebar', 20)):
    print('Perfil carregado com sucesso.')
