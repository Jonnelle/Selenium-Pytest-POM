"""
基础测试类
所有测试类的基础类
"""
import pytest
import allure
import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.account_created_page import AccountCreatedPage
from pages.products_page import ProductsPage
from pages.contact_us_page import ContactUsPage
from pages.cart_page import CartPage
from utils.logger import log


class BaseTest:
    """基础测试类"""

    def setup_method(self, method):
        """测试方法设置"""
        self.test_start_time = time.time()
        log.test_start(method.__name__)

    def teardown_method(self, method):
        """测试方法清理"""
        duration = time.time() - self.test_start_time
        log.test_end(method.__name__, "COMPLETED", duration)

    @pytest.fixture(autouse=True)
    def setup(self, browser_setup, config, test_data):
        """自动设置fixture"""
        self.driver = browser_setup
        self.config = config
        self.test_data = test_data

        # 初始化页面对象
        self.home_page = HomePage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.signup_page = SignupPage(self.driver)
        self.account_created_page = AccountCreatedPage(self.driver)
        self.products_page = ProductsPage(self.driver)
        self.contact_us_page = ContactUsPage(self.driver)
        self.cart_page = CartPage(self.driver)

    def take_screenshot(self, name: str = None) -> str:
        """
        截图

        Args:
            name: 截图名称

        Returns:
            截图文件路径
        """
        if not name:
            test_name = self.__class__.__name__
            timestamp = int(time.time())
            name = f"{test_name}_{timestamp}"

        screenshot_path = self.home_page.take_screenshot(name)

        # 添加到Allure报告
        allure.attach.file(
            screenshot_path,
            name=f"Screenshot_{name}",
            attachment_type=allure.attachment_type.PNG
        )

        return screenshot_path

    def attach_page_source(self, name: str = "Page Source"):
        """
        附加页面源码到Allure报告

        Args:
            name: 附件名称
        """
        page_source = self.driver.page_source
        allure.attach(
            page_source,
            name=name,
            attachment_type=allure.attachment_type.HTML
        )

    def verify_page_loaded(self, page_object, page_name: str) -> bool:
        """
        通用页面加载验证

        Args:
            page_object: 页面对象
            page_name: 页面名称

        Returns:
            是否加载成功
        """
        with allure.step(f"验证{page_name}页面加载"):
            is_loaded = page_object.verify_page_loaded()
            if not is_loaded:
                self.take_screenshot(f"{page_name}_load_failed")
                log.error(f"{page_name}页面加载失败")
            return is_loaded

    def navigate_to_home(self):
        """导航到首页"""
        with allure.step("导航到首页"):
            self.home_page.open_home_page()
            return self.verify_page_loaded(self.home_page, "首页")

    def navigate_to_login(self):
        """导航到登录页面"""
        with allure.step("导航到登录页面"):
            self.login_page.open_login_page()
            return self.verify_page_loaded(self.login_page, "登录页面")

    def navigate_to_products(self):
        """导航到产品页面"""
        with allure.step("导航到产品页面"):
            self.products_page.open_products_page()
            return self.verify_page_loaded(self.products_page, "产品页面")

    def navigate_to_contact_us(self):
        """导航到联系我们页面"""
        with allure.step("导航到联系我们页面"):
            self.contact_us_page.open_contact_us_page()
            return self.verify_page_loaded(self.contact_us_page, "联系我们页面")

    def navigate_to_cart(self):
        """导航到购物车页面"""
        with allure.step("导航到购物车页面"):
            self.cart_page.open_cart_page()
            return self.verify_page_loaded(self.cart_page, "购物车页面")

    def register_new_user(self, user_data: dict = None) -> bool:
        """
        注册新用户的通用方法

        Args:
            user_data: 用户数据，如果为None则生成随机用户

        Returns:
            是否注册成功
        """
        if user_data is None:
            user_data = self.test_data.generate_test_user()

        with allure.step(f"注册新用户: {user_data['first_name']} {user_data['last_name']}"):
            # 导航到登录页面
            if not self.navigate_to_login():
                return False

            # 填写注册表单
            self.login_page.signup_new_user(
                name=f"{user_data['first_name']} {user_data['last_name']}",
                email=user_data['email']
            )

            # 验证注册页面加载
            if not self.verify_page_loaded(self.signup_page, "注册详情页面"):
                return False

            # 完成注册
            self.signup_page.complete_registration(user_data)

            # 验证账户创建成功
            return self.verify_page_loaded(self.account_created_page, "账户创建成功页面")

    def login_user(self, email: str = None, password: str = None) -> bool:
        """
        用户登录的通用方法

        Args:
            email: 邮箱
            password: 密码

        Returns:
            是否登录成功
        """
        if email is None or password is None:
            user_data = self.test_data.get_user_data()
            email = user_data.get("valid_user", {}).get("email", "testuser@example.com")
            password = user_data.get("valid_user", {}).get("password", "Test123456")

        with allure.step(f"用户登录: {email}"):
            # 导航到登录页面
            if not self.navigate_to_login():
                return False

            # 执行登录
            self.login_page.login_user(email, password)

            # 验证登录成功（通过URL变化或页面元素）
            time.sleep(2)  # 等待页面跳转
            current_url = self.driver.current_url

            # 如果URL包含login，说明登录失败
            if "/login" in current_url:
                log.error("登录失败，仍在登录页面")
                return False

            log.step(f"登录成功，当前URL: {current_url}")
            return True

    def add_product_to_cart(self, product_index: int = 0) -> bool:
        """
        添加产品到购物车的通用方法

        Args:
            product_index: 产品索引

        Returns:
            是否添加成功
        """
        with allure.step(f"添加第{product_index + 1}个产品到购物车"):
            # 导航到首页
            if not self.navigate_to_home():
                return False

            # 添加产品到购物车
            self.home_page.add_product_to_cart_by_index(product_index)

            # 等待模态框出现
            time.sleep(2)

            return True

    def perform_search(self, search_term: str) -> bool:
        """
        执行产品搜索

        Args:
            search_term: 搜索词

        Returns:
            是否搜索成功
        """
        with allure.step(f"搜索产品: {search_term}"):
            # 导航到产品页面
            if not self.navigate_to_products():
                return False

            # 执行搜索
            self.products_page.search_product(search_term)

            # 验证搜索结果
            return self.products_page.verify_searched_products_title()

    def submit_contact_form(self, contact_data: dict = None) -> bool:
        """
        提交联系表单

        Args:
            contact_data: 联系数据

        Returns:
            是否提交成功
        """
        if contact_data is None:
            contact_data = self.test_data.generate_contact_data()

        with allure.step(f"提交联系表单: {contact_data['name']}"):
            # 导航到联系我们页面
            if not self.navigate_to_contact_us():
                return False

            # 提交表单
            self.contact_us_page.submit_contact_form(contact_data)

            # 验证成功消息
            return self.contact_us_page.verify_success_message()

    def cleanup_test_data(self):
        """清理测试数据"""
        with allure.step("清理测试数据"):
            try:
                # 清空购物车（如果需要）
                self.navigate_to_cart()
                if self.cart_page.verify_cart_has_items():
                    self.cart_page.clear_cart()
                    log.step("购物车已清空")
            except Exception as e:
                log.warning(f"清理测试数据时出现错误: {str(e)}")

    def assert_with_screenshot(self, condition: bool, message: str):
        """
        带截图的断言

        Args:
            condition: 断言条件
            message: 错误消息
        """
        if not condition:
            self.take_screenshot("assertion_failed")
            self.attach_page_source()

        assert condition, message
