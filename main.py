from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

ChromeDriverManager().install()
driver = webdriver.Chrome()

driver.get('https://www.linkedin.com/')
driver.find_element(By.CLASS_NAME, 'nav__button-secondary').click()

driver.find_element(By.NAME ,'session_key').send_keys('your_email')
driver.find_element(By.NAME, 'session_password').send_keys('your_password')

sleep(1000)
