from unittest import TestCase
from unfi_api.unfi_driver import UnfiDriver


class TestUnfiDriver(TestCase):

    def test_create_driver(self):
        unfi_driver = UnfiDriver()
        unfi_driver.quit()

    def test_web_driver_login(self):
        unfi_driver = UnfiDriver()
        unfi_driver.login("grocery@capellamarket.com", "Organic1")
        # this shouldnt work if login fails
        unfi_driver.get_current_account()
        unfi_driver.quit()

    def test_set_account(self):
        unfi_driver = UnfiDriver()
        unfi_driver.login("grocery@capellamarket.com", "Organic1")
        unfi_driver.set_account("001014")
        print(unfi_driver.get_current_account())
        # self.assertEqual(unfi_driver.get_current_account(), "001014")
        unfi_driver.set_account("001016")
        # self.assertEqual(unfi_driver.get_current_account(), "001016")
        print(unfi_driver.get_current_account())

    def test_get_token(self):
        unfi_driver = UnfiDriver()
        unfi_driver.login("grocery@capellamarket.com", "Organic1")
        unfi_driver.set_account("001014")
        tok1 = unfi_driver.get_token()
        self.assertEqual(len(unfi_driver.get_token()), 745)
        unfi_driver.set_account("001016")
        tok2 = unfi_driver.get_token()
