#!/usr/bin/env python

import time
import unittest

from selenium import webdriver
from nose.tools import *
from nose.plugins.attrib import attr

from pages import HomePage, ProductPage, CartPage, CheckoutLoginPage, ShippingPage


class TestFenderCheckoutProcess(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.home_page = HomePage(cls.driver)
        cls.home_page.navigate()
        cls.home_page.wait_until_title_contains("Fender")
        cls.home_page.driver.maximize_window()
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_checkout_process(self):
        # Get Header Nav Elements
        # self.home_page.get_header_elements()
        self.home_page.search_and_submit("jimi hendrix stratocaster")
        time.sleep(3)

        # Product Page validation
        self.product = ProductPage(self.driver)
        self.product.wait_until_title_contains("Jimi Hendrix")
        self.product.get_metadata_elements()

        self.assertIn("JIMI HENDRIX STRATOCASTER", self.product.product_header_text)
        self.assertEquals("OLYMPIC WHITE", self.product.selected_color_text)
        self.assertEquals("MAPLE", self.product.fingerboard_material_text)
        self.assertEquals("0145802305", self.product.model_number_text)

        self.product.add_to_cart()
        time.sleep(2) # Refactor! Should be using a proper wait here or ...
        self.assertTrue(self.product.mini_cart_content_is_displayed())
        self.product.get_mini_cart_quantity() # ...in this method
        self.assertEquals(self.product.mini_cart_quantity, 1)

        # Mini Cart Validation
        self.product.get_mini_cart_product_metadata(1)
        self.assertEquals(self.product.product_header_text, self.product.mini_cart_item_1_name)
        self.assertEquals(self.product.selected_color_text.lower(), self.product.mini_cart_item_1_color.lower())
        self.assertEquals(self.product.fingerboard_material_text.lower(), self.product.mini_cart_item_1_fingerboard.lower())
        self.assertEquals(self.product.price_text, self.product.mini_cart_item_1_price)
        self.assertEquals(self.product.mini_cart_item_1_quantity, 1)

        self.product.click_mini_cart_button()

        # Cart Page Validation
        self.cart = CartPage(self.driver)
        self.cart.wait_until_title_contains("Cart")
        self.cart.get_cart_product_metadata()

        self.assertIn("JIMI HENDRIX STRATOCASTER", self.cart.cart_item_name)
        self.assertEquals(self.cart.cart_item_model_number, "0145802305")
        self.assertEquals(self.cart.cart_item_color, "Olympic White")
        self.assertEquals(self.cart.cart_item_fingerboard, "Maple")
        self.assertEquals(self.cart.cart_item_price, "$899.99")
        self.assertEquals(self.cart.cart_item_quantity, "1")

        self.cart.click_secure_checkout_button()
        time.sleep(5)

        # Checkout as guest
        self.checkout_login = CheckoutLoginPage(self.driver)
        self.checkout_login.click_checkout_as_guest_button()
        time.sleep(3)

        # Shipping Page Data Entry
        self.shipping = ShippingPage(self.driver)
        self.shipping.fill_in_and_submit_shipping_address()
        time.sleep(5)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFenderCheckoutProcess)
    unittest.TextTestRunner(verbosity=2).run(suite)
