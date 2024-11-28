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
        self.browser.get(f"{self.live_server_url}")
        time.sleep(1)
        self.browser.find_element(By.LINK_TEXT, "Cadastre-se").click()








        # Preenche o formulário de cadastro
        time.sleep(1)
        self.browser.find_element(By.ID, "first_name").send_keys("Fulano de Tal")
        time.sleep(1)
        self.browser.find_element(By.ID, "username").send_keys("fulano2024")
        time.sleep(1)
        self.browser.find_element(By.ID, "email").send_keys("fulano2024@example.com")
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
        self.browser.find_element(By.ID, "login_input").send_keys("fulano2024")
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
        self.browser.find_element(By.ID, "name").send_keys("Comunidade Exemplo")
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
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'flex-grow') and contains(text(), 'Áreas de Plantio')]"))
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




       




        # Aguarda que o modal de criação seja carregado (se houver um modal ou nova página)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Nova Área de Plantio')]"))
        )
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
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'text-white') and contains(text(), 'Visualizar')]"))
        )
        # Clica no botão
        visualizar_area_plantio_btn.click()
        time.sleep(1)




        # Espera até que o botão "Criar Canteiro" seja visível e clicável
        criar_canteiro_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'text-white') and contains(text(), 'Criar Canteiro')]"))
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
            EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'brown-box')]//a")))




        # Clica no botão
        adicionar_cultivo_btn.click()
        time.sleep(1)




        # Aguarda que a próxima página ou modal de adicionar cultivo seja carregado
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Adicionar Cultivo')]"))
        )




        # Clicar em "Criar Novo Cultivo"
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Criar Novo Cultivo')]"))).click()
        time.sleep(1)




        # Espera até que a página de cadastrar cultivo seja carregada
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Cadastrar Cultivo')]")))
        time.sleep(1)




        # Preenche o campo abaixo de "Nome"
        self.browser.find_element(By.ID, "name").send_keys("Tomate")
        time.sleep(1)








        # Preenche o campo abaixo de "Ciclo de vida (em meses)"
        self.browser.find_element(By.ID, "lifecycle").send_keys("6")
        time.sleep(1)




        # Preenche o campo abaixo de "Intervalo de irrigação (em dias)"
        self.browser.find_element(By.ID, "irrigacao").send_keys("3")
        time.sleep(1)




        # Preenche o campo abaixo de "Intervalo de Poda (em dias):"
        self.browser.find_element(By.ID, "poda").send_keys("10")
        time.sleep(1)




        # Preenche o campo abaixo de "Intervalo de Manejo (em dias):"
        self.browser.find_element(By.ID, "manejo").send_keys("3")
        time.sleep(1)








        # Clica no botão "Cadastrar"
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)




        # Espera até que a mensagem de sucesso seja visível ou até ser redirecionado
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))).click()
        time.sleep(1)
       
        # Espera até que o botão de "Adicionar Cultivo" seja clicável
        adicionar_cultivo_btn = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'brown-box')]//a")))




        # Clica no botão
        adicionar_cultivo_btn.click()
        time.sleep(1)




        # Preencher Adicionar Cultivo no canteiro 1
        self.browser.find_element(By.ID, "type_name").click()
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Tomate')]"))).click()
        time.sleep(1)




        canteiro_qnt = self.browser.find_element(By.ID, "quantity").click()
        # Apaga o valor existente
        canteiro_qnt.send_keys(Keys.CONTROL + "a")  # Seleciona todo o texto no campo
        canteiro_qnt.send_keys(Keys.BACKSPACE)  # Apaga o texto selecionado
        time.sleep(0.5)




        # Insere o novo valor
        canteiro_qnt.send_keys("2")  # Digita o número 2
        time.sleep(0.5)




        data_plantio = self.browser.find_element(By.ID, "planting_date").click()




        #substituir dd/mm/aaa por uma data
        data_plantio.send_keys("29112024")
        time.sleep(0.5)




        comentario = self.browser.find_element(By.ID, "comment").click()
        comentario.send_keys("Tomate plantado com muito amor")




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


        # Pular para a aba de Tarefas
        botao_tasks = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'flex-grow') and contains(text(), 'Tarefas')]"))
        )
        # Realiza o clique no botão "Tarefas"
        botao_tasks.click()
        time.sleep(1)


        # Adicionar tarefa
        self.browser.find_element(By.ID, "addArea").click()
        time.sleep(1)




        # Espera até que a página de adicionar tarefa seja carregada
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Adicionar Tarefa')]"))
        )
        time.sleep(1)


        # Preenche o campo abaixo de "Descrição"
        self.browser.find_element(By.ID, "description").send_keys("Regar plantas")
        time.sleep(1)


        # Preenche o campo abaixo de "Data de início"
        self.browser.find_element(By.ID, "start_date").send_keys("28112024")
        time.sleep(1)


        # Preenche o campo abaixo de "Data final"
        self.browser.find_element(By.ID, "final_date").send_keys("28112025")
        time.sleep(1)


        # Preenche o campo abaixo de "Frequência"
        self.browser.find_element(By.ID, "recurrence").click()
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Semanal')]"))
).click()
        time.sleep(1)


        # Preenche o campo abaixo de "Local"
        self.browser.find_element(By.ID, "local").click()
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Área - Aline')]"))
).click()
        time.sleep(1)


        # Preenche o campo abaixo de "Local"
        self.browser.find_element(By.ID, "responsible_users").click()
        time.sleep(1)
        # Localiza o checkbox "Buscar" pelo seletor único
        checkbox_buscar = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'vscomp-toggle-all-button')]")))


        # Clica no checkbox "Buscar"
        checkbox_buscar.click()
        time.sleep(1)


        # Preenche o campo abaixo de "Status"
        self.browser.find_element(By.ID, "status").click()
        time.sleep(1)
        WebDriverWait(self.browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//option[contains(text(), 'Progresso')]"))
).click()
        time.sleep(1)


        # Preenche o campo abaixo de "Material"
        self.browser.find_element(By.ID, "'material'").send_keys("água e regador")
        time.sleep(1)


        # Clica no botão de Criar
        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(1)
        # Espera até que a mensagem de sucesso seja visível ou até ser redirecionado
        WebDriverWait(self.browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))
).click()
        time.sleep(1)






        # H10 MENSAGEM DE DELETAR TAREFA


        # Localiza o botão "Consultar" pelo texto
        botao_consultar = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'bg-[#8ABF17]') and text()='Consultar']"))
        )


        # Clica no botão "Consultar"
        botao_consultar.click()
        time.sleep(1)


        # Espera até que a página de Editar Tarefa seja carregada
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Editar Tarefa 2')]"))
        )
        time.sleep(1)


        # Localiza o botão "Excluir" pelo seletor único
        botao_excluir = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'bg-red-500') and text()='Excluir']"))
        )


        # Clica no botão "Excluir"
        botao_excluir.click()
        time.sleep(1)


        # Clica no botão de Cancelar o cancelamento
        self.browser.find_element(By.CSS_SELECTOR, "button[type='button']").click()
        time.sleep(1)


        # Clica no botão de Cancelar a edição
        self.browser.find_element(By.CSS_SELECTOR, "button[type='button']").click()
        time.sleep(1)


        # Localiza o elemento "Pendente" pelo seletor único
        status_pendente = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='status-dropdown-2' and contains(@class, 'bg-red-700')]"))
        )


        # Clica no elemento "Pendente"
        status_pendente.click()
        time.sleep(1)


        # Localiza o botão "Concluída" pelo texto ou atributo 'onclick'
        botao_concluida = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'relative') and contains(@onclick, \"changeStatus(2, 'Concluída')\")]"))
        )


        # Clica no botão "Concluída"
        botao_concluida.click()
        time.sleep(1)


        # Espera até que a mensagem de sucesso seja visível ou até ser redirecionado
        WebDriverWait(self.browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'OK')]"))
).click()
        time.sleep(1)