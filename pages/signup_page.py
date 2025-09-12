"""
注册表单页面对象
AutomationExercise网站用户注册详细信息页面
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import log


class SignupPage(BasePage):
    """注册表单页面对象"""

    # 页面标题
    PAGE_TITLE = (By.XPATH, "//b[text()='Enter Account Information']")

    # 账户信息区域
    ACCOUNT_INFO_TITLE = (By.XPATH, "//h2[@class='title text-center']/b[text()='Enter Account Information']")

    # 性别选择
    TITLE_MR = (By.ID, "id_gender1")
    TITLE_MRS = (By.ID, "id_gender2")

    # 用户信息
    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")

    # 生日选择
    BIRTH_DAY_SELECT = (By.ID, "days")
    BIRTH_MONTH_SELECT = (By.ID, "months")
    BIRTH_YEAR_SELECT = (By.ID, "years")

    # 复选框
    NEWSLETTER_CHECKBOX = (By.ID, "newsletter")
    SPECIAL_OFFERS_CHECKBOX = (By.ID, "optin")

    # 地址信息
    ADDRESS_INFO_TITLE = (By.XPATH, "//h2[@class='title text-center']/b[text()='Address Information']")
    FIRST_NAME_INPUT = (By.ID, "first_name")
    LAST_NAME_INPUT = (By.ID, "last_name")
    COMPANY_INPUT = (By.ID, "company")
    ADDRESS1_INPUT = (By.ID, "address1")
    ADDRESS2_INPUT = (By.ID, "address2")
    COUNTRY_SELECT = (By.ID, "country")
    STATE_INPUT = (By.ID, "state")
    CITY_INPUT = (By.ID, "city")
    ZIPCODE_INPUT = (By.ID, "zipcode")
    MOBILE_NUMBER_INPUT = (By.ID, "mobile_number")

    # 创建账户按钮
    CREATE_ACCOUNT_BUTTON = (By.XPATH, "//button[@data-qa='create-account']")

    # 错误消息
    ERROR_MESSAGE = (By.CLASS_NAME, "alert-danger")

    def __init__(self, driver):
        """初始化注册表单页面"""
        super().__init__(driver)
        self.page_url = f"{self.base_url}/signup"

    def verify_page_loaded(self) -> bool:
        """验证页面加载成功"""
        log.step("Verifying signup page loaded")
        return self.verify_element_visible(self.PAGE_TITLE)

    def verify_account_info_section(self) -> bool:
        """验证账户信息区域"""
        log.step("Verifying account info section")
        return self.verify_element_visible(self.ACCOUNT_INFO_TITLE)

    def verify_address_info_section(self) -> bool:
        """验证地址信息区域"""
        log.step("Verifying address info section")
        return self.verify_element_visible(self.ADDRESS_INFO_TITLE)

    def select_title(self, title: str):
        """
        选择称谓

        Args:
            title: 'Mr' 或 'Mrs'
        """
        log.step(f"Selecting title: {title}")
        if title.lower() == "mr":
            self.click_element(self.TITLE_MR)
        elif title.lower() == "mrs":
            self.click_element(self.TITLE_MRS)
        return self

    def fill_account_information(self, password: str, birth_day: str = None,
                                birth_month: str = None, birth_year: str = None):
        """
        填写账户信息

        Args:
            password: 密码
            birth_day: 出生日期
            birth_month: 出生月份
            birth_year: 出生年份
        """
        log.step("Filling account information")

        # 输入密码
        self.send_keys(self.PASSWORD_INPUT, password)

        # 选择生日（如果提供）
        if birth_day:
            self.select_dropdown_by_value(self.BIRTH_DAY_SELECT, birth_day)

        if birth_month:
            self.select_dropdown_by_text(self.BIRTH_MONTH_SELECT, birth_month)

        if birth_year:
            self.select_dropdown_by_value(self.BIRTH_YEAR_SELECT, birth_year)

        return self

    def check_newsletter_subscription(self):
        """勾选新闻订阅"""
        log.step("Checking newsletter subscription")
        self.click_element(self.NEWSLETTER_CHECKBOX)
        return self

    def check_special_offers(self):
        """勾选特殊优惠"""
        log.step("Checking special offers")
        self.click_element(self.SPECIAL_OFFERS_CHECKBOX)
        return self

    def fill_address_information(self, user_data: dict):
        """
        填写地址信息

        Args:
            user_data: 用户数据字典
        """
        log.step("Filling address information")

        # 填写姓名
        if "first_name" in user_data:
            self.send_keys(self.FIRST_NAME_INPUT, user_data["first_name"])

        if "last_name" in user_data:
            self.send_keys(self.LAST_NAME_INPUT, user_data["last_name"])

        # 填写公司（可选）
        if "company" in user_data:
            self.send_keys(self.COMPANY_INPUT, user_data["company"])

        # 填写地址
        if "address" in user_data:
            self.send_keys(self.ADDRESS1_INPUT, user_data["address"])

        if "address2" in user_data:
            self.send_keys(self.ADDRESS2_INPUT, user_data["address2"])

        # 选择国家
        if "country" in user_data:
            self.select_dropdown_by_text(self.COUNTRY_SELECT, user_data["country"])

        # 填写州/省
        if "state" in user_data:
            self.send_keys(self.STATE_INPUT, user_data["state"])

        # 填写城市
        if "city" in user_data:
            self.send_keys(self.CITY_INPUT, user_data["city"])

        # 填写邮编
        if "zipcode" in user_data:
            self.send_keys(self.ZIPCODE_INPUT, user_data["zipcode"])

        # 填写手机号
        if "mobile_number" in user_data:
            self.send_keys(self.MOBILE_NUMBER_INPUT, user_data["mobile_number"])

        return self

    def click_create_account_button(self):
        """点击创建账户按钮"""
        log.step("Clicking create account button")
        self.scroll_to_element(self.CREATE_ACCOUNT_BUTTON)
        self.click_element(self.CREATE_ACCOUNT_BUTTON)
        return self

    def complete_registration(self, user_data: dict):
        """
        完成注册流程

        Args:
            user_data: 用户数据字典
        """
        log.step(f"Completing registration for user: {user_data.get('first_name', 'Unknown')}")

        # 选择称谓
        self.select_title("Mr")

        # 填写账户信息
        self.fill_account_information(
            password=user_data.get("password", "Test123456"),
            birth_day="1",
            birth_month="January",
            birth_year="1990"
        )

        # 勾选订阅选项
        self.check_newsletter_subscription()
        self.check_special_offers()

        # 填写地址信息
        self.fill_address_information(user_data)

        # 创建账户
        self.click_create_account_button()

        return self

    def get_name_field_value(self) -> str:
        """获取姓名字段的值"""
        return self.get_attribute(self.NAME_INPUT, "value")

    def get_email_field_value(self) -> str:
        """获取邮箱字段的值"""
        return self.get_attribute(self.EMAIL_INPUT, "value")

    def verify_name_and_email_prefilled(self, expected_name: str, expected_email: str) -> bool:
        """
        验证姓名和邮箱是否预填充

        Args:
            expected_name: 期望的姓名
            expected_email: 期望的邮箱

        Returns:
            是否预填充正确
        """
        log.step("Verifying name and email prefilled")

        actual_name = self.get_name_field_value()
        actual_email = self.get_email_field_value()

        name_match = actual_name == expected_name
        email_match = actual_email == expected_email

        log.assertion("Name prefilled", expected_name, actual_name)
        log.assertion("Email prefilled", expected_email, actual_email)

        return name_match and email_match

    def get_error_message(self) -> str:
        """获取错误消息"""
        log.step("Getting error message")
        return self.get_text(self.ERROR_MESSAGE)

    def verify_all_required_fields_visible(self) -> bool:
        """验证所有必填字段可见"""
        log.step("Verifying all required fields visible")

        required_fields = [
            self.PASSWORD_INPUT,
            self.FIRST_NAME_INPUT,
            self.LAST_NAME_INPUT,
            self.ADDRESS1_INPUT,
            self.COUNTRY_SELECT,
            self.STATE_INPUT,
            self.CITY_INPUT,
            self.ZIPCODE_INPUT,
            self.MOBILE_NUMBER_INPUT
        ]

        for field in required_fields:
            if not self.verify_element_visible(field):
                return False

        return True

    def get_selected_country(self) -> str:
        """获取选中的国家"""
        from selenium.webdriver.support.ui import Select
        element = self.wait_for_element_visible(self.COUNTRY_SELECT)
        if element:
            select = Select(element)
            return select.first_selected_option.text
        return ""

    def get_available_countries(self) -> list:
        """获取可用的国家列表"""
        from selenium.webdriver.support.ui import Select
        element = self.wait_for_element_visible(self.COUNTRY_SELECT)
        if element:
            select = Select(element)
            return [option.text for option in select.options]
        return []
