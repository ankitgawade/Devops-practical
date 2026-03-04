from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LogoutSeleniumTests(StaticLiveServerTestCase):
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

    def setUp(self):
        User.objects.create_user(username="logoutuser", password="TestPass123!")

    def test_user_can_logout_after_login(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, "username").send_keys("logoutuser")
        self.browser.find_element(By.NAME, "password").send_keys("TestPass123!")
        self.browser.find_element(By.XPATH, "//button[text()='Submit']").click()

        logout_link = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))
        )
        logout_link.click()

        login_heading = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "h2"))
        )
        self.assertEqual(login_heading.text, "Login")
