from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class LoginTests(LiveServerTestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")  # Maximize window on startup
        self.browser = webdriver.Chrome(options=options)
        self.browser.implicitly_wait(10)  # Implicit wait for elements

    def tearDown(self):
        self.browser.quit()  # Close the browser after each test

    def test_login(self):
        self.browser.get(f"{self.live_server_url}/auth/login/?next=/")

        login_input = self.browser.find_element(By.ID, "login_input")
        password_input = self.browser.find_element(By.ID, "password") # or similar wait
        login_button = self.browser.find_element(By.ID, "login_button") # or similar wait

        time.sleep(2)
        login_input.send_keys("usuario_teste")  # Your test username
        time.sleep(2)
        password_input.send_keys("senha123")    # Your test password
        time.sleep(2)
        login_button.click()

        try:
            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".swal2-title"))
            )

            error_message = self.browser.find_element(By.CSS_SELECTOR, ".swal2-title").text
            self.assertEqual(error_message, "Usuário ou senha inválidos.")

             # Accept the alert to continue the test.
            confirm_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".swal2-confirm"))
            )
            time.sleep(3)
            confirm_button.click()

            WebDriverWait(self.browser, 10).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".swal2-container"))
            )
        except:
            self.fail("SweetAlert2 error message not found or not visible after failed login")