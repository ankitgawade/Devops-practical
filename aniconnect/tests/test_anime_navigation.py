from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from aniconnect.models import AniconnectAniDesc


class AnimeNavigationSeleniumTests(StaticLiveServerTestCase):
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
        User.objects.create_user(username="animeuser", password="TestPass123!")
        AniconnectAniDesc.objects.create(
            anime_id=999002,
            name="One Piece",
            synopsis="Pirate adventure",
            image_url="https://example.com/onepiece.jpg",
            genres="Adventure",
        )

    def test_user_can_open_an_anime_page_from_home(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, "username").send_keys("animeuser")
        self.browser.find_element(By.NAME, "password").send_keys("TestPass123!")
        self.browser.find_element(By.XPATH, "//button[text()='Submit']").click()

        anime_link = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "One Piece"))
        )
        anime_link.click()

        anime_title = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h5.card-title"))
        )
        self.assertEqual(anime_title.text, "One Piece")
