"""
登录/注册页面对象
AutomationExercise网站登录和注册页面
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import log


class LoginPage(BasePage):
    """登录/注册页面对象"""

    # 新用户注册区域
    NEW_USER_SIGNUP = (By.XPATH, "//h2[text()='New User Signup!']")
    SIGNUP_NAME_INPUT = (By.XPATH, "//input[@data-qa='signup-name']")
    SIGNUP_EMAIL_INPUT = (By.XPATH, "//input[@data-qa='signup-email']")
    SIGNUP_BUTTON = (By.XPATH, "//button[@data-qa='signup-button']")

    # 登录区域
    LOGIN_TO_ACCOUNT = (By.XPATH, "//h2[text()='Login to your account']")
    LOGIN_EMAIL_INPUT = (By.XPATH, "//input[@data-qa='login-email']")
    LOGIN_PASSWORD_INPUT = (By.XPATH, "//input[@data-qa='login-password']")
    LOGIN_BUTTON = (By.XPATH, "//button[@data-qa='login-button']")

    # 错误消息
    ERROR_MESSAGE = (By.XPATH, "//p[contains(@style, 'color: red')]")
    EMAIL_ALREADY_EXISTS_ERROR = (By.XPATH, "//p[text()='Email Address already exist!']")
    INCORRECT_LOGIN_ERROR = (By.XPATH, "//p[text()='Your email or password is incorrect!']")

    # 成功消息
    SUCCESS_MESSAGE = (By.CLASS_NAME, "alert-success")

    def __init__(self, driver):
        """初始化登录页面"""
        super().__init__(driver)
        self.page_url = f"{self.base_url}/login"

    def open_login_page(self):
        """打开登录页面"""
        self.open_page(self.page_url)
        log.step("Opened login page")
        return self

    def verify_page_loaded(self) -> bool:
        """验证页面加载成功"""
        log.step("Verifying login page loaded")
        return (self.verify_element_visible(self.NEW_USER_SIGNUP) and
                self.verify_element_visible(self.LOGIN_TO_ACCOUNT))

    def verify_signup_section_visible(self) -> bool:
        """验证注册区域可见"""
        log.step("Verifying signup section visible")
        return self.verify_element_visible(self.NEW_USER_SIGNUP)

    def verify_login_section_visible(self) -> bool:
        """验证登录区域可见"""
        log.step("Verifying login section visible")
        return self.verify_element_visible(self.LOGIN_TO_ACCOUNT)

    def fill_signup_form(self, name: str, email: str):
        """
        填写注册表单

        Args:
            name: 用户名
            email: 邮箱地址
        """
        log.step(f"Filling signup form with name: {name}, email: {email}")

        # 输入姓名
        if not self.send_keys(self.SIGNUP_NAME_INPUT, name):
            log.error("Failed to enter signup name")
            return False

        # 输入邮箱
        if not self.send_keys(self.SIGNUP_EMAIL_INPUT, email):
            log.error("Failed to enter signup email")
            return False

        return True

    def click_signup_button(self):
        """点击注册按钮"""
        log.step("Clicking signup button")
        self.click_element(self.SIGNUP_BUTTON)
        return self

    def signup_new_user(self, name: str, email: str):
        """
        注册新用户

        Args:
            name: 用户名
            email: 邮箱地址
        """
        log.step(f"Signing up new user: {name}")
        self.fill_signup_form(name, email)
        self.click_signup_button()
        return self

    def fill_login_form(self, email: str, password: str):
        """
        填写登录表单

        Args:
            email: 邮箱地址
            password: 密码
        """
        log.step(f"Filling login form with email: {email}")

        # 输入邮箱
        if not self.send_keys(self.LOGIN_EMAIL_INPUT, email):
            log.error("Failed to enter login email")
            return False

        # 输入密码
        if not self.send_keys(self.LOGIN_PASSWORD_INPUT, password):
            log.error("Failed to enter login password")
            return False

        return True

    def click_login_button(self):
        """点击登录按钮"""
        log.step("Clicking login button")
        self.click_element(self.LOGIN_BUTTON)
        return self

    def login_user(self, email: str, password: str):
        """
        用户登录

        Args:
            email: 邮箱地址
            password: 密码
        """
        log.step(f"Logging in user: {email}")
        self.fill_login_form(email, password)
        self.click_login_button()
        return self

    def get_error_message(self) -> str:
        """获取错误消息"""
        log.step("Getting error message")
        return self.get_text(self.ERROR_MESSAGE)

    def verify_email_already_exists_error(self) -> bool:
        """验证邮箱已存在错误"""
        log.step("Verifying email already exists error")
        return self.verify_element_visible(self.EMAIL_ALREADY_EXISTS_ERROR)

    def verify_incorrect_login_error(self) -> bool:
        """验证登录错误"""
        log.step("Verifying incorrect login error")
        return self.verify_element_visible(self.INCORRECT_LOGIN_ERROR)

    def verify_signup_form_fields(self) -> bool:
        """验证注册表单字段"""
        log.step("Verifying signup form fields")
        return (self.verify_element_visible(self.SIGNUP_NAME_INPUT) and
                self.verify_element_visible(self.SIGNUP_EMAIL_INPUT) and
                self.verify_element_visible(self.SIGNUP_BUTTON))

    def verify_login_form_fields(self) -> bool:
        """验证登录表单字段"""
        log.step("Verifying login form fields")
        return (self.verify_element_visible(self.LOGIN_EMAIL_INPUT) and
                self.verify_element_visible(self.LOGIN_PASSWORD_INPUT) and
                self.verify_element_visible(self.LOGIN_BUTTON))

    def clear_signup_form(self):
        """清空注册表单"""
        log.step("Clearing signup form")
        self.clear_and_send_keys(self.SIGNUP_NAME_INPUT, "")
        self.clear_and_send_keys(self.SIGNUP_EMAIL_INPUT, "")
        return self

    def clear_login_form(self):
        """清空登录表单"""
        log.step("Clearing login form")
        self.clear_and_send_keys(self.LOGIN_EMAIL_INPUT, "")
        self.clear_and_send_keys(self.LOGIN_PASSWORD_INPUT, "")
        return self

    def get_signup_name_value(self) -> str:
        """获取注册姓名输入框的值"""
        return self.get_attribute(self.SIGNUP_NAME_INPUT, "value")

    def get_signup_email_value(self) -> str:
        """获取注册邮箱输入框的值"""
        return self.get_attribute(self.SIGNUP_EMAIL_INPUT, "value")

    def get_login_email_value(self) -> str:
        """获取登录邮箱输入框的值"""
        return self.get_attribute(self.LOGIN_EMAIL_INPUT, "value")

    def is_signup_button_enabled(self) -> bool:
        """检查注册按钮是否可用"""
        return self.is_element_visible(self.SIGNUP_BUTTON)

    def is_login_button_enabled(self) -> bool:
        """检查登录按钮是否可用"""
        return self.is_element_visible(self.LOGIN_BUTTON)

    def wait_for_page_redirect(self, timeout: int = 10) -> str:
        """
        等待页面跳转并返回新的URL

        Args:
            timeout: 等待超时时间

        Returns:
            新的URL
        """
        import time
        current_url = self.get_current_url()
        start_time = time.time()

        while time.time() - start_time < timeout:
            new_url = self.get_current_url()
            if new_url != current_url:
                log.step(f"Page redirected to: {new_url}")
                return new_url
            time.sleep(0.5)

        log.warning(f"No page redirect detected within {timeout} seconds")
        return current_url
