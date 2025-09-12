"""
购物车页面对象
AutomationExercise网站购物车页面
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import log


class CartPage(BasePage):
    """购物车页面对象"""

    # 页面标题
    CART_TITLE = (By.XPATH, "//ol[@class='breadcrumb']")
    SHOPPING_CART_TITLE = (By.XPATH, "//h2[text()='Shopping Cart']")

    # 购物车表格
    CART_TABLE = (By.ID, "cart_info_table")
    CART_ITEMS = (By.XPATH, "//tbody/tr")

    # 产品信息列
    PRODUCT_IMAGES = (By.XPATH, "//td[@class='cart_product']//img")
    PRODUCT_NAMES = (By.XPATH, "//td[@class='cart_description']//h4/a")
    PRODUCT_PRICES = (By.XPATH, "//td[@class='cart_price']//p")
    PRODUCT_QUANTITIES = (By.XPATH, "//td[@class='cart_quantity']//button")
    PRODUCT_TOTALS = (By.XPATH, "//td[@class='cart_total']//p")

    # 数量控制
    QUANTITY_INPUTS = (By.XPATH, "//td[@class='cart_quantity']//input")

    # 删除按钮
    DELETE_BUTTONS = (By.XPATH, "//td[@class='cart_delete']//a")

    # 空购物车消息
    EMPTY_CART_MESSAGE = (By.XPATH, "//b[contains(text(), 'Cart is empty')]")

    # 结账区域
    PROCEED_TO_CHECKOUT_BUTTON = (By.XPATH, "//a[text()='Proceed To Checkout']")

    # 登录/注册链接（在结账时可能出现）
    LOGIN_REGISTER_LINK = (By.XPATH, "//a[@href='/login']")

    # 总价区域
    TOTAL_AMOUNT = (By.XPATH, "//tr[@id='total_amount']//p")

    def __init__(self, driver):
        """初始化购物车页面"""
        super().__init__(driver)
        self.page_url = f"{self.base_url}/view_cart"

    def open_cart_page(self):
        """打开购物车页面"""
        self.open_page(self.page_url)
        log.step("Opened cart page")
        return self

    def verify_page_loaded(self) -> bool:
        """验证页面加载成功"""
        log.step("Verifying cart page loaded")
        return (self.verify_element_visible(self.CART_TABLE) or
                self.verify_element_visible(self.EMPTY_CART_MESSAGE))

    def verify_cart_table_visible(self) -> bool:
        """验证购物车表格可见"""
        log.step("Verifying cart table visible")
        return self.verify_element_visible(self.CART_TABLE)

    def get_cart_item_count(self) -> int:
        """获取购物车商品数量"""
        items = self.get_elements(self.CART_ITEMS)
        count = len(items)
        log.step(f"Cart contains {count} items")
        return count

    def verify_cart_is_empty(self) -> bool:
        """验证购物车为空"""
        log.step("Verifying cart is empty")
        return (self.verify_element_visible(self.EMPTY_CART_MESSAGE) or
                self.get_cart_item_count() == 0)

    def verify_cart_has_items(self) -> bool:
        """验证购物车有商品"""
        log.step("Verifying cart has items")
        return self.get_cart_item_count() > 0

    def get_product_names_in_cart(self) -> list:
        """获取购物车中的产品名称"""
        log.step("Getting product names in cart")

        name_elements = self.get_elements(self.PRODUCT_NAMES)
        names = [element.text for element in name_elements]

        log.step(f"Products in cart: {names}")
        return names

    def get_product_prices_in_cart(self) -> list:
        """获取购物车中的产品价格"""
        log.step("Getting product prices in cart")

        price_elements = self.get_elements(self.PRODUCT_PRICES)
        prices = [element.text for element in price_elements]

        log.step(f"Product prices in cart: {prices}")
        return prices

    def get_product_quantities_in_cart(self) -> list:
        """获取购物车中的产品数量"""
        log.step("Getting product quantities in cart")

        quantity_elements = self.get_elements(self.QUANTITY_INPUTS)
        quantities = [element.get_attribute("value") for element in quantity_elements]

        log.step(f"Product quantities in cart: {quantities}")
        return quantities

    def get_product_totals_in_cart(self) -> list:
        """获取购物车中的产品小计"""
        log.step("Getting product totals in cart")

        total_elements = self.get_elements(self.PRODUCT_TOTALS)
        totals = [element.text for element in total_elements]

        log.step(f"Product totals in cart: {totals}")
        return totals

    def delete_product_by_index(self, index: int = 0):
        """
        通过索引删除产品

        Args:
            index: 产品索引
        """
        log.step(f"Deleting product at index {index}")

        delete_buttons = self.get_elements(self.DELETE_BUTTONS)
        if index < len(delete_buttons):
            delete_buttons[index].click()
        else:
            log.error(f"Product index {index} not found")

        return self

    def delete_first_product(self):
        """删除第一个产品"""
        log.step("Deleting first product")
        self.delete_product_by_index(0)
        return self

    def update_product_quantity(self, index: int, quantity: str):
        """
        更新产品数量

        Args:
            index: 产品索引
            quantity: 新数量
        """
        log.step(f"Updating product {index} quantity to {quantity}")

        quantity_inputs = self.get_elements(self.QUANTITY_INPUTS)
        if index < len(quantity_inputs):
            self.clear_and_send_keys(
                (By.XPATH, f"(//td[@class='cart_quantity']//input)[{index + 1}]"),
                quantity
            )

        return self

    def verify_product_in_cart(self, product_name: str) -> bool:
        """
        验证产品在购物车中

        Args:
            product_name: 产品名称

        Returns:
            是否在购物车中
        """
        log.step(f"Verifying product '{product_name}' in cart")

        product_names = self.get_product_names_in_cart()
        is_in_cart = any(product_name in name for name in product_names)

        log.assertion("Product in cart", product_name, str(product_names))
        return is_in_cart

    def verify_product_quantity(self, product_name: str, expected_quantity: str) -> bool:
        """
        验证产品数量

        Args:
            product_name: 产品名称
            expected_quantity: 期望数量

        Returns:
            数量是否正确
        """
        log.step(f"Verifying quantity for '{product_name}' is {expected_quantity}")

        product_names = self.get_product_names_in_cart()
        quantities = self.get_product_quantities_in_cart()

        for i, name in enumerate(product_names):
            if product_name in name and i < len(quantities):
                actual_quantity = quantities[i]
                is_correct = actual_quantity == expected_quantity
                log.assertion("Product quantity", expected_quantity, actual_quantity)
                return is_correct

        log.error(f"Product '{product_name}' not found in cart")
        return False

    def click_proceed_to_checkout(self):
        """点击结账按钮"""
        log.step("Clicking proceed to checkout")
        self.click_element(self.PROCEED_TO_CHECKOUT_BUTTON)
        return self

    def verify_proceed_to_checkout_button(self) -> bool:
        """验证结账按钮存在"""
        log.step("Verifying proceed to checkout button")
        return self.verify_element_visible(self.PROCEED_TO_CHECKOUT_BUTTON)

    def get_total_amount(self) -> str:
        """获取总金额"""
        log.step("Getting total amount")
        return self.get_text(self.TOTAL_AMOUNT)

    def verify_total_amount_visible(self) -> bool:
        """验证总金额可见"""
        log.step("Verifying total amount visible")
        return self.verify_element_visible(self.TOTAL_AMOUNT)

    def clear_cart(self):
        """清空购物车"""
        log.step("Clearing cart")

        # 删除所有商品
        while self.verify_cart_has_items():
            self.delete_first_product()
            # 等待页面更新
            self.wait_for_page_load()

            # 防止无限循环
            import time
            time.sleep(1)

        return self

    def get_cart_summary(self) -> dict:
        """获取购物车摘要信息"""
        log.step("Getting cart summary")

        summary = {
            "item_count": self.get_cart_item_count(),
            "product_names": self.get_product_names_in_cart(),
            "total_amount": self.get_total_amount() if self.verify_total_amount_visible() else "N/A",
            "is_empty": self.verify_cart_is_empty()
        }

        log.step(f"Cart summary: {summary}")
        return summary

    def verify_cart_page_elements(self) -> bool:
        """验证购物车页面关键元素"""
        log.step("Verifying cart page elements")

        # 如果购物车为空，只需验证空消息
        if self.verify_cart_is_empty():
            return self.verify_element_visible(self.EMPTY_CART_MESSAGE)

        # 如果有商品，验证表格和结账按钮
        return (self.verify_cart_table_visible() and
                self.verify_proceed_to_checkout_button())
