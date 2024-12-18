from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

# Criar comunidade

class UserRegistrationAndLoginTest(LiveServerTestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.browser = webdriver.Chrome(options=options)
        self.browser.implicitly_wait(10)


    def tearDown(self):
        self.browser.quit()


    def test_user_registration_and_login(self):
        # Navega até a página de cadastro
        self.browser.get("http://127.0.0.1:8000/")
          
        self.browser.find_element(By.LINK_TEXT, "Cadastre-se").click()


        # Preenche o formulário de cadastro
          
        self.browser.find_element(By.ID, "first_name").send_keys("Fulano de Tal")
          
        self.browser.find_element(By.ID, "username").send_keys("fulano3")
          
        self.browser.find_element(By.ID, "email").send_keys("fulano3@example.com")
          
        self.browser.find_element(By.ID, "state").click()
          
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Pernambuco')]"))).click()
          
        self.browser.find_element(By.ID, "city").send_keys("Cidade")
          
        self.browser.find_element(By.ID, "password").send_keys("senha_segura")
          
        self.browser.find_element(By.ID, "confirm_password").send_keys("senha_segura")


          
       
        # Clica no botão de cadastrar
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
          
        # Espera até que a mensagem de sucesso seja visível ou até ser redirecionado
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))).click()
          
        # Preenche o formulário de login
        self.browser.find_element(By.ID, "login_input").send_keys("fulano3")
          
        self.browser.find_element(By.ID, "password").send_keys("senha_segura")


        # Clica no botão de login
          
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


        # Verifica se o login foi bem-sucedido, checando a presença de um elemento específico da página de usuário logado
          
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))).click()
       
          
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Criar comunidade')]"))).click()
       
          
        # Espera até que a página de criação de comunidade seja carregada
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Nova comunidade')]")))
          


        # Preenche o campo abaixo de "Nome"
        self.browser.find_element(By.ID, "name").send_keys("Comunidade Exemplo3")
          


        # Preenche o campo abaixo de "Descrição"
        self.browser.find_element(By.ID, "description").send_keys("Comunidade exemplo 1")
          


        # Clica no botão "Criar"
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)


        # Espera até que a mensagem de sucesso seja visível ou até ser redirecionado
        WebDriverWait(self.browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))).click()
        time.sleep(1)