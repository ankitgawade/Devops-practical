from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class RegisterSeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        cls.browser = webdriver.Chrome(options=chrome_options)
        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_user_can_register_from_register_page(self):
        self.browser.get(f"{self.live_server_url}/register/")

        self.browser.find_element(By.NAME, "username").send_keys("registeruser")
        self.browser.find_element(By.NAME, "email").send_keys("registeruser@example.com")
        self.browser.find_element(By.NAME, "password1").send_keys("TestPass123!")
        self.browser.find_element(By.NAME, "password2").send_keys("TestPass123!")
        self.browser.find_element(By.XPATH, "//button[text()='Register']").click()

        WebDriverWait(self.browser, 10).until(EC.url_to_be(f"{self.live_server_url}/"))
        logout_link = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Logout"))
        )
        self.assertTrue(logout_link.is_displayed())
