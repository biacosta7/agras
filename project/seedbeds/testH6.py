from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time




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
        self.browser.find_element(By.ID, "username").send_keys("fulano6")
        time.sleep(1)
        self.browser.find_element(By.ID, "email").send_keys("fulano6@example.com")
        time.sleep(1)
        self.browser.find_element(By.ID, "state").click()
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Pernambuco')]"))
).click()
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
        WebDriverWait(self.browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))
).click()
        time.sleep(1)
        # Preenche o formulário de login
        self.browser.find_element(By.ID, "login_input").send_keys("fulano6")
        time.sleep(1)
        self.browser.find_element(By.ID, "password").send_keys("senha_segura")




        # Clica no botão de login
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()




        # Verifica se o login foi bem-sucedido, checando a presença de um elemento específico da página de usuário logado
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))
).click()
       
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Criar comunidade')]"))
).click()
       
        time.sleep(1)
        # Espera até que a página de criação de comunidade seja carregada
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Nova comunidade')]"))
        )
        time.sleep(1)




        # Preenche o campo abaixo de "Nome"
        self.browser.find_element(By.ID, "name").send_keys("Comunidade Exemplo6")
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
        time.sleep(1)


        # Espera até que o botão "Áreas de Plantio" esteja visível e clicável
        botao_areas_plantio = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/a[2]/span[2]'))
        )
        # Realiza o clique no botão "Áreas de Plantio"
        botao_areas_plantio.click()
        time.sleep(1)


        # Espera até que o botão "Criar Área de Plantio" seja visível e clicável
        criar_area_plantio_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.ID, "addCommunityBtn"))
        )
        # Clica no botão
        criar_area_plantio_btn.click()
        time.sleep(1)

        # Preenche o campo abaixo de "Nome"
        self.browser.find_element(By.ID, "name").send_keys("Área 1")
        time.sleep(1)

        # Preenche o campo abaixo de "Descrição"
        self.browser.find_element(By.ID, "description").send_keys("área de plantio 1")
        time.sleep(1)

        # Clica no botão "Criar"
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)

        # Espera até que a mensagem de sucesso seja visível ou até ser redirecionado
        WebDriverWait(self.browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))).click()
        time.sleep(1)