from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os

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

    def login(self, email, password):
        self.driver.find_element(By.NAME ,'session_key').send_keys(email)
        self.driver.find_element(By.NAME, 'session_password').send_keys(password)

# Uso da classe
bot = LinkedInInteraction()
bot.navigate_to_linkedin()
bot.login(email, password)
