import os
import pickle
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

email = os.environ['LINKEDIN_EMAIL']
password = os.environ['LINKEDIN_PASSWORD']

class LinkedInInteraction:
    def __init__(self):
        self.driver = self.setup_driver()

    def setup_driver(self):
        ChromeDriverManager().install()
        opts = Options()
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        opts.add_argument("--disable-blink-features=AutomationControlled")

        if not os.path.exists('userdata'):
            os.makedirs('userdata')

        driver = webdriver.Chrome(options=opts)
        return driver

    def save_cookies(self):
        with open("userdata/cookies.pkl", "wb") as file:
            pickle.dump(self.driver.get_cookies(), file)

    def load_cookies(self):
        try:
            with open("userdata/cookies.pkl", "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
        except FileNotFoundError:
            pass

    def navigate_to_linkedin(self):
        self.driver.get('https://www.linkedin.com/login')
    
    def wait_for_element(self, by, value, time):
        try:
            wait = WebDriverWait(self.driver, time)
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except TimeoutException:
            return None

    def login(self, email, password):
        self.driver.find_element(By.NAME ,'session_key').send_keys(email)
        self.driver.find_element(By.NAME, 'session_password').send_keys(password)
        self.driver.find_element(By.CLASS_NAME, 'btn__primary--large').click()

        if (self.wait_for_element(By.CLASS_NAME, 'recognizedDevice__label', 20)):
          print('Check o LinkedIn no Celular...')
        if (self.wait_for_element(By.CLASS_NAME, 'scaffold-layout__sidebar', 20)):
            self.save_cookies()
            print('Perfil carregado com sucesso.')

    def invitations_accepted(self):
        self.load_cookies()
        self.driver.get('https://www.linkedin.com/mynetwork/invitation-manager/')
        sleep(5)
        while True:
            try:
                self.driver.find_element(By.CLASS_NAME, 'invitation-card__action-btn').click()
                sleep(3)
            except NoSuchElementException:
                break

        print('Convites aceitos com sucesso.')

    def controlled_scroll(self, scroll_step, sleep_time, max_fail_count=9999):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        fail_count = 0
        while True:
            self.driver.execute_script(f"window.scrollBy(0, {scroll_step});")
            sleep(sleep_time)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                fail_count += 1
                if fail_count >= max_fail_count:
                    break
            else:
                last_height = new_height
                fail_count = 0 

            self.like_posts()

            # exibir mais atualizações no feed
            # like_button = self.wait_for_element(By.XPATH, '//button[@aria-label="Reagir com gostei"]', 1)
            # see_new_publications = self.wait_for_element(By.XPATH, '//button[text()="Ver novas publicações"]', 1)
            # if like_button and like_button.get_attribute('aria-pressed') == 'false':
            #     like_button.click()
            # if see_new_publications:
            #     see_new_publications.click()
            
    def like_posts(self):
        self.load_cookies()
        self.driver.get('https://www.linkedin.com/feed/')
        self.controlled_scroll(scroll_step=450, sleep_time=2)

        posts = self.driver.find_elements(By.XPATH, '//button[@aria-label="Reagir com gostei"]')
        for post in posts:
            if post.get_attribute('aria-pressed') == 'false':
                post.click()
                sleep(2)

        print('Posts curtidos com sucesso.')

    def start(self):
        self.navigate_to_linkedin()
        self.login(email, password)
        self.controlled_scroll(scroll_step=450, sleep_time=2)

bot = LinkedInInteraction()
bot.start()
