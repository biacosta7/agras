from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

# Usar o chat bot

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
        time.sleep(1)
        self.browser.find_element(By.LINK_TEXT, "Cadastre-se").click()


        # Preenche o formulário de cadastro
        time.sleep(1)
        self.browser.find_element(By.ID, "first_name").send_keys("Fulano de Tal")
        time.sleep(1)
        self.browser.find_element(By.ID, "username").send_keys("fulano17")
        time.sleep(1)
        self.browser.find_element(By.ID, "email").send_keys("fulano17@example.com")
        time.sleep(1)
        self.browser.find_element(By.ID, "state").click()
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Pernambuco')]"))).click()
        time.sleep(1)
        self.browser.find_element(By.ID, "city").send_keys("Cidade")
        time.sleep(1)
        self.browser.find_element(By.ID, "password").send_keys("senha_segura")
        time.sleep(1)
        self.browser.find_element(By.ID, "confirm_password").send_keys("senha_segura")


        time.sleep(1)
       
        # Clica no botão de cadastrar
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        # Espera até que a mensagem de sucesso seja visível ou até ser redirecionado
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))).click()
        time.sleep(1)
        # Preenche o formulário de login
        self.browser.find_element(By.ID, "login_input").send_keys("fulano17")
        time.sleep(1)
        self.browser.find_element(By.ID, "password").send_keys("senha_segura")


        # Clica no botão de login
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


        # Verifica se o login foi bem-sucedido, checando a presença de um elemento específico da página de usuário logado
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))).click()
       
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Criar comunidade')]"))).click()
       
        time.sleep(1)
        # Espera até que a página de criação de comunidade seja carregada
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Nova comunidade')]")))
        time.sleep(1)


        # Preenche o campo abaixo de "Nome"
        self.browser.find_element(By.ID, "name").send_keys("Comunidade Exemplo17")
        time.sleep(1)


        # Preenche o campo abaixo de "Descrição"
        self.browser.find_element(By.ID, "description").send_keys("Comunidade exemplo 1")
        time.sleep(1)


        # Clica no botão "Criar"
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)


        # Espera até que a mensagem de sucesso seja visível ou até ser redirecionado
        WebDriverWait(self.browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))).click()
        time.sleep(1)

        # Espera até que o botão "Entrar" esteja visível e clicável
        botao_entrar = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'text-white') and contains(text(), 'Entrar')]"))
        )
        # Realiza o clique no botão "Entrar"
        botao_entrar.click()

        # Clicar em CHAT/IA
        self.browser.find_element(By.XPATH, '//*[@id="help-button"]').click()
        time.sleep(1)

        # Digitar Duvida
        self.browser.find_element(By.XPATH, '//*[@id="helpModal"]/div[7]/input').send_keys("Como plantar tomate?")
        time.sleep(1)

        # Enter na duvida
        self.browser.find_element(By.XPATH, '//*[@id="helpModal"]/div[7]/button').click()
        time.sleep(10)


