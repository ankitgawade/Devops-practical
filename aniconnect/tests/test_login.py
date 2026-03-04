from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginSeleniumTests(StaticLiveServerTestCase):
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
        User.objects.create_user(username="loginuser", password="TestPass123!")

    def test_user_can_login_from_homepage(self):
        self.browser.get(self.live_server_url)

        self.browser.find_element(By.NAME, "username").send_keys("loginuser")
        self.browser.find_element(By.NAME, "password").send_keys("TestPass123!")
        self.browser.find_element(By.XPATH, "//button[text()='Submit']").click()

        logout_link = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Logout"))
        )
        self.assertTrue(logout_link.is_displayed())
