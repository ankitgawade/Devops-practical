from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class HomePageSeleniumTests(StaticLiveServerTestCase):
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

    def test_homepage_shows_login_form_for_guest(self):
        self.browser.get(self.live_server_url)

        page_title = self.browser.find_element(By.TAG_NAME, "h2").text
        self.assertEqual(page_title, "Login")

        username_input = self.browser.find_element(By.NAME, "username")
        password_input = self.browser.find_element(By.NAME, "password")
        self.assertTrue(username_input.is_displayed())
        self.assertTrue(password_input.is_displayed())

        sign_up_link = self.browser.find_element(By.LINK_TEXT, "Sign up!")
        self.assertTrue(sign_up_link.is_displayed())
