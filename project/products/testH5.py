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
         
        self.browser.find_element(By.LINK_TEXT, "Cadastre-se").click()




        # Preenche o formulário de cadastro
         
        self.browser.find_element(By.ID, "first_name").send_keys("Fulano de Tal")
         
        self.browser.find_element(By.ID, "username").send_keys("fulano5")
         
        self.browser.find_element(By.ID, "email").send_keys("fulano5@example.com")
         
        self.browser.find_element(By.ID, "state").click()
         
        WebDriverWait(self.browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Pernambuco')]"))
).click()
         
        self.browser.find_element(By.ID, "city").send_keys("Cidade")
         
        self.browser.find_element(By.ID, "password").send_keys("senha_segura")
         
        self.browser.find_element(By.ID, "confirm_password").send_keys("senha_segura")




         
       
        # Clica no botão de cadastrar
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
         
        # Espera até que a mensagem de sucesso seja visível ou até ser redirecionado
        WebDriverWait(self.browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))
).click()
         
        # Preenche o formulário de login
        self.browser.find_element(By.ID, "login_input").send_keys("fulano5")
         
        self.browser.find_element(By.ID, "password").send_keys("senha_segura")




        # Clica no botão de login
         
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()




        # Verifica se o login foi bem-sucedido, checando a presença de um elemento específico da página de usuário logado
         
        WebDriverWait(self.browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))
).click()
       
         
        WebDriverWait(self.browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Criar comunidade')]"))
).click()
       
         
        # Espera até que a página de criação de comunidade seja carregada
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Nova comunidade')]"))
        )
         
        # Preenche o campo abaixo de "Nome"
        self.browser.find_element(By.ID, "name").send_keys("Comunidade Exemplo5")
         
        # Preenche o campo abaixo de "Descrição"
        self.browser.find_element(By.ID, "description").send_keys("Comunidade exemplo 1")
         
        # Clica no botão "Criar"
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
         
        # Espera até que a mensagem de sucesso seja visível ou até ser redirecionado
        WebDriverWait(self.browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))).click()
         
        # Espera até que o botão "Entrar" esteja visível e clicável
        botao_entrar = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'text-white') and contains(text(), 'Entrar')]"))
        )
        # Realiza o clique no botão "Entrar"
        botao_entrar.click()
         


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

        # Espera até que o botão "Visualizar" seja visível e clicável
        visualizar_area_plantio_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[3]/div/div/div/div[3]/a'))
        )
        # Clica no botão
        visualizar_area_plantio_btn.click()
        time.sleep(1)

        # Espera até que o botão "Criar Canteiro" seja visível e clicável
        criar_canteiro_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="addCommunityBtn"]'))
        )
        # Clica no botão
        criar_canteiro_btn.click()
        time.sleep(1)

        # Para funcionar, preenche o campo abaixo de "Nome"
        self.browser.find_element(By.ID, "seedbed_name").send_keys("Canteiro 1")
        time.sleep(1)

        #Para dar o erro necessário para a história
        # Clica no botão "Criar"
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)

        # Espera até que a mensagem de sucesso seja visível ou até ser redirecionado
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))).click()
        time.sleep(1)

        # Espera até que o botão "Visualizar" seja visível e clicável
        visualizar_canteiro_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'text-white') and contains(text(), 'Visualizar')]"))
        )
        # Clica no botão
        visualizar_canteiro_btn.click()
        time.sleep(1)

        # Espera até que o botão de "Adicionar Cultivo" seja clicável
        adicionar_cultivo_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[2]/a')))

        # Clica no botão
        adicionar_cultivo_btn.click()
        time.sleep(1)


        # Clicar em "Criar Novo Cultivo"
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/form/a'))).click()
        time.sleep(1)

        # Preenche o campo abaixo de "Nome"
        self.browser.find_element(By.XPATH, '//*[@id="nome"]').send_keys("Tomate")
        time.sleep(1)

        # Preenche o campo abaixo de "Ciclo de vida (em meses)"
        self.browser.find_element(By.XPATH, '//*[@id="lifecycle"]').send_keys("6")
        time.sleep(1)

        # Preenche o campo abaixo de "Intervalo de irrigação (em dias)"
        self.browser.find_element(By.XPATH, '//*[@id="irrigacao"]').send_keys("3")
        time.sleep(1)

        # Preenche o campo abaixo de "Intervalo de Poda (em dias):"
        self.browser.find_element(By.XPATH, '//*[@id="poda"]').send_keys("10")
        time.sleep(1)

        # Preenche o campo abaixo de "Intervalo de Manejo (em dias):"
        self.browser.find_element(By.XPATH, '//*[@id="manejo"]').send_keys("3")
        time.sleep(1)

        # Clica no botão "Cadastrar"
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)

        # Espera até que a mensagem de sucesso seja visível ou até ser redirecionado
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))).click()
        time.sleep(1)
       
        # Espera até que o botão de "Adicionar Cultivo" seja clicável
        adicionar_cultivo_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div[2]/a')))
        # Clica no botão
        adicionar_cultivo_btn.click()
        time.sleep(1)

        # Preencher Adicionar Cultivo no canteiro 1
        self.browser.find_element(By.ID, "type_name").click()
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Tomate')]"))).click()
        time.sleep(1)

        self.browser.find_element(By.XPATH, '//*[@id="quantity"]').send_keys("12")

        data_plantio = self.browser.find_element(By.XPATH, '//*[@id="planting_date"]').send_keys("29112024")


        self.browser.find_element(By.XPATH, '//*[@id="comment"]').send_keys("Tomate plantado com muito amor")

        # Clica no botão de Adicionar produto
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        # Espera até que a mensagem de sucesso seja visível ou até ser redirecionado
        WebDriverWait(self.browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))
).click()
        time.sleep(1)

        # Localiza o elemento correspondente ao "Tomate" pelo atributo único
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'brown-box') and @data-product-id='22']"))
        ).click()
        time.sleep(1)