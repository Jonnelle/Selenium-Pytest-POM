"""
产品页面对象
AutomationExercise网站产品页面
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import log


class ProductsPage(BasePage):
    """产品页面对象"""

    # 页面标题和元素
    PAGE_TITLE = (By.XPATH, "//h2[@class='title text-center']")
    ALL_PRODUCTS_TITLE = (By.XPATH, "//h2[text()='All Products']")

    # 搜索功能
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")
    SEARCHED_PRODUCTS_TITLE = (By.XPATH, "//h2[@class='title text-center' and text()='Searched Products']")

    # 产品列表
    PRODUCT_ITEMS = (By.CLASS_NAME, "productinfo")
    PRODUCT_CARDS = (By.XPATH, "//div[@class='col-sm-4']")
    PRODUCT_IMAGES = (By.XPATH, "//div[@class='productinfo text-center']//img")
    PRODUCT_NAMES = (By.XPATH, "//div[@class='productinfo text-center']//p")
    PRODUCT_PRICES = (By.XPATH, "//div[@class='productinfo text-center']//h2")

    # 产品操作按钮
    VIEW_PRODUCT_LINKS = (By.XPATH, "//a[contains(text(), 'View Product')]")
    ADD_TO_CART_BUTTONS = (By.XPATH, "//a[contains(@class, 'add-to-cart')]")

    # 产品悬停时显示的叠加层
    PRODUCT_OVERLAY = (By.CLASS_NAME, "product-overlay")
    OVERLAY_ADD_TO_CART = (By.XPATH, "//div[@class='overlay-content']//a[contains(@class, 'add-to-cart')]")

    # 分类侧边栏
    CATEGORY_PANEL = (By.XPATH, "//div[@class='left-sidebar']")
    WOMEN_CATEGORY = (By.XPATH, "//a[@href='#Women']")
    MEN_CATEGORY = (By.XPATH, "//a[@href='#Men']")
    KIDS_CATEGORY = (By.XPATH, "//a[@href='#Kids']")

    # 品牌侧边栏
    BRANDS_PANEL = (By.XPATH, "//div[@class='brands_products']")
    BRAND_LINKS = (By.XPATH, "//div[@class='brands_products']//li/a")

    # 模态框
    MODAL = (By.CLASS_NAME, "modal")
    MODAL_TITLE = (By.XPATH, "//h4[@class='modal-title']")
    CONTINUE_SHOPPING_BUTTON = (By.XPATH, "//button[text()='Continue Shopping']")
    VIEW_CART_BUTTON = (By.XPATH, "//a[text()='View Cart']")

    # 无产品消息
    NO_PRODUCTS_MESSAGE = (By.XPATH, "//p[contains(text(), 'No products found')]")

    def __init__(self, driver):
        """初始化产品页面"""
        super().__init__(driver)
        self.page_url = f"{self.base_url}/products"

    def open_products_page(self):
        """打开产品页面"""
        self.open_page(self.page_url)
        log.step("Opened products page")
        return self

    def verify_page_loaded(self) -> bool:
        """验证页面加载成功"""
        log.step("Verifying products page loaded")
        return self.verify_element_visible(self.ALL_PRODUCTS_TITLE)

    def verify_all_products_title(self) -> bool:
        """验证所有产品标题"""
        log.step("Verifying 'All Products' title")
        return self.verify_element_visible(self.ALL_PRODUCTS_TITLE)

    def search_product(self, search_term: str):
        """
        搜索产品

        Args:
            search_term: 搜索词
        """
        log.step(f"Searching for product: {search_term}")

        # 输入搜索词
        self.send_keys(self.SEARCH_INPUT, search_term)

        # 点击搜索按钮
        self.click_element(self.SEARCH_BUTTON)

        return self

    def verify_searched_products_title(self) -> bool:
        """验证搜索产品标题"""
        log.step("Verifying 'Searched Products' title")
        return self.verify_element_visible(self.SEARCHED_PRODUCTS_TITLE)

    def get_product_count(self) -> int:
        """获取产品数量"""
        products = self.get_elements(self.PRODUCT_ITEMS)
        count = len(products)
        log.step(f"Found {count} products on page")
        return count

    def get_product_names(self) -> list:
        """获取所有产品名称"""
        elements = self.get_elements(self.PRODUCT_NAMES)
        names = [element.text for element in elements if element.text.strip()]
        log.step(f"Got product names: {names}")
        return names

    def get_product_prices(self) -> list:
        """获取所有产品价格"""
        elements = self.get_elements(self.PRODUCT_PRICES)
        prices = [element.text for element in elements if element.text.strip()]
        log.step(f"Got product prices: {prices}")
        return prices

    def verify_products_visible(self) -> bool:
        """验证产品可见"""
        log.step("Verifying products visible")
        return self.get_product_count() > 0

    def click_view_product_by_index(self, index: int = 0):
        """
        通过索引点击查看产品

        Args:
            index: 产品索引
        """
        log.step(f"Clicking view product for index: {index}")

        view_links = self.get_elements(self.VIEW_PRODUCT_LINKS)
        if index < len(view_links):
            # 滚动到元素
            self.scroll_to_element(self.VIEW_PRODUCT_LINKS)
            view_links[index].click()
        else:
            log.error(f"Product index {index} not found")

        return self

    def click_view_first_product(self):
        """点击查看第一个产品"""
        log.step("Clicking view first product")
        self.click_view_product_by_index(0)
        return self

    def add_product_to_cart_by_index(self, index: int = 0):
        """
        通过索引添加产品到购物车

        Args:
            index: 产品索引
        """
        log.step(f"Adding product {index} to cart")

        add_buttons = self.get_elements(self.ADD_TO_CART_BUTTONS)
        if index < len(add_buttons):
            # 滚动到元素
            self.scroll_to_element(self.ADD_TO_CART_BUTTONS)
            add_buttons[index].click()
        else:
            log.error(f"Product index {index} not found")

        return self

    def add_first_product_to_cart(self):
        """添加第一个产品到购物车"""
        log.step("Adding first product to cart")
        self.add_product_to_cart_by_index(0)
        return self

    def hover_on_product_by_index(self, index: int = 0):
        """
        鼠标悬停在产品上

        Args:
            index: 产品索引
        """
        log.step(f"Hovering on product {index}")

        products = self.get_elements(self.PRODUCT_ITEMS)
        if index < len(products):
            self.scroll_to_element(self.PRODUCT_ITEMS)
            from selenium.webdriver.common.action_chains import ActionChains
            ActionChains(self.driver).move_to_element(products[index]).perform()

        return self

    def click_overlay_add_to_cart(self):
        """点击叠加层的添加到购物车按钮"""
        log.step("Clicking overlay add to cart")
        self.click_element(self.OVERLAY_ADD_TO_CART)
        return self

    def verify_modal_appeared(self) -> bool:
        """验证模态框出现"""
        log.step("Verifying modal appeared")
        return self.verify_element_visible(self.MODAL, timeout=5)

    def click_continue_shopping(self):
        """点击继续购物按钮"""
        log.step("Clicking continue shopping")
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)
        return self

    def click_view_cart_from_modal(self):
        """从模态框点击查看购物车"""
        log.step("Clicking view cart from modal")
        self.click_element(self.VIEW_CART_BUTTON)
        return self

    def search_and_verify_results(self, search_term: str) -> bool:
        """
        搜索并验证结果

        Args:
            search_term: 搜索词

        Returns:
            是否有搜索结果
        """
        log.step(f"Searching and verifying results for: {search_term}")

        # 执行搜索
        self.search_product(search_term)

        # 验证搜索结果标题
        if not self.verify_searched_products_title():
            return False

        # 检查是否有产品
        return self.verify_products_visible()

    def verify_search_results_contain_term(self, search_term: str) -> bool:
        """
        验证搜索结果包含搜索词

        Args:
            search_term: 搜索词

        Returns:
            是否包含搜索词
        """
        log.step(f"Verifying search results contain term: {search_term}")

        product_names = self.get_product_names()

        for name in product_names:
            if search_term.lower() in name.lower():
                log.step(f"Found matching product: {name}")
                return True

        log.warning(f"No products found containing term: {search_term}")
        return False

    def get_search_input_value(self) -> str:
        """获取搜索输入框的值"""
        return self.get_attribute(self.SEARCH_INPUT, "value")

    def clear_search_input(self):
        """清空搜索输入框"""
        log.step("Clearing search input")
        self.clear_and_send_keys(self.SEARCH_INPUT, "")
        return self

    def verify_category_panel_visible(self) -> bool:
        """验证分类面板可见"""
        log.step("Verifying category panel visible")
        return self.verify_element_visible(self.CATEGORY_PANEL)

    def verify_brands_panel_visible(self) -> bool:
        """验证品牌面板可见"""
        log.step("Verifying brands panel visible")
        return self.verify_element_visible(self.BRANDS_PANEL)

    def get_available_brands(self) -> list:
        """获取可用品牌列表"""
        log.step("Getting available brands")

        brand_elements = self.get_elements(self.BRAND_LINKS)
        brands = [element.text for element in brand_elements if element.text.strip()]

        log.step(f"Found brands: {brands}")
        return brands

    def click_brand_by_name(self, brand_name: str):
        """
        通过名称点击品牌

        Args:
            brand_name: 品牌名称
        """
        log.step(f"Clicking brand: {brand_name}")

        brand_locator = (By.XPATH, f"//a[contains(@href, '/brand_products/{brand_name}')]")
        self.click_element(brand_locator)

        return self

    def verify_no_products_message(self) -> bool:
        """验证无产品消息"""
        log.step("Verifying no products message")
        return self.verify_element_visible(self.NO_PRODUCTS_MESSAGE)
