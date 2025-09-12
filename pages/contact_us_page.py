"""
联系我们页面对象
AutomationExercise网站联系我们页面
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import log


class ContactUsPage(BasePage):
    """联系我们页面对象"""

    # 页面标题
    PAGE_TITLE = (By.XPATH, "//h2[@class='title text-center']")
    GET_IN_TOUCH_TITLE = (By.XPATH, "//h2[text()='Get In Touch']")

    # 联系表单
    NAME_INPUT = (By.XPATH, "//input[@data-qa='name']")
    EMAIL_INPUT = (By.XPATH, "//input[@data-qa='email']")
    SUBJECT_INPUT = (By.XPATH, "//input[@data-qa='subject']")
    MESSAGE_TEXTAREA = (By.XPATH, "//textarea[@data-qa='message']")

    # 文件上传
    UPLOAD_FILE_INPUT = (By.XPATH, "//input[@name='upload_file']")

    # 提交按钮
    SUBMIT_BUTTON = (By.XPATH, "//input[@data-qa='submit-button']")

    # 成功消息
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'alert-success')]")
    SUCCESS_TEXT = (By.XPATH, "//div[contains(text(), 'Success! Your details have been submitted successfully.')]")

    # 返回首页按钮
    HOME_BUTTON = (By.XPATH, "//a[contains(@class, 'btn') and text()=' Home']")

    # 联系信息区域
    CONTACT_INFO = (By.XPATH, "//div[@class='contact-info']")

    def __init__(self, driver):
        """初始化联系我们页面"""
        super().__init__(driver)
        self.page_url = f"{self.base_url}/contact_us"

    def open_contact_us_page(self):
        """打开联系我们页面"""
        self.open_page(self.page_url)
        log.step("Opened contact us page")
        return self

    def verify_page_loaded(self) -> bool:
        """验证页面加载成功"""
        log.step("Verifying contact us page loaded")
        return self.verify_element_visible(self.GET_IN_TOUCH_TITLE)

    def verify_get_in_touch_title(self) -> bool:
        """验证'Get In Touch'标题"""
        log.step("Verifying 'Get In Touch' title")
        return self.verify_element_visible(self.GET_IN_TOUCH_TITLE)

    def fill_contact_form(self, name: str, email: str, subject: str, message: str):
        """
        填写联系表单

        Args:
            name: 姓名
            email: 邮箱
            subject: 主题
            message: 消息内容
        """
        log.step(f"Filling contact form - Name: {name}, Email: {email}")

        # 填写姓名
        self.send_keys(self.NAME_INPUT, name)

        # 填写邮箱
        self.send_keys(self.EMAIL_INPUT, email)

        # 填写主题
        self.send_keys(self.SUBJECT_INPUT, subject)

        # 填写消息
        self.send_keys(self.MESSAGE_TEXTAREA, message)

        return self

    def upload_file(self, file_path: str):
        """
        上传文件

        Args:
            file_path: 文件路径
        """
        log.step(f"Uploading file: {file_path}")

        # 确保文件输入框存在
        if self.verify_element_visible(self.UPLOAD_FILE_INPUT):
            self.send_keys(self.UPLOAD_FILE_INPUT, file_path, clear=False)

        return self

    def click_submit_button(self):
        """点击提交按钮"""
        log.step("Clicking submit button")
        self.click_element(self.SUBMIT_BUTTON)
        return self

    def handle_alert(self) -> bool:
        """
        处理JavaScript警告框

        Returns:
            是否成功处理警告框
        """
        try:
            log.step("Handling JavaScript alert")
            alert = self.driver.switch_to.alert
            alert.accept()
            log.step("Alert accepted")
            return True
        except Exception as e:
            log.warning(f"No alert found or failed to handle: {str(e)}")
            return False

    def submit_contact_form(self, contact_data: dict, file_path: str = None):
        """
        提交联系表单

        Args:
            contact_data: 联系数据字典
            file_path: 可选的文件路径
        """
        log.step("Submitting contact form")

        # 填写表单
        self.fill_contact_form(
            name=contact_data.get("name", ""),
            email=contact_data.get("email", ""),
            subject=contact_data.get("subject", ""),
            message=contact_data.get("message", "")
        )

        # 上传文件（如果提供）
        if file_path:
            self.upload_file(file_path)

        # 提交表单
        self.click_submit_button()

        # 处理可能的警告框
        self.handle_alert()

        return self

    def verify_success_message(self) -> bool:
        """验证成功消息"""
        log.step("Verifying success message")
        return (self.verify_element_visible(self.SUCCESS_MESSAGE, timeout=10) or
                self.verify_element_visible(self.SUCCESS_TEXT, timeout=10))

    def get_success_message_text(self) -> str:
        """获取成功消息文本"""
        log.step("Getting success message text")

        if self.is_element_visible(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        elif self.is_element_visible(self.SUCCESS_TEXT):
            return self.get_text(self.SUCCESS_TEXT)

        return ""

    def click_home_button(self):
        """点击返回首页按钮"""
        log.step("Clicking home button")
        self.click_element(self.HOME_BUTTON)
        return self

    def verify_form_fields_visible(self) -> bool:
        """验证表单字段可见"""
        log.step("Verifying form fields visible")

        required_fields = [
            self.NAME_INPUT,
            self.EMAIL_INPUT,
            self.SUBJECT_INPUT,
            self.MESSAGE_TEXTAREA,
            self.SUBMIT_BUTTON
        ]

        for field in required_fields:
            if not self.verify_element_visible(field):
                return False

        return True

    def clear_form(self):
        """清空表单"""
        log.step("Clearing contact form")

        self.clear_and_send_keys(self.NAME_INPUT, "")
        self.clear_and_send_keys(self.EMAIL_INPUT, "")
        self.clear_and_send_keys(self.SUBJECT_INPUT, "")
        self.clear_and_send_keys(self.MESSAGE_TEXTAREA, "")

        return self

    def get_form_field_values(self) -> dict:
        """获取表单字段值"""
        log.step("Getting form field values")

        return {
            "name": self.get_attribute(self.NAME_INPUT, "value"),
            "email": self.get_attribute(self.EMAIL_INPUT, "value"),
            "subject": self.get_attribute(self.SUBJECT_INPUT, "value"),
            "message": self.get_attribute(self.MESSAGE_TEXTAREA, "value")
        }

    def verify_form_validation(self) -> bool:
        """验证表单验证"""
        log.step("Verifying form validation")

        # 尝试提交空表单
        self.click_submit_button()

        # 检查是否有HTML5验证消息
        name_field = self.wait_for_element_visible(self.NAME_INPUT)
        if name_field:
            validation_message = name_field.get_attribute("validationMessage")
            if validation_message:
                log.step(f"Form validation detected: {validation_message}")
                return True

        return False

    def verify_contact_info_visible(self) -> bool:
        """验证联系信息可见"""
        log.step("Verifying contact info visible")
        return self.verify_element_visible(self.CONTACT_INFO)
