#!/usr/bin/env python

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class BasePage(object):
    """ Page Object containing locators and functional items for all shared elements
        between pages including:
        - Header
        - Footer
    """
    def __init__(self, driver):
        super(BasePage, self).__init__()
        self.driver = driver
        self.driver.implicitly_wait(10)
        self.url = "http://shop.fender.com/en-US/"
        self.wait = WebDriverWait(self.driver, 30)
        self.locators = {
            "header": {
                "header_nav": (By.CSS_SELECTOR, 'div#navigation'),
                "search_bar": (By.CSS_SELECTOR, 'input#search-value'),
                "nav_products": (By.CSS_SELECTOR, 'nav#siteNav ul li.item a[data-category-id=fender-products]'),
                "cart": (By.CSS_SELECTOR, 'div.mini-cart-total'),
                "cart_quantity_text": (By.CSS_SELECTOR, 'div.mini-cart-total span.mini-cart-qty')
            }
        }

        self.page_elements = []
        self.failed_elements = []

    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def title(self):
        return self.driver.title

    def __str__(self):
        if self.url:
            print "\nURL: {}\n".format(self.url)

        if self.page_elements:
            print "Page Elements\n"
            for item in self.page_elements:
                print "- {}".format(item)
            print "\n"

    def navigate(self):
        """Navigate to instantiated class' url"""
        self.driver.get(self.url)

    # ---- ELEMENT RETRIEVAL ----
    def _get_elements_from_locators_key(self, locator_key):
        """ Retrieve all elements listed under specified section of locator dictionary.

            Dynamically applies the correct locator retrieval function based on the
            naming of each element locator key in the locator dictionary.

            :param locator_key: section key name within locator dict
            :type locator_key: str
        """
        for name, locator in self.locators[locator_key].iteritems():
            try:
                if "text" in name:
                    setattr(self, name, self.driver.find_element(*locator).text)
                elif "list" in name:
                    setattr(self, name, self.driver.find_elements(*locator))
                else:
                    setattr(self, name, self.driver.find_element(*locator))
            except NoSuchElementException:
                self.failed_elements.append(name)
            else:
                self.page_elements.append(name)

    def get_elements(self, section_name=None):
        """ Get Page Elements

            :param section_name: Name of section from self.locators dictionary (e.g. "header")
            :type section_name: str
        """
        if section_name:
            try:
                locator_key = self.locators[section_name]
            except:
                raise Exception("Failed to load locator. Incorrect locator key - {}".format(section_name))
            else:
                self._get_elements_from_locators_key(locator_key)
        else:
            for section_name, locator_key in self.locators.iteritems():
                self._get_elements_from_locators_key(locator_key)

    def get_header_elements(self):
        self._get_elements_from_locators_key("header")

    def select_from_dropdown(self, dropdown_element, value):
        select = Select(dropdown_element)
        try:
            select.select_by_visible_text(value)
        except NoSuchElementException:
            print "{} is not a valid option. Please try one of the following:\n".format(value)
            for option in select.options:
                print "\t- {}".format(option.text)
            print "\n"
            raise

    # ---- WAIT UTILS ----
    def wait_until_title_contains(self, phrase):
        """ Wait for title to contain supplied phrase

            :param phrase: phrase contained in title
            :type phrase: str
        """
        self.wait.until(EC.title_contains(phrase))


    def wait_for_visibility_of_element(self, element):
        """ Wait for visibility of element before proceeding

            element: WebElement
        """
        self.wait.until(EC.visibility_of_element_located(
            element)
        )

    # ---- ACTION CHAINS ----
    def hover_over(self, element):
        """ Hover over element passed in as argument

            element: WebElement
        """
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.perform()

    def hover_over_and_click(self, element):
        """ Hover over element passed in as argument

            element: WebElement
        """
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click(element)
        actions.perform()

    def search_and_submit(self, search_phrase):
        if not hasattr(self, "search_bar"):
            self.search_bar = self.driver.find_element(
                *self.locators["header"]["search_bar"])
        self.search_bar.send_keys(search_phrase)
        self.search_bar.send_keys(Keys.RETURN)

    def fill_form_element(self, form_element, value):
        try:
            form_element.clear()
            form_element.send_keys(value)
        except:
            print "Form Element Not Present"

    # ---- MINI CART FUNCTIONS ----
    def get_mini_cart_product_metadata(self, index):
        """ Get metadata for specified index item in mini cart.

            :param index: list index number of item in mini cart. Starts with 1 and is
                            in desc order. So the first item is 1, second is 2, etc.
            :type index: int
        """
        item_name = "mini_cart_item_{}_name".format(index)
        item_color = "mini_cart_item_{}_color".format(index)
        item_fingerboard = "mini_cart_item_{}_fingerboard".format(index)
        item_price = "mini_cart_item_{}_price".format(index)
        item_quantity = "mini_cart_item_{}_quantity".format(index)
        name_locator = "div.mini-cart-product:nth-child({}) div.mini-cart-name a".format(index)
        color_locator = "div.mini-cart-product:nth-child({}) div.attribute:nth-child(1) span.value".format(index)
        fingerboard_locator = "div.mini-cart-product:nth-child({}) div.attribute:nth-child(2) span.value".format(index)
        price_locator = "div.mini-cart-product:nth-child({}) span.mini-cart-price".format(index)
        quantity_locator = "div.mini-cart-product:nth-child({}) div.mini-cart-qty p span.value".format(index)

        try:
            setattr(self, item_name, self.driver.find_element_by_css_selector(name_locator).text)
            setattr(self, item_color, self.driver.find_element_by_css_selector(color_locator).text)
            setattr(self, item_fingerboard, self.driver.find_element_by_css_selector(fingerboard_locator).text)
            setattr(self, item_price, self.driver.find_element_by_css_selector(price_locator).text)
            setattr(self, item_quantity, int(self.driver.find_element_by_css_selector(quantity_locator).text))
        except NoSuchElementException:
            pass

    def get_mini_cart_quantity(self):
        """ Retrieve cart quantity value from View Cart section in header """
        try:
            quantity = self.driver.find_element_by_css_selector("span.mini-cart-qty")
            setattr(self, "mini_cart_quantity", int(quantity.text.strip("()")))
        except NoSuchElementException:
            self.failed_elements.append("mini_cart_quantity")
            print "Cart Quantity element cannot be found"
        except AttributeError:
            self.failed_elements.append("mini_cart_quantity")
            print "Cart Quantity element cannot be found"
        finally:
            if not hasattr(self, "mini_cart_quantity"):
                self.mini_cart_quantity = 0

    def mini_cart_content_is_displayed(self):
        """ Verify whether or not mini cart content is displayed.
            Returns either True or False.

            :type return: boolean
        """
        return self.driver.find_element_by_css_selector("div.mini-cart-content").is_displayed()

    def click_mini_cart_button(self):
        self.driver.find_element_by_css_selector("a.mini-cart-link").click()

class HomePage(BasePage):
    """ Page Object for Home Page elements and functionality"""
    def __init__(self, driver):
        super(HomePage, self).__init__(driver)


class ProductPage(BasePage):
    """ Page Object for Product Page elements and functionality """
    def __init__(self, driver):
        super(ProductPage, self).__init__(driver)
        self.locators.update({
                "product_metadata": {
                    "product_header": (By.CSS_SELECTOR, "h1.prod-name"),
                    "product_header_text": (By.CSS_SELECTOR, "h1.prod-name"),
                    "model_number_text": (By.CSS_SELECTOR, "span#pdpProductID"),
                    "selected_color_text": (
                        By.CSS_SELECTOR, "div.product-variations ul li.attribute:nth-child(1) div.selected-value span"),
                    "fingerboard_material_text": (
                        By.CSS_SELECTOR, "div.product-variations ul li.attribute:nth-child(2) div.selected-value span"),
                    "price_text": (By.CSS_SELECTOR, "span.price-sales")
                }
            })

    def get_metadata_elements(self):
        self._get_elements_from_locators_key("product_metadata")

    def add_to_cart(self):
        """ Add Product to cart """
        self.driver.find_element_by_css_selector("button#add-to-cart").click()


class CartPage(BasePage):
    """ Page Object for Cart Page elements and functionality """
    def __init__(self, driver):
        super(CartPage, self).__init__(driver)
        self.driver = driver

    def get_cart_product_metadata(self):
        """ Get metadata for specified index item on cart page.

            :param index: list index number of item in cart. Starts with 1 and is
                            in desc order. So the first item is 1, second is 2, etc.
            :type index: int
        """
        name_locator = '//*[@id="cart-items-form"]/fieldset/div/div/div[2]/div[2]/div[1]/h2'
        model_locator = '//*[@id="cart-items-form"]/fieldset/div/div/div[2]/div[2]/div[1]/p/span[2]'
        color_locator = '//*[@id="cart-items-form"]/fieldset/div/div/div[2]/div[2]/div[2]/div[1]/span[2]'
        fingerboard_locator = '//*[@id="cart-items-form"]/fieldset/div/div/div[2]/div[2]/div[2]/div[2]/span[2]'
        price_locator = '//*[@id="cart-items-form"]/fieldset/div/div/div[2]/div[3]/span'
        self.cart_item_name = self.driver.find_element_by_xpath(name_locator).text
        self.cart_item_model_number = self.driver.find_element_by_xpath(model_locator).text
        self.cart_item_color = self.driver.find_element_by_xpath(color_locator).text
        self.cart_item_fingerboard = self.driver.find_element_by_xpath(fingerboard_locator).text
        self.cart_item_price = self.driver.find_element_by_xpath(price_locator).text

        self.cart_item_dropdown = self.driver.find_element_by_css_selector("select#dw_frmquantity")

        select = Select(self.cart_item_dropdown)
        self.cart_item_quantity = select.first_selected_option.text

    def click_secure_checkout_button(self):
        self.driver.find_elements_by_css_selector("#checkout-form button")[2].click()

class CheckoutLoginPage(BasePage):
    """ Page Object for Checkout Login Page elements and functionality """
    def __init__(self, driver):
        super(CheckoutLoginPage, self).__init__(driver)
        self.driver = driver
        self.wait_until_title_contains("Checkout")

    def click_checkout_as_guest_button(self):
        """ Click checkout as guest button. Will navigate to next page """
        checkout_as_guest_button = self.driver.find_element_by_xpath(
            '//*[@id="primary"]/div[2]/div[3]/div/div/form/fieldset/div/button/span').click()


class ShippingPage(BasePage):
    """ Page Object for Shipping Page elements and functionality """
    def __init__(self, driver):
        super(ShippingPage, self).__init__(driver)
        self.driver = driver
        self.wait_until_title_contains("Checkout")

    def fill_in_and_submit_shipping_address(self):
        """ Fill in shipping form info and submit """
        self.driver.find_element_by_css_selector(
            "input#dwfrm_singleshipping_shippingAddress_addressFields_firstName").send_keys("Shawn")
        self.driver.find_element_by_css_selector(
            "input#dwfrm_singleshipping_shippingAddress_addressFields_lastName").send_keys("Bacot")
        self.driver.find_element_by_css_selector(
            "input#dwfrm_singleshipping_shippingAddress_addressFields_address1").send_keys(
            "833 S Plymouth Blvd Apt. 3")
        self.driver.find_element_by_css_selector(
            "input#dwfrm_singleshipping_shippingAddress_addressFields_city").send_keys(
            "Los Angeles")
        self.driver.find_element_by_css_selector(
            "input#dwfrm_singleshipping_shippingAddress_addressFields_zip").send_keys(
            "90005")
        self.driver.find_element_by_css_selector(
            "input#dwfrm_singleshipping_shippingAddress_addressFields_phone").send_keys(
            "9177745248")
        state_dropdown = self.driver.find_element_by_css_selector(
            "select#dwfrm_singleshipping_shippingAddress_addressFields_states_state")
        self.select_from_dropdown(state_dropdown, "California")

        # Submit Form
        self.driver.find_element_by_xpath('//*[@id="main"]/section[2]/div/div[2]/div[2]/div[2]/div[2]/label').click()

