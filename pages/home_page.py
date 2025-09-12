"""
首页页面对象
AutomationExercise网站首页
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import log


class HomePage(BasePage):
    """首页页面对象"""

    # 页面元素定位器
    LOGO = (By.XPATH, "//img[@alt='Website for automation practice']")
    HOME_LINK = (By.XPATH, "//a[contains(@href, '/')]//i[@class='fa fa-home']")
    PRODUCTS_LINK = (By.XPATH, "//a[@href='/products']")
    CART_LINK = (By.XPATH, "//a[@href='/view_cart']")
    SIGNUP_LOGIN_LINK = (By.XPATH, "//a[@href='/login']")
    TEST_CASES_LINK = (By.XPATH, "//a[@href='/test_cases']")
    API_TESTING_LINK = (By.XPATH, "//a[@href='/api_list']")
    VIDEO_TUTORIALS_LINK = (By.XPATH, "//a[contains(@href, 'youtube')]")
    CONTACT_US_LINK = (By.XPATH, "//a[@href='/contact_us']")

    # 轮播图
    CAROUSEL = (By.ID, "slider-carousel")
    CAROUSEL_SLIDES = (By.CLASS_NAME, "item")

    # 分类侧边栏
    CATEGORY_TITLE = (By.XPATH, "//h2[text()='Category']")
    WOMEN_CATEGORY = (By.XPATH, "//a[@href='#Women']")
    MEN_CATEGORY = (By.XPATH, "//a[@href='#Men']")
    KIDS_CATEGORY = (By.XPATH, "//a[@href='#Kids']")

    # 女装子分类
    WOMEN_DRESS = (By.XPATH, "//a[@href='/category_products/1']")
    WOMEN_TOPS = (By.XPATH, "//a[@href='/category_products/2']")
    WOMEN_SAREE = (By.XPATH, "//a[@href='/category_products/7']")

    # 男装子分类
    MEN_TSHIRTS = (By.XPATH, "//a[@href='/category_products/3']")
    MEN_JEANS = (By.XPATH, "//a[@href='/category_products/6']")

    # 童装子分类
    KIDS_DRESS = (By.XPATH, "//a[@href='/category_products/4']")
    KIDS_TOPS_SHIRTS = (By.XPATH, "//a[@href='/category_products/5']")

    # 品牌侧边栏
    BRANDS_TITLE = (By.XPATH, "//h2[text()='Brands']")
    POLO_BRAND = (By.XPATH, "//a[@href='/brand_products/Polo']")
    HM_BRAND = (By.XPATH, "//a[@href='/brand_products/H&M']")
    MADAME_BRAND = (By.XPATH, "//a[@href='/brand_products/Madame']")

    # 特色商品区域
    FEATURES_ITEMS_TITLE = (By.XPATH, "//h2[@class='title text-center']")
    PRODUCT_ITEMS = (By.CLASS_NAME, "productinfo")
    PRODUCT_IMAGES = (By.XPATH, "//div[@class='productinfo text-center']//img")
    PRODUCT_NAMES = (By.XPATH, "//div[@class='productinfo text-center']//p")
    PRODUCT_PRICES = (By.XPATH, "//div[@class='productinfo text-center']//h2")
    ADD_TO_CART_BUTTONS = (By.XPATH, "//a[contains(@class, 'add-to-cart')]")
    VIEW_PRODUCT_LINKS = (By.XPATH, "//a[contains(text(), 'View Product')]")

    # 推荐商品区域
    RECOMMENDED_ITEMS_TITLE = (By.XPATH, "//h2[text()='recommended items']")
    RECOMMENDED_PRODUCTS = (By.XPATH, "//div[@id='recommended-item-carousel']//div[@class='productinfo text-center']")

    # 页脚订阅区域
    SUBSCRIPTION_TITLE = (By.XPATH, "//h2[text()='Subscription']")
    EMAIL_INPUT = (By.ID, "susbscribe_email")
    SUBSCRIBE_BUTTON = (By.ID, "subscribe")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "alert-success")

    # 页脚版权信息
    COPYRIGHT = (By.XPATH, "//p[contains(text(), 'Copyright')]")

    def __init__(self, driver):
        """初始化首页"""
        super().__init__(driver)
        self.page_url = self.base_url

    def open_home_page(self):
        """打开首页"""
        self.open_page(self.page_url)
        log.step("Opened home page")
        return self

    def verify_page_loaded(self) -> bool:
        """验证页面加载成功"""
        log.step("Verifying home page loaded")
        return (self.verify_element_visible(self.LOGO) and
                self.verify_element_visible(self.FEATURES_ITEMS_TITLE))

    def click_products_link(self):
        """点击产品链接"""
        log.step("Clicking products link")
        self.click_element(self.PRODUCTS_LINK)
        return self

    def click_cart_link(self):
        """点击购物车链接"""
        log.step("Clicking cart link")
        self.click_element(self.CART_LINK)
        return self

    def click_signup_login_link(self):
        """点击注册/登录链接"""
        log.step("Clicking signup/login link")
        self.click_element(self.SIGNUP_LOGIN_LINK)
        return self

    def click_contact_us_link(self):
        """点击联系我们链接"""
        log.step("Clicking contact us link")
        self.click_element(self.CONTACT_US_LINK)
        return self

    def click_test_cases_link(self):
        """点击测试用例链接"""
        log.step("Clicking test cases link")
        self.click_element(self.TEST_CASES_LINK)
        return self

    def expand_women_category(self):
        """展开女装分类"""
        log.step("Expanding women category")
        self.click_element(self.WOMEN_CATEGORY)
        return self

    def expand_men_category(self):
        """展开男装分类"""
        log.step("Expanding men category")
        self.click_element(self.MEN_CATEGORY)
        return self

    def expand_kids_category(self):
        """展开童装分类"""
        log.step("Expanding kids category")
        self.click_element(self.KIDS_CATEGORY)
        return self

    def click_women_dress_category(self):
        """点击女装连衣裙分类"""
        log.step("Clicking women dress category")
        self.expand_women_category()
        self.click_element(self.WOMEN_DRESS)
        return self

    def click_women_tops_category(self):
        """点击女装上衣分类"""
        log.step("Clicking women tops category")
        self.expand_women_category()
        self.click_element(self.WOMEN_TOPS)
        return self

    def click_men_tshirts_category(self):
        """点击男装T恤分类"""
        log.step("Clicking men tshirts category")
        self.expand_men_category()
        self.click_element(self.MEN_TSHIRTS)
        return self

    def click_brand(self, brand_name: str):
        """
        点击品牌

        Args:
            brand_name: 品牌名称
        """
        log.step(f"Clicking brand: {brand_name}")
        brand_locator = (By.XPATH, f"//a[@href='/brand_products/{brand_name}']")
        self.click_element(brand_locator)
        return self

    def get_product_count(self) -> int:
        """获取产品数量"""
        products = self.get_elements(self.PRODUCT_ITEMS)
        count = len(products)
        log.step(f"Found {count} products on page")
        return count

    def get_product_names(self) -> list:
        """获取所有产品名称"""
        elements = self.get_elements(self.PRODUCT_NAMES)
        names = [element.text for element in elements]
        log.step(f"Got product names: {names}")
        return names

    def get_product_prices(self) -> list:
        """获取所有产品价格"""
        elements = self.get_elements(self.PRODUCT_PRICES)
        prices = [element.text for element in elements]
        log.step(f"Got product prices: {prices}")
        return prices

    def click_add_to_cart_by_index(self, index: int = 0):
        """
        通过索引点击添加到购物车按钮

        Args:
            index: 产品索引
        """
        log.step(f"Adding product {index} to cart")
        buttons = self.get_elements(self.ADD_TO_CART_BUTTONS)
        if index < len(buttons):
            buttons[index].click()
        return self

    def click_view_product_by_index(self, index: int = 0):
        """
        通过索引点击查看产品

        Args:
            index: 产品索引
        """
        log.step(f"Viewing product {index}")
        links = self.get_elements(self.VIEW_PRODUCT_LINKS)
        if index < len(links):
            links[index].click()
        return self

    def hover_on_product(self, index: int = 0):
        """
        鼠标悬停在产品上

        Args:
            index: 产品索引
        """
        log.step(f"Hovering on product {index}")
        products = self.get_elements(self.PRODUCT_ITEMS)
        if index < len(products):
            self.driver.execute_script("arguments[0].scrollIntoView(true);", products[index])
            from selenium.webdriver.common.action_chains import ActionChains
            ActionChains(self.driver).move_to_element(products[index]).perform()
        return self

    def subscribe_to_newsletter(self, email: str) -> bool:
        """
        订阅邮件

        Args:
            email: 邮箱地址

        Returns:
            是否订阅成功
        """
        log.step(f"Subscribing to newsletter with email: {email}")

        # 滚动到页脚
        self.scroll_to_element(self.EMAIL_INPUT)

        # 输入邮箱
        if not self.send_keys(self.EMAIL_INPUT, email):
            return False

        # 点击订阅按钮
        if not self.click_element(self.SUBSCRIBE_BUTTON):
            return False

        # 验证成功消息
        return self.verify_element_visible(self.SUCCESS_MESSAGE, timeout=5)

    def scroll_to_top_of_page(self):
        """滚动到页面顶部"""
        log.step("Scrolling to top of page")
        self.scroll_to_top()
        return self

    def scroll_to_bottom_of_page(self):
        """滚动到页面底部"""
        log.step("Scrolling to bottom of page")
        self.scroll_to_bottom()
        return self

    def verify_subscription_section(self) -> bool:
        """验证订阅区域可见"""
        log.step("Verifying subscription section")
        return self.verify_element_visible(self.SUBSCRIPTION_TITLE)

    def verify_categories_section(self) -> bool:
        """验证分类区域可见"""
        log.step("Verifying categories section")
        return self.verify_element_visible(self.CATEGORY_TITLE)

    def verify_brands_section(self) -> bool:
        """验证品牌区域可见"""
        log.step("Verifying brands section")
        return self.verify_element_visible(self.BRANDS_TITLE)

    def verify_recommended_items_section(self) -> bool:
        """验证推荐商品区域可见"""
        log.step("Verifying recommended items section")
        return self.verify_element_visible(self.RECOMMENDED_ITEMS_TITLE)

    def get_navigation_links(self) -> dict:
        """获取导航链接状态"""
        log.step("Getting navigation links status")
        links = {
            "home": self.is_element_visible(self.HOME_LINK),
            "products": self.is_element_visible(self.PRODUCTS_LINK),
            "cart": self.is_element_visible(self.CART_LINK),
            "signup_login": self.is_element_visible(self.SIGNUP_LOGIN_LINK),
            "contact_us": self.is_element_visible(self.CONTACT_US_LINK)
        }
        return links
